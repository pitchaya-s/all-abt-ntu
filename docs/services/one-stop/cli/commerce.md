# One Stop: Payments, cart and favourites CLI commands

[One Stop overview](../index.md) · [All One Stop CLI topics](index.md) · [MCP reference](../mcp/index.md)

A checkout link opens the native payment gateway; generating one does not complete payment. Checkout is reviewed and confirmed in a single interactive invocation. Loading a saved cart appends items; replacing it replaces the current cart.

```sh
ntu onestop cart show
ntu onestop favourites list
ntu onestop payments services
```

Replace capitalized placeholders with values returned by the service. Use `--help` after a command for its current options. Choose a command to see its arguments, examples and result fields.

| Command | What it does |
| --- | --- |
| [`ntu onestop cart quantity`](commerce.md#cmd-onestop-cart-quantity) | Set the quantity of an item in your active cart. |
| [`ntu onestop cart remove`](commerce.md#cmd-onestop-cart-remove) | Remove an item from your active cart. |
| [`ntu onestop cart clear`](commerce.md#cmd-onestop-cart-clear) | Remove all items from your active cart. |
| [`ntu onestop cart checkout`](commerce.md#cmd-onestop-cart-checkout) | Review and submit a cart checkout in one session. |
| [`ntu onestop cart show`](commerce.md#cmd-onestop-cart-show) | Read your native shopping cart, item quantities/prices, saved-cart IDs/names and checkout defaults. |
| [`ntu onestop cart saved show`](commerce.md#cmd-onestop-cart-saved-show) | Inspect items in a verified own saved cart before loading it. |
| [`ntu onestop cart saved load`](commerce.md#cmd-onestop-cart-saved-load) | Append the items from a saved cart to your active cart. |
| [`ntu onestop cart saved replace`](commerce.md#cmd-onestop-cart-saved-replace) | Replace your active cart with the items from a saved cart. |
| [`ntu onestop cart saved delete`](commerce.md#cmd-onestop-cart-saved-delete) | Delete a saved cart. |
| [`ntu onestop cart saved create`](commerce.md#cmd-onestop-cart-saved-create) | Save the current cart, or selected own cart item IDs, as a new named cart using native name/selection validation. |
| [`ntu onestop favourites pin`](commerce.md#cmd-onestop-favourites-pin) | Pin a saved favourite to the homepage. |
| [`ntu onestop favourites unpin`](commerce.md#cmd-onestop-favourites-unpin) | Unpin a favourite from the homepage. |
| [`ntu onestop favourites remove`](commerce.md#cmd-onestop-favourites-remove) | Remove a saved favourite. |
| [`ntu onestop favourites clear`](commerce.md#cmd-onestop-favourites-clear) | Remove eligible saved favourites. |
| [`ntu onestop favourites list`](commerce.md#cmd-onestop-favourites-list) | Read your saved catalog favourites and which are pinned to the homepage. |
| [`ntu onestop payments services`](commerce.md#cmd-onestop-payments-services) | Search/browse services in the student's native payment directory, preserving its active/category/access filter. |
| [`ntu onestop payments service`](commerce.md#cmd-onestop-payments-service) | Read a visible payment service's native fixed-amount information. |
| [`ntu onestop payments checkout-link`](commerce.md#cmd-onestop-payments-checkout-link) | Ask One Stop to prepare a checkout link for a visible payment service. |

## Command details

<a id="cmd-onestop-cart-quantity"></a>
### `ntu onestop cart quantity`

Set the quantity of an item in your active cart.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop cart quantity ITEM_ID 1
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop cart quantity --help` for the current interface.

#### Arguments and options

- `ITEM_ID`: **Required.** The item ID returned by the relevant listing or details command.
- `QUANTITY`: **Required.** The desired item quantity.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_update_cart).

<a id="cmd-onestop-cart-remove"></a>
### `ntu onestop cart remove`

Remove an item from your active cart.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop cart remove ITEM_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop cart remove --help` for the current interface.

#### Arguments and options

- `ITEM_ID`: **Required.** The item ID returned by the relevant listing or details command.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_update_cart).

<a id="cmd-onestop-cart-clear"></a>
### `ntu onestop cart clear`

Remove all items from your active cart.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop cart clear
```

Use `ntu onestop cart clear --help` for the current interface.

#### Arguments and options

- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_update_cart).

<a id="cmd-onestop-cart-checkout"></a>
### `ntu onestop cart checkout`

Review and submit a cart checkout in one session.

This interactive workflow keeps its temporary state in one process and asks for confirmation before submitting.

#### Usage

```sh
ntu onestop cart checkout
```

Use `ntu onestop cart checkout --help` for the current interface.

#### Arguments and options

This command has no arguments or options other than `--help`.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_submit_cart_checkout).

<a id="cmd-onestop-cart-show"></a>
### `ntu onestop cart show`

Read your native shopping cart, item quantities/prices, saved-cart IDs/names and checkout defaults.

#### Usage

```sh
ntu onestop cart show
```

Use `ntu onestop cart show --help` for the current interface.

#### Arguments and options

- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `items`, `saved_carts`, `delivery_address`, `special_instructions`, `two_step_checkout`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_get_cart).

<a id="cmd-onestop-cart-saved-show"></a>
### `ntu onestop cart saved show`

Inspect items in a verified own saved cart before loading it.

#### Usage

```sh
ntu onestop cart saved show SAVED_CART_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop cart saved show --help` for the current interface.

#### Arguments and options

- `SAVED_CART_ID`: **Required.** The saved cart ID returned by the relevant listing or details command.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `records`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_get_saved_cart).

<a id="cmd-onestop-cart-saved-load"></a>
### `ntu onestop cart saved load`

Append the items from a saved cart to your active cart.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop cart saved load SAVED_CART_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop cart saved load --help` for the current interface.

#### Arguments and options

- `SAVED_CART_ID`: **Required.** The saved cart ID returned by the relevant listing or details command.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_update_cart).

<a id="cmd-onestop-cart-saved-replace"></a>
### `ntu onestop cart saved replace`

Replace your active cart with the items from a saved cart.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop cart saved replace SAVED_CART_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop cart saved replace --help` for the current interface.

#### Arguments and options

- `SAVED_CART_ID`: **Required.** The saved cart ID returned by the relevant listing or details command.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_update_cart).

<a id="cmd-onestop-cart-saved-delete"></a>
### `ntu onestop cart saved delete`

Delete a saved cart.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop cart saved delete SAVED_CART_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop cart saved delete --help` for the current interface.

#### Arguments and options

- `SAVED_CART_ID`: **Required.** The saved cart ID returned by the relevant listing or details command.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_update_cart).

<a id="cmd-onestop-cart-saved-create"></a>
### `ntu onestop cart saved create`

Save the current cart, or selected own cart item IDs, as a new named cart using native name/selection validation.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop cart saved create NAME
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop cart saved create --help` for the current interface.

#### Arguments and options

- `NAME`: **Required.** The name of the item, setting or field to use.
- `--item-ids`: A JSON array of selected item IDs.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_save_cart).

<a id="cmd-onestop-favourites-pin"></a>
### `ntu onestop favourites pin`

Pin a saved favourite to the homepage.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop favourites pin FAVOURITE_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop favourites pin --help` for the current interface.

#### Arguments and options

- `FAVOURITE_ID`: **Required.** The favourite ID returned by the relevant listing or details command.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_update_favourite).

<a id="cmd-onestop-favourites-unpin"></a>
### `ntu onestop favourites unpin`

Unpin a favourite from the homepage.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop favourites unpin FAVOURITE_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop favourites unpin --help` for the current interface.

#### Arguments and options

- `FAVOURITE_ID`: **Required.** The favourite ID returned by the relevant listing or details command.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_update_favourite).

<a id="cmd-onestop-favourites-remove"></a>
### `ntu onestop favourites remove`

Remove a saved favourite.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop favourites remove FAVOURITE_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop favourites remove --help` for the current interface.

#### Arguments and options

- `FAVOURITE_ID`: **Required.** The favourite ID returned by the relevant listing or details command.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_update_favourite).

<a id="cmd-onestop-favourites-clear"></a>
### `ntu onestop favourites clear`

Remove eligible saved favourites.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop favourites clear
```

Use `ntu onestop favourites clear --help` for the current interface.

#### Arguments and options

- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `operation`, `completed_at`, `source_url`, `resource_id`, `outcome`, `verified`, `message`, `references`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_update_favourite).

<a id="cmd-onestop-favourites-list"></a>
### `ntu onestop favourites list`

Read your saved catalog favourites and which are pinned to the homepage.

#### Usage

```sh
ntu onestop favourites list
```

Use `ntu onestop favourites list --help` for the current interface.

#### Arguments and options

- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `items`, `pinned_count`, `maximum_pins`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_list_favourites).

<a id="cmd-onestop-payments-services"></a>
### `ntu onestop payments services`

Search/browse services in the student's native payment directory, preserving its active/category/access filter.

#### Usage

```sh
ntu onestop payments services example
```

Use `ntu onestop payments services --help` for the current interface.

#### Arguments and options

- `QUERY`: The search terms. Quote multiword text so the shell passes it as one argument.
- `--limit`, `-l`: Maximum number of results to return in this page. Default: `20`.
- `--offset`: Number of results to skip before this page. Default: `0`.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `offset`, `available_count`, `total_count`, `complete`, `next_offset`, `retrieved_at`, `source_url`, `cached`, `records`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_list_payment_services).

<a id="cmd-onestop-payments-service"></a>
### `ntu onestop payments service`

Read a visible payment service's native fixed-amount information.

#### Usage

```sh
ntu onestop payments service SERVICE_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop payments service --help` for the current interface.

#### Arguments and options

- `SERVICE_ID`: **Required.** The service ID returned by the relevant listing or details command.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `retrieved_at`, `source_url`, `cached`, `service_id`, `title`, `fixed_amount`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_get_payment_service).

<a id="cmd-onestop-payments-checkout-link"></a>
### `ntu onestop payments checkout-link`

Ask One Stop to prepare a checkout link for a visible payment service.

This operation requires local confirmation and is refused when confirmation cannot be obtained interactively.

#### Usage

```sh
ntu onestop payments checkout-link SERVICE_ID
```

Replace the uppercase placeholders with values returned by the relevant listing or details command. Use `ntu onestop payments checkout-link --help` for the current interface.

#### Arguments and options

- `SERVICE_ID`: **Required.** The service ID returned by the relevant listing or details command.
- `--json`, `-j`: Write the result as JSON to stdout; diagnostics go to stderr.

#### Result

The result may include: `service_id`, `title`, `checkout_url`, `requires_browser_completion`.

For the corresponding MCP operation and its field types, see the [MCP schema](../mcp/commerce.md#onestop_prepare_payment).
