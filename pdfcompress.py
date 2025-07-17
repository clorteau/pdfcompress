#!/usr/bin/env python3
#
# This file is part of PDFCompress. See LICENSE.txt.
# Copyright (c) 2025 Clem Lorteau

import subprocess
import os
import argparse
from __init__ import __version__

class PDFCompressor:
    def __init__(self, input_path, output_path, compression="default"):
        self.input = input_path
        self.output = output_path
        self.compression = compression

    def compress(self):
        if not os.path.isfile(self.input):
            raise FileNotFoundError(f"Input file '{self.input}' does not exist.")

        valid_settings = {"screen", "ebook", "prepress", "printer", "default"}
        if self.compression.lower() not in valid_settings:
            raise ValueError(f"Invalid compression setting: {self.compression}")

        setting = f"/{self.compression.lower()}"

        command = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={setting}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={self.output}",
            self.input
        ]

        subprocess.run(command, check=True)
        print(f"Compressed PDF saved to: {self.output}")

def main():
    parser = argparse.ArgumentParser(
        description="Compress a PDF file using Ghostscript.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-i", "--input",
        help="Path to the input PDF file",
        required=False
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to the output compressed PDF file",
        required=False
    )
    parser.add_argument(
        "-c", "--compression",
        choices=["screen", "ebook", "prepress", "printer", "default"],
        default="default",
        help="Compression level: default, screen (72 dpi), ebook (150 dpi), printer (300 dpi), prepress (highest)"
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Force overwrite of output file without confirmation"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    input_path = args.input or input("Enter the path to the input PDF file: ")
    output_path = args.output or input("Enter the path to the output PDF file: ")

    if os.path.exists(output_path) and not args.force:
        confirm = input(f"Output file '{output_path}' already exists. Overwrite? [y/N]: ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return

    compression = args.compression
    compressor = PDFCompressor(input_path, output_path, compression)
    try:
        compressor.compress()
    except subprocess.CalledProcessError as e:
        print ("Command failed:" + str(e))

if __name__ == "__main__":
    main()
