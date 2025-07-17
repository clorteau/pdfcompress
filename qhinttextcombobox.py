#!/usr/bin/env python3
#
# This file is part of PDFCompress. See LICENSE.txt.
# Copyright (c) 2025 Clem Lorteau

from PyQt6.QtWidgets import QApplication, QComboBox, QStyledItemDelegate, QWidget, QVBoxLayout
from PyQt6.QtWidgets import QStyleOptionViewItem, QStyle
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QSize, QRect


class _CustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()

        # Get the texts from the model
        left_text = "  " + index.data(Qt.ItemDataRole.DisplayRole)
        right_text = index.data(Qt.ItemDataRole.UserRole) + " "

        # Define rectangles for left and right text
        rect = option.rect
        half_width = rect.width() // 2
        left_rect = QRect(rect.left(), rect.top(), half_width, rect.height())
        right_rect = QRect(rect.left() + half_width, rect.top(), half_width, rect.height())

        # Draw left text (normal)
        painter.setPen(option.palette.text().color())
        painter.drawText(left_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, left_text)

        # Draw right text (italic and semi-transparent)
        font = painter.font()
        font.setItalic(True)
        painter.setFont(font)
        color = option.palette.text().color()
        color.setAlphaF(0.5)
        painter.setPen(color)
        painter.drawText(right_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight, right_text)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(200, 30)


class QHintTextComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        delegate = _CustomDelegate()
        self.setItemDelegate(delegate)
        self.setMinimumWidth(250)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

        # Apply delegate to the line edit display
        self.setLineEditDisplayDelegate(delegate)

    def setLineEditDisplayDelegate(self, delegate):
        # Override paintEvent of line edit to use the same delegate
        class LineEditDelegate(QWidget):
            def __init__(self, combo):
                super().__init__(combo)
                self.combo = combo
                self.delegate = delegate
                self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

            def paintEvent(self, event):
                painter = QPainter(self)
                index = self.combo.model().index(self.combo.currentIndex(), 0)

                option = QStyleOptionViewItem()
                option.rect = self.rect().adjusted(0, 0, -22, 0)  # Leave space for the arrow
                option.state = QStyle.StateFlag.State_Enabled
                option.font = self.combo.font()
                option.palette = self.combo.palette()

                self.delegate.paint(painter, option, index)


        # Replace line edit with custom paint widget
        self.lineEdit().hide()
        self._custom_display = LineEditDelegate(self)
        self._custom_display.setGeometry(self.rect())
        self._custom_display.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, '_custom_display'):
            self._custom_display.setGeometry(self.rect())

    def addItem(self, left_text, right_text):
        super().addItem(left_text)
        index = self.model().index(self.count() - 1, 0)
        self.model().setData(index, right_text, Qt.ItemDataRole.UserRole)


class _ExampleMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        combo = QHintTextComboBox()
        combo.addItem("Apple", "Fruit")
        combo.addItem("Carrot", "Vegetable")
        combo.addItem("Salmon", "Fish")

        layout.addWidget(combo)
        self.setLayout(layout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = _ExampleMainWindow()
    window.show()
    sys.exit(app.exec())
