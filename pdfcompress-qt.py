#!/usr/bin/env python3
#
# This file is part of PDFCompress. See LICENSE.txt.
# Copyright (c) 2025 Clem Lorteau


from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QMessageBox, QFileDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
import sys
import os

from __init__ import __version__
from pdfcompress import PDFCompressor
from qhinttextcombobox import QHintTextComboBox

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About PDFCompress")
        self.setWindowIcon(QIcon(PDFCompressorUI.iconPath))
        self.setFixedSize(400, 250)

        layout = QVBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(PDFCompressorUI.iconPath).pixmap(128, 128))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text = QLabel(f"<b>PDFCompress</b> {__version__}<br>"
                      "Compress PDF files using Ghostscript<br><br>"
                      "©2025 Clem Lorteau<br><br>"
                      "<a href='https://github.com/clorteau/pdfcompress'>"
                      "github.com/clorteau/pdfcompress</a>")
        text.setOpenExternalLinks(True)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(icon_label)
        layout.addWidget(text)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setLayout(layout)

class PDFCompressorUI(QWidget):
    iconPath ="res/icon.svg"

    def __init__(self):
        super().__init__()
        uic.loadUi("res/pdfcompress-qt.ui", self)

        self.setAcceptDrops(True)
        self.setWindowIcon(QIcon(self.iconPath))

        self.browseInputButton.clicked.connect(self.browse_input)
        self.browseOutputButton.clicked.connect(self.browse_output)
        self.compressButton.clicked.connect(self.compress_pdf)
        self.aboutButton.clicked.connect(self.show_about)

        #add our custom QComboBox
        self.compressionComboBox = QHintTextComboBox()
        self.compressionComboBox.addItem("default", "")
        self.compressionComboBox.addItem("screen", "72 dpi")
        self.compressionComboBox.addItem("ebook", "150 dpi")
        self.compressionComboBox.addItem("printer", "300 dpi")
        self.compressionComboBox.addItem("prepress", "highest")
        self.formLayout.addRow("Compression level:", self.compressionComboBox)
        
    def browse_input(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Input PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.inputLineEdit.setText(file_path)

    def browse_output(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select Output PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.outputLineEdit.setText(file_path)

    def compress_pdf(self):
        input_path = self.inputLineEdit.text().strip()
        output_path = self.outputLineEdit.text().strip()
        compression = self.compressionComboBox.currentText()

        if not input_path or not output_path:
            QMessageBox.warning(self, "Missing Fields", "Please specify both input and output PDF paths.")
            return

        if not os.path.isfile(input_path):
            QMessageBox.critical(self, "Error", "Input file does not exist.")
            return

        if os.path.exists(output_path):
            reply = QMessageBox.question(self, "Overwrite File",
                                         f"The file '{output_path}' already exists. Overwrite?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                return

        try:
            compressor = PDFCompressor(input_path, output_path, compression)
            compressor.compress()
            self.statusLabel.setText("Compression successful.")
        except Exception as e:
            self.statusLabel.setText("Compression failed.")
            QMessageBox.critical(self, "Error", str(e))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            if url.toLocalFile().lower().endswith(".pdf"):
                self.inputLineEdit.setText(url.toLocalFile())
                break

    def show_about(self):
        dialog = AboutDialog()
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFCompressorUI()
    window.show()
    sys.exit(app.exec())
