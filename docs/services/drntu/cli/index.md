# DR-NTU: CLI reference

[Service overview](../index.md) · [CLI reference](index.md) · [MCP reference](../mcp/index.md)

## Example

Search publication metadata in the research repository.

```sh
ntu research search "machine learning" --page 0 --page-size 10
```

## Commands

Choose a command for its arguments, examples and result fields. Use `ntu research --help` and append `--help` to a command for option details. Each command page identifies required arguments and any defaults. See the [complete CLI reference](../../../cli/commands.md) for shared settings and all services.

### Search and browse

Search publications and explore their metadata, bundles and files. Metadata does not establish permission to download a file.

| Command | What it does |
| --- | --- |
| [`ntu research search`](repository.md#cmd-research-search) | Search DR-NTU publications by keywords or Solr query. |
| [`ntu research facets`](repository.md#cmd-research-facets) | Discover search facet names, or supply a facet name to list its values and counts for the query/scope/filters. |
| [`ntu research dataset`](repository.md#cmd-research-dataset) | Read a published DR-NTU Data dataset by doi: identifier: title, authors, descriptions, subjects, license and paginated file inventory. |
| [`ntu research browse communities`](repository.md#cmd-research-browse-communities) | Browse repository communities or collections. |
| [`ntu research browse collections`](repository.md#cmd-research-browse-collections) | Browse repository communities or collections. |
| [`ntu research bundle files`](repository.md#cmd-research-bundle-files) | List a bundle's file metadata: names, byte sizes, checksums, published rights and content URLs. |
| [`ntu research item bundles`](repository.md#cmd-research-item-bundles) | List an item's file groups. |
| [`ntu research item show`](repository.md#cmd-research-item-show) | Read a repository item's published metadata, including abstracts, citations, DOI, subjects and rights where supplied. |

### OAI-PMH

Use these commands for repository metadata harvesting. Follow returned continuation tokens when the server provides them.

| Command | What it does |
| --- | --- |
| [`ntu research oai info`](oai.md#cmd-research-oai-info) | Describe DR-NTU's OAI-PMH repository, modification-date precision, deletion policy and earliest datestamp. |
| [`ntu research oai formats`](oai.md#cmd-research-oai-formats) | List OAI metadata prefixes, namespaces and schemas. |
| [`ntu research oai sets`](oai.md#cmd-research-oai-sets) | List OAI collection/community sets. |
| [`ntu research oai records`](oai.md#cmd-research-oai-records) | Read one bounded OAI records page, defaulting to oai_dc. |
| [`ntu research oai record`](oai.md#cmd-research-oai-record) | Get one record by its OAI identifier, not a REST UUID. |
