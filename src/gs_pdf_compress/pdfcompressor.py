#!/usr/bin/env
#
# This file is part of PDFCompress. See LICENSE.txt.
# Copyright (c) 2025 Clem Lorteau

import subprocess
import os

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
