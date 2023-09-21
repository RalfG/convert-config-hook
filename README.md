# convert-config-hook
Pre-commit hook to interconvert JSON/TOML/YAML files.


## Usage

Add the following to your `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/ralfg/convert-config-hook
    rev: 0.1.6
    hooks:
      - id: convert-config
        files: "examples\\/.*-ms2rescore\\.toml"
        args: ["--output-format", "json"]
```

where `rev` is the latest version tag of this project. Use `files` to specify which files to convert. In `args`, use `--output-format` to specify the output format.


## Contributing

All contributions are welcome! Please open an issue or a pull request.

For local development, clone the repository and install the Python project with:

```sh
pip install --editable .
```
