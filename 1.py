from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QApplication, QPlainTextEdit
from PySide6.QtGui import QTextCursor

class PairInputTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.special_pairs = {'"': '"', "'": "'", '{': '}', '(': ')', '[': ']'}

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        if key in (Qt.Key_Backspace, Qt.Key_Delete):
            self.handleDeletion(event)
        elif text and text in self.special_pairs:
            self.insertPairedSymbol(text)
        else:
            super().keyPressEvent(event)

    def handleDeletion(self, event):
        cursor = self.textCursor()
        if event.key() == Qt.Key_Backspace:
            pos = cursor.position()
            if pos > 0:
                prev_char = self.toPlainText()[pos - 1]
                if prev_char in self.special_pairs:
                    next_char_pos = pos
                    if pos < len(self.toPlainText()) and self.toPlainText()[pos] == self.special_pairs[prev_char]:
                        next_char_pos += 1
                    cursor.setPosition(pos - 1)
                    cursor.setPosition(next_char_pos, QTextCursor.KeepAnchor)
                    cursor.removeSelectedText()
                else:
                    super().keyPressEvent(event)
        elif event.key() == Qt.Key_Delete:
            # Only delete the character to the right of the cursor without considering pairs.
            if cursor.position() < len(self.toPlainText()):
                cursor.deleteChar()
        else:
            super().keyPressEvent(event)

    def insertPairedSymbol(self, symbol):
        cursor = self.textCursor()
        cursor.insertText(symbol + self.special_pairs[symbol])
        cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

if __name__ == "__main__":
    app = QApplication([])
    text_edit = PairInputTextEdit()
    text_edit.show()
    app.exec()