"""Microsoft/NTU browser sign-in used only when no validated session is found."""

import re
import time
from urllib.parse import urlsplit

from shared.credentials import Credentials

from ..models import LearnError
from .browser_cookies import BASE_URL, SessionCookie, playwright_cookies

TIMEOUT_MS = 30_000
_MICROSOFT = "login.microsoftonline.com"
_FEDERATION = "loginfs.ntu.edu.sg"
_BLACKBOARD = "ntulearn.ntu.edu.sg"
_CHALLENGE = re.compile(
    r"captcha|approve (?:the )?sign.in|verify your identity|verification code|authenticator|multi.factor|security info",
    re.I,
)


def _https_host(url: str) -> str | None:
    try:
        parsed = urlsplit(url)
        if (
            parsed.scheme == "https"
            and parsed.port in (None, 443)
            and parsed.username is None
            and parsed.password is None
        ):
            return parsed.hostname
    except ValueError:
        pass
    return None


async def _check_form(page, field, expected_host: str) -> None:
    if _https_host(page.url) != expected_host:
        raise LearnError("The sign-in page changed before submission.")
    form = await field.evaluate(
        """input => input.form && ({
            action: input.getAttribute('formaction') ? input.formAction : input.form.action,
            method: input.getAttribute('formmethod') ? input.formMethod : input.form.method
        })"""
    )
    if (
        not form
        or form["method"] != "post"
        or _https_host(form["action"]) != expected_host
    ):
        raise LearnError("The identity provider returned an unexpected sign-in form.")


async def login(
    credentials: Credentials, *, headless: bool
) -> tuple[SessionCookie, ...]:
    """Run the regular NTU SSO flow; interactive challenges are never bypassed."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise LearnError(
            "Automatic NTULearn sign-in needs the optional personal dependencies and Chromium."
        ) from None

    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=headless)
            try:
                context = await browser.new_context(locale="en-US")
                page = await context.new_page()
                await page.goto(
                    BASE_URL, wait_until="domcontentloaded", timeout=TIMEOUT_MS
                )
                deadline = time.monotonic() + (60 if headless else 180)
                username_sent = password_sent = False
                while time.monotonic() < deadline:
                    host = _https_host(page.url)
                    if host not in {_BLACKBOARD, _MICROSOFT, _FEDERATION}:
                        raise LearnError(
                            "The login reached an unexpected host; no further credentials were submitted."
                        )
                    if host == _BLACKBOARD and urlsplit(page.url).path.startswith(
                        "/ultra/"
                    ):
                        cookies = playwright_cookies(await context.cookies(BASE_URL))
                        if cookies:
                            return cookies
                        raise LearnError(
                            "NTULearn did not provide a usable authenticated browser session."
                        )

                    body = await page.locator("body").inner_text(timeout=5000)
                    if _CHALLENGE.search(body):
                        if headless:
                            raise LearnError(
                                "NTULearn requires MFA or CAPTCHA. Set NTULEARN_HEADLESS=false and complete it in the local browser; no security checks were bypassed."
                            )
                        await page.wait_for_timeout(500)
                        continue
                    if password_sent and re.search(
                        r"password (?:is )?incorrect|incorrect password|account.*locked|too many.*attempts|sign.in.*blocked",
                        body,
                        re.I,
                    ):
                        raise LearnError(
                            "Microsoft rejected the login or account access. Check your NTULearn credentials; no automatic password retry was made."
                        )

                    if host == _BLACKBOARD:
                        await page.wait_for_timeout(500)
                        continue
                    if host == _FEDERATION:
                        email = page.locator("#userNameInput:visible")
                        password = page.locator("#passwordInput:visible")
                        next_button = submit = page.locator("#submitButton:visible")
                    else:
                        email = page.locator('input[name="loginfmt"]:visible')
                        password = page.locator('input[name="passwd"]:visible')
                        next_button = page.get_by_role(
                            "button", name="Next", exact=True
                        )
                        submit = page.get_by_role("button", name="Sign in", exact=True)
                    if (
                        host == _FEDERATION
                        and not password_sent
                        and await password.count()
                    ):
                        await _check_form(page, email, host)
                        await _check_form(page, password, host)
                        await email.fill(credentials.email)
                        await password.fill(credentials.password)
                        password_sent = True
                        await _check_form(page, password, host)
                        await _check_form(page, submit, host)
                        await submit.click()
                    elif not username_sent and await email.count():
                        await _check_form(page, email, host)
                        await email.fill(credentials.email)
                        username_sent = True
                        await _check_form(page, email, host)
                        await _check_form(page, next_button, host)
                        await next_button.click()
                    elif not password_sent and await password.count():
                        await submit.wait_for(state="visible", timeout=TIMEOUT_MS)
                        await _check_form(page, password, host)
                        await password.fill(credentials.password)
                        password_sent = True
                        await _check_form(page, password, host)
                        await _check_form(page, submit, host)
                        await submit.click()
                    elif (
                        "Stay signed in?" in body
                        and await page.locator("#idBtn_Back:visible").count()
                    ):
                        await page.locator("#idBtn_Back").click()
                    await page.wait_for_timeout(500)
                raise LearnError(
                    "NTULearn login did not finish. Check the account and complete any required interaction in a visible browser."
                )
            finally:
                await browser.close()
    except LearnError:
        raise
    except Exception:  # noqa: BLE001 - browser exceptions can include credentials, URLs, or page contents.
        raise LearnError(
            "NTULearn login failed or timed out; no automatic password retry was made."
        ) from None
