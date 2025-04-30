from PySide6.QtWidgets import QTableView, QMenu, QApplication
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QKeyEvent, QKeySequence

class SmartTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditTriggers(QTableView.AllEditTriggers)
        self.undo_stack = []  # [(row, col, old_value)]

    def keyPressEvent(self, event: QKeyEvent):
        if event.matches(QKeySequence.Paste):
            self.paste_clipboard()
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Z:
            self.undo_last()
        else:
            super().keyPressEvent(event)

    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return

        menu = QMenu(self)
        paste_action = menu.addAction("Вставить")
        action = menu.exec(event.globalPos())

        if action == paste_action:
            self.paste_clipboard()

    def paste_clipboard(self):
        clipboard = QApplication.clipboard()
        value = clipboard.text()
        index = self.currentIndex()
        if index.isValid():
            model = self.model()
            old_value = model.data(index)
            self.undo_stack.append((index.row(), index.column(), old_value))
            model.setData(index, value)

    def undo_last(self):
        if not self.undo_stack:
            return
        model = self.model()
        row, col, old_val = self.undo_stack.pop()
        index = model.index(row, col)
        model.setData(index, old_val)
