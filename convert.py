"""Simple conversion between JSON, TOML, and YAML files."""


import argparse
import json
import logging
import sys
from pathlib import Path

try:
    import tomllib as tomli_r
except ImportError:
    import tomli as tomli_r

import tomli_w
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()],
)

# Define supported file formats and their corresponding functions
FORMATS = {
    "json": {
        "load": json.load,
        "dump": json.dump,
        "dump_kwargs": {"indent": 4, "sort_keys": False},
        "read_mode": "rt",
        "write_mode": "wt",
        "extensions": [".json"],
    },
    "toml": {
        "load": tomli_r.load,
        "dump": tomli_w.dump,
        "dump_kwargs": {},
        "read_mode": "rb",
        "write_mode": "wb",
        "extensions": [".toml", ".tml"],
    },
    "yaml": {
        "load": yaml.safe_load,
        "dump": yaml.dump,
        "dump_kwargs": {},
        "read_mode": "rt",
        "write_mode": "wt",
        "extensions": [".yaml", ".yml"],
    },
}


def convert(input_file, output_file, input_format, output_format):
    """Convert between JSON, TOML, and YAML files."""
    # Check if the input and output formats are supported
    if input_format not in FORMATS or output_format not in FORMATS:
        raise ValueError("Unsupported input or output format")

    # Read the input file
    with open(input_file, FORMATS[input_format]["read_mode"]) as file:
        data = FORMATS[input_format]["load"](file)

    # Write the output file
    with open(output_file, FORMATS[output_format]["write_mode"]) as file:
        FORMATS[output_format]["dump"](data, file, **FORMATS[output_format]["dump_kwargs"])

    logging.info(
        f"Conversion successful: {input_format.upper()} -> {output_format.upper()}"
    )


def _detect_format(filename: Path) -> str:
    """Automatically detect format from file extension."""
    input_extension = filename.suffix.lower()
    for format_name, format_info in FORMATS.items():
        if input_extension in format_info["extensions"]:
            return format_name
    else:
        raise ValueError("Input format could not be detected")


def main():
    parser = argparse.ArgumentParser(description="Convert JSON, TOML, and YAML files.")
    parser.add_argument("input_files", type=Path, nargs='+', help="Input file(s) to convert")
    parser.add_argument(
        "--input-format",
        choices=FORMATS.keys(),
        help="Specify the input format (json, toml, yaml). By default derived from extension.",
    )
    parser.add_argument(
        "--output-format",
        required=True,
        choices=FORMATS.keys(),
        help="Specify the output format (json, toml, yaml).",
    )

    args = parser.parse_args()

    for input_file in args.input_files:
        input_format = args.input_format or _detect_format(input_file)
        output_format = args.output_format
        output_file = input_file.with_suffix("." + output_format)

        # Convert the file
        try:
            convert(input_file, output_file, input_format, output_format)
        except Exception as e:
            logging.exception(e)
            sys.exit(1)


if __name__ == "__main__":
    main()
