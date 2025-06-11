import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton,
    QFileDialog, QScrollArea, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtCore import Qt, QMimeData, QPoint, QEvent, QCoreApplication
from PIL import Image
import img2pdf
from threading import Thread


class CustomEvent(QEvent):
    def __init__(self, func):
        super().__init__(QEvent.User)
        self.func = func

    def execute(self):
        self.func()


class DraggableLabel(QWidget):
    def __init__(self, path, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.path = path
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)

        pixmap = QPixmap(path).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label = QLabel()
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        fname = os.path.basename(path)
        self.text = QLabel(fname)
        self.text.setStyleSheet("color: white; font-size: 10px;")
        self.text.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.text)

        self.setLayout(layout)
        self.setFixedSize(160, 180)
        self.setAcceptDrops(True)
        self.setStyleSheet("border: 2px solid #444; border-radius: 8px; background-color: #2d2d2d;")

        # delete button
        self.del_btn = QPushButton('❌', self)
        self.del_btn.setFixedSize(20, 20)
        self.del_btn.setStyleSheet("background: transparent; color: red; border: none;")
        self.del_btn.clicked.connect(self.delete_self)
        self.del_btn.move(self.width() - 25, 5)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            mimeData = QMimeData()
            mimeData.setText(self.path)
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setPixmap(self.label.pixmap())
            drag.setHotSpot(QPoint(self.width() // 2, self.height() // 2))
            drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        source = event.source()
        target = self
        if isinstance(source, DraggableLabel) and source != target:
            source.path, target.path = target.path, source.path
            source.update_display()
            target.update_display()

    def update_display(self):
        pixmap = QPixmap(self.path).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)
        fname = os.path.basename(self.path)
        self.text.setText(fname)

    def delete_self(self):
        if hasattr(self, 'app'):
            self.app.remove_image(self)


class ImageToPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔥 Tejas Style - Drag & Drop Images to PDF")
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Segoe UI;")
        self.resize(1100, 700)

        self.image_labels = []

        main_layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.container = QWidget()
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(10)
        self.scroll_area.setWidget(self.container)

        main_layout.addWidget(self.scroll_area)

        btn_row = QHBoxLayout()

        self.add_btn = QPushButton("➕ Add Images")
        self.add_btn.clicked.connect(self.add_images)
        self.add_btn.setStyleSheet("background-color: #ef5a3c; color: white; padding: 10px; border-radius: 5px;")
        btn_row.addWidget(self.add_btn)

        self.clear_btn = QPushButton("🧹 Clear All")
        self.clear_btn.clicked.connect(self.clear_images)
        self.clear_btn.setStyleSheet("background-color: #ef5a3c; color: white; padding: 10px; border-radius: 5px;")
        btn_row.addWidget(self.clear_btn)

        self.export_btn = QPushButton("📄 Export to PDF")
        self.export_btn.clicked.connect(self.export_pdf)
        self.export_btn.setStyleSheet("background-color: #00b894; color: white; padding: 10px; border-radius: 5px; font-size: 16px;")
        btn_row.addWidget(self.export_btn)

        main_layout.addLayout(btn_row)

        # Loading overlay
        self.overlay = QLabel(self.container)
        self.overlay.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            color: white;
            font-size: 18px;
            border-radius: 10px;
        """)
        self.overlay.setAlignment(Qt.AlignCenter)
        self.overlay.setText("🔄 Converting images to PDF...")
        self.overlay.hide()

    def add_images(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg *.webp *.bmp)")
        for path in paths:
            if path not in [lbl.path for lbl in self.image_labels]:
                label = DraggableLabel(path, self)
                self.image_labels.append(label)
        self.refresh_grid()

    def refresh_grid(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        for i, label in enumerate(self.image_labels):
            self.grid.addWidget(label, i // 5, i % 5)

    def remove_image(self, label):
        if label in self.image_labels:
            self.image_labels.remove(label)
            label.setParent(None)
            self.refresh_grid()

    def clear_images(self):
        self.image_labels = []
        self.refresh_grid()

    def export_pdf(self):
        if not self.image_labels:
            QMessageBox.warning(self, "No Images", "Please add images before exporting.")
            return

        self.save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if self.save_path:
            self.overlay.setGeometry(0, 0, self.container.width(), self.container.height())
            self.overlay.show()
            QApplication.processEvents()

            thread = Thread(target=self.convert_pdf)
            thread.start()

    def convert_pdf(self):
        try:
            img_paths = [lbl.path for lbl in self.image_labels]
            with open(self.save_path, "wb") as f:
                f.write(img2pdf.convert(img_paths))
            self.queue_event(lambda: self.show_message("Success", "PDF saved successfully!", error=False))
        except Exception as e:
            self.queue_event(lambda: self.show_message("Error", str(e), error=True))

    def queue_event(self, func):
        QCoreApplication.postEvent(self, CustomEvent(func))

    def show_message(self, title, text, error=False):
        self.overlay.hide()
        if error:
            QMessageBox.critical(self, title, text)
        else:
            QMessageBox.information(self, title, text)

    def event(self, event):
        if isinstance(event, CustomEvent):
            event.execute()
            return True
        return super().event(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageToPDFApp()
    window.show()
    sys.exit(app.exec_())
