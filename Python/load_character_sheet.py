
import sys
import io
import contextlib

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QFormLayout, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from pdfrw import PdfReader
except ImportError:
    PdfReader = None

class LoadCharacterSheetWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Load Character Sheet PDF')
        self.setGeometry(200, 200, 1720, 1000)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.load_btn = QPushButton('Load Character Sheet PDF')
        self.load_btn.clicked.connect(self.load_pdf)
        layout.addWidget(self.load_btn)


        self.info_label = QLabel('No file loaded.')
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)

        from PySide6.QtWidgets import QScrollArea
        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.form_widget)
        layout.addWidget(self.scroll_area)
        self.form_widget.hide()

    def load_pdf(self):
        if PdfReader is None:
            QMessageBox.critical(self, 'Error', 'pdfrw is not installed. Please run: pip install pdfrw')
            return
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Character Sheet PDF', '', 'PDF Files (*.pdf)')
        if not file_path:
            return

        # Extract field values using pdfrw
        try:
            pdf = PdfReader(file_path)
            fields = {}
            if hasattr(pdf, 'Root') and hasattr(pdf.Root, 'AcroForm') and hasattr(pdf.Root.AcroForm, 'Fields'):
                for field in pdf.Root.AcroForm.Fields:
                    key = None
                    val = ''
                    if hasattr(field, 'T') and field.T is not None:
                        key = str(field.T)
                        if key.startswith('(') and key.endswith(')'):
                            key = key[1:-1]
                    if hasattr(field, 'V') and field.V is not None:
                        val = str(field.V)
                        if val.startswith('(') and val.endswith(')'):
                            val = val[1:-1]
                    if key:
                        fields[key] = val
        except Exception as e:
            self.info_label.setText('Failed to extract PDF fields.')
            QMessageBox.critical(self, 'Error', f'Failed to extract PDF fields: {e}')
            return

        # Clear previous form
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Add fields to form as editable QLineEdit
        for key, val in fields.items():
            label = QLabel(key)
            edit = QLineEdit(val)
            self.form_layout.addRow(label, edit)

        self.form_widget.show()
        self.info_label.setText('PDF fields loaded into editable form.')

    def extract_fields(self, pdf):
        fields = {}
        if not hasattr(pdf, 'Root') or not hasattr(pdf.Root, 'AcroForm'):
            return fields
        acroform = pdf.Root.AcroForm
        if not hasattr(acroform, 'Fields'):
            return fields
        for field in acroform.Fields:
            key = None
            val = ''
            if hasattr(field, 'T') and field.T is not None:
                key = str(field.T)
                if key.startswith('(') and key.endswith(')'):
                    key = key[1:-1]
            if hasattr(field, 'V') and field.V is not None:
                val = str(field.V)
                if val.startswith('(') and val.endswith(')'):
                    val = val[1:-1]
            if key:
                fields[key] = val
        return fields

def main():
    app = QApplication(sys.argv)
    win = LoadCharacterSheetWidget()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
