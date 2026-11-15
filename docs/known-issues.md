# Known issues and follow-up work

These are implementation limitations identified while organizing the documentation. They describe current behavior, not planned or completed fixes.

## NTULearn lecture launch URLs

The CLI can extract course and content IDs from a supported NTULearn lecture launch URL. That does not guarantee the video can be downloaded: the downloader reads the content record and supports specific Kaltura player and wrapper formats; it does not launch arbitrary LTI tools.
