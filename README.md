# convert-config-hook
Pre-commit hook to interconvert JSON/TOML/YAML files.


## About

The script `convert.py` supports conversion between JSON, TOML, and YAML files in each direction. This script can be added as a pre-commit hook to ensure that certain files in your repository are aways the same across file formats (e.g., the same configuration in both YAML and TOML formats).


## Usage

Add the following to your `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/ralfg/convert-config-hook
    rev: 0.1.6
    hooks:
      - id: convert-config
        files: "examples\\/.*\\.(toml|yaml)"
        args: ["--output-format", "json"]
```

where `rev` is the latest version tag of this project. Use `files` to specify which files to convert. In `args`, use `--output-format` to specify the output format.

The above example will convert all TOML and YAML files in the `examples` folder to JSON.

## Contributing

All contributions are welcome! Please open an issue or a pull request.

For local development, clone the repository and install the Python project with:

```sh
pip install --editable .
```
