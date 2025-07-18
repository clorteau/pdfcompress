#!/usr/bin/env python3
#
# This file is part of PDFCompress. See LICENSE.txt.
# Copyright (c) 2025 Clem Lorteau

import argparse
import os

# try importing our modules from the local folder in case it's running locally
# if failed, try importing globally in case it's installed 
try:
    from __init__ import __version__
    from pdfcompressor import PDFCompressor
except ModuleNotFoundError:
    from gs_pdf_compress import __version__
    from gs_pdf_compress.pdfcompressor import PDFCompressor

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
