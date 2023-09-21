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
        "read_mode": "rt",
        "write_mode": "wt",
        "extensions": [".json"],
    },
    "toml": {
        "load": tomli_r.load,
        "dump": tomli_w.dump,
        "read_mode": "rb",
        "write_mode": "wb",
        "extensions": [".toml", ".tml"],
    },
    "yaml": {
        "load": yaml.safe_load,
        "dump": yaml.dump,
        "read_mode": "rt",
        "write_mode": "wt",
        "extensions": [".yaml", ".yml"],
    },
}


def convert(input_file, output_file, input_format, output_format):
    # Check if the input and output formats are supported
    if input_format not in FORMATS or output_format not in FORMATS:
        raise ValueError("Unsupported input or output format")

    # Read the input file
    with open(input_file, FORMATS[input_format]["read_mode"]) as file:
        data = FORMATS[input_format]["load"](file)

    # Write the output file
    with open(output_file, FORMATS[output_format]["write_mode"]) as file:
        FORMATS[output_format]["dump"](data, file)

    logging.info(
        f"Conversion successful: {input_format.upper()} -> {output_format.upper()}"
    )


def main():
    parser = argparse.ArgumentParser(description="Convert JSON, TOML, and YAML files.")
    parser.add_argument("input_file", type=Path, help="Input file to convert")
    parser.add_argument("--output_file", type=Path, help="Output file after conversion")
    parser.add_argument(
        "--input-format",
        choices=FORMATS.keys(),
        help="Specify the input format (json, toml, yaml).",
    )
    parser.add_argument(
        "--output-format",
        choices=FORMATS.keys(),
        help="Specify the output format (json, toml, yaml).",
    )

    args = parser.parse_args()

    # Automatically detect input format from file extension if not specified
    if not args.input_format:
        input_extension = args.input_file.suffix.lower()
        for format_name, format_info in FORMATS.items():
            if input_extension in format_info["extensions"]:
                input_format = format_name
                break
        else:
            raise ValueError("Input format could not be detected")
    else:
        input_format = args.input_format

    # Automatically detect output format from file extension if not specified
    if not args.output_format:
        if args.output_file is None:
            raise ValueError("Output format must be specified if output file is not")
        output_extension = args.output_file.suffix.lower()
        for format_name, format_info in FORMATS.items():
            if output_extension in format_info["extensions"]:
                output_format = format_name
                break
        else:
            raise ValueError("Output format could not be detected")
    else:
        output_format = args.output_format

    # Automatically set output file if not specified
    if not args.output_file:
        args.output_file = args.input_file.with_suffix(
            FORMATS[output_format]["extensions"][0]
        )

    # Convert the file
    try:
        convert(args.input_file, args.output_file, input_format, output_format)
    except Exception as e:
        logging.exception(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
