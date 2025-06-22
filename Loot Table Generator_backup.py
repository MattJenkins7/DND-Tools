import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QTextEdit,
    QFileDialog, QMessageBox, QSpinBox, QDoubleSpinBox, QStatusBar, QAbstractItemView, QHeaderView,
    QScrollArea, QToolButton, QSizePolicy, QFrame, QListWidget, QCheckBox, QDialog
)
from PySide6.QtCore import Qt, QEvent, QTimer
from PySide6.QtGui import QKeySequence
import os
import csv
import random
import difflib
import functools
import json
import re

RARITY_VALUES = {
    'common': 50,
    'uncommon': 325,
    'rare': 1250,
    'very rare': 3000,
    'legendary': 30000,
    'artifact': 60000,
}

LEVEL_RARITY_TABLE = {
    1: {'common': 6, 'uncommon': 2, 'rare': 0, 'very rare': 0, 'legendary': 0},
    2: {'common': 8, 'uncommon': 3, 'rare': 0, 'very rare': 0, 'legendary': 0},
    3: {'common': 9, 'uncommon': 5, 'rare': 1, 'very rare': 0, 'legendary': 0},
    4: {'common': 10, 'uncommon': 8, 'rare': 1, 'very rare': 0, 'legendary': 0},
    5: {'common': 10, 'uncommon': 13, 'rare': 2, 'very rare': 1, 'legendary': 0},
    6: {'common': 10, 'uncommon': 14, 'rare': 3, 'very rare': 1, 'legendary': 0},
    7: {'common': 10, 'uncommon': 15, 'rare': 4, 'very rare': 1, 'legendary': 0},
    8: {'common': 10, 'uncommon': 16, 'rare': 5, 'very rare': 2, 'legendary': 0},
    9: {'common': 10, 'uncommon': 17, 'rare': 6, 'very rare': 2, 'legendary': 1},
    10: {'common': 8, 'uncommon': 16, 'rare': 8, 'very rare': 2, 'legendary': 1},
    11: {'common': 7, 'uncommon': 13, 'rare': 10, 'very rare': 4, 'legendary': 1},
    12: {'common': 5, 'uncommon': 10, 'rare': 11, 'very rare': 6, 'legendary': 1},
    13: {'common': 5, 'uncommon': 9, 'rare': 11, 'very rare': 6, 'legendary': 1},
    14: {'common': 4, 'uncommon': 7, 'rare': 11, 'very rare': 9, 'legendary': 1},
    15: {'common': 3, 'uncommon': 6, 'rare': 11, 'very rare': 11, 'legendary': 2},
    16: {'common': 3, 'uncommon': 5, 'rare': 11, 'very rare': 11, 'legendary': 2},
    17: {'common': 2, 'uncommon': 3, 'rare': 10, 'very rare': 12, 'legendary': 2},
    18: {'common': 0, 'uncommon': 2, 'rare': 10, 'very rare': 13, 'legendary': 3},
    19: {'common': 0, 'uncommon': 2, 'rare': 10, 'very rare': 14, 'legendary': 3},
    20: {'common': 0, 'uncommon': 2, 'rare': 10, 'very rare': 15, 'legendary': 3},
}

GEMSTONE_VALUE_LIST = {
    'AMETHYST': {'Flawless': 500, 'Brilliant': 400, 'Cut': 300, 'Raw': 200, 'Rough': 100},
    'AQUAMARINE': {'Flawless': 400, 'Brilliant': 300, 'Cut': 200, 'Raw': 100, 'Rough': 50},
    'CITRINE': {'Flawless': 300, 'Brilliant': 250, 'Cut': 200, 'Raw': 150, 'Rough': 100},
    'GARNET': {'Flawless': 200, 'Brilliant': 150, 'Cut': 100, 'Raw': 75, 'Rough': 50},
    'ONYX': {'Flawless': 300, 'Brilliant': 250, 'Cut': 200, 'Raw': 150, 'Rough': 100},
    'OPAL': {'Flawless': 400, 'Brilliant': 350, 'Cut': 300, 'Raw': 250, 'Rough': 200},
    'PEARL': {'Flawless': 500, 'Brilliant': 400, 'Cut': 300, 'Raw': 200, 'Rough': 100},
    'RUBY': {'Flawless': 700, 'Brilliant': 600, 'Cut': 500, 'Raw': 400, 'Rough': 300},
    'SAPPHIRE': {'Flawless': 800, 'Brilliant': 700, 'Cut': 600, 'Raw': 500, 'Rough': 400},
    'TOPAZ': {'Flawless': 100, 'Brilliant': 75, 'Cut': 50, 'Raw': 20, 'Rough': 5},
    'TOURMALINE': {'Flawless': 500, 'Brilliant': 400, 'Cut': 300, 'Raw': 200, 'Rough': 100},
    'DIAMOND': {'Flawless': 1000, 'Brilliant': 800, 'Cut': 700, 'Raw': 500, 'Rough': 300},
    'EMERALD': {'Flawless': 500, 'Brilliant': 400, 'Cut': 300, 'Raw': 200, 'Rough': 100},
    'JADE': {'Flawless': 400, 'Brilliant': 350, 'Cut': 300, 'Raw': 250, 'Rough': 200},
    'JASPER': {'Flawless': 300, 'Brilliant': 250, 'Cut': 200, 'Raw': 150, 'Rough': 100},
    'PERIDOT': {'Flawless': 300, 'Brilliant': 250, 'Cut': 200, 'Raw': 150, 'Rough': 100},
    'SPINEL': {'Flawless': 600, 'Brilliant': 500, 'Cut': 400, 'Raw': 300, 'Rough': 200},
    'ZIRCON': {'Flawless': 500, 'Brilliant': 400, 'Cut': 300, 'Raw': 200, 'Rough': 100},
    'AMBER': {'Flawless': 300, 'Brilliant': 250, 'Cut': 200, 'Raw': 150, 'Rough': 100},
    'MOONSTONE': {'Flawless': 400, 'Brilliant': 350, 'Cut': 300, 'Raw': 250, 'Rough': 200},
    'TURQUOISE': {'Flawless': 200, 'Brilliant': 150, 'Cut': 100, 'Raw': 75, 'Rough': 50},
}

RARITY_LIST = ['common', 'uncommon', 'rare', 'very rare', 'legendary', 'artifact']

def get_rarity(row, header=None):
    idx = 3
    if header:
        for i, col in enumerate(header):
            if col.strip().lower() == 'rarity':
                idx = i
                break
    rarity = row[idx].strip().lower()
    if rarity in RARITY_LIST:
        return rarity
    for r in RARITY_LIST:
        if r in rarity:
            return r
    return 'unknown'

def filter_items_by_rarity(items, rarity):
    return [item for item in items if get_rarity(item) == rarity]

def get_random_rarity_distribution(level):
    rarity_caps = LEVEL_RARITY_TABLE.get(level, LEVEL_RARITY_TABLE[1])
    rarity_dist = {}
    for rarity, cap in rarity_caps.items():
        if cap > 0:
            rarity_dist[rarity] = random.randint(0, cap)
        else:
            rarity_dist[rarity] = 0
    return rarity_dist

def select_items_by_level(items, level):
    rarity_counts = get_random_rarity_distribution(level)
    selected = []
    for rarity, count in rarity_counts.items():
        pool = filter_items_by_rarity(items, rarity)
        if pool and count > 0:
            selected.extend(random.sample(pool, min(count, len(pool))))
    return selected

def get_item_value(rarity):
    ranges = {
        'common': (40, 60),
        'uncommon': (150, 500),
        'rare': (500, 2000),
        'very rare': (1000, 5000),
        'legendary': (10000, 50000),
        'artifact': (50000, 70000),
    }
    low, high = ranges.get(rarity, (0, 0))
    return random.randint(low, high)

def write_csv_shop(header, data, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

def write_csv_loot(header, data, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

def run_generation(mode, method, out_name, max_items, level=None, value=None):
    csv_path = 'magic items.csv'
    output_dir = os.path.join(os.path.dirname(__file__), 'Generated Loot Tables')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    out_path = os.path.join(output_dir, f'{out_name}.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        if not rows:
            raise Exception('No data found.')
        header = rows[0]
        data = rows[1:]
    # Find column indices by header
    name_idx = None
    rarity_idx = None
    type_idx = None
    attune_idx = None
    text_idx = None
    for i, col in enumerate(header):
        col_l = col.strip().lower()
        if col_l == 'name':
            name_idx = i
        elif col_l == 'rarity':
            rarity_idx = i
        elif col_l == 'type':
            type_idx = i
        elif col_l == 'attunement':
            attune_idx = i
        elif col_l == 'text':
            text_idx = i
    if None in [name_idx, rarity_idx, type_idx, attune_idx, text_idx]:
        raise Exception('CSV missing required columns.')
    if method == 'level':
        selected = select_items_by_level(data, level)
    elif method == 'value':
        selected = select_items_by_value(data, value)
    else:
        raise Exception('Invalid method.')
    if len(selected) > max_items:
        selected = random.sample(selected, max_items)
    if mode == 'Shop':
        shop_header = ['Name', 'Rarity', 'Type', 'Value', 'Attunement', 'Text']
        shop_data = []
        for row in selected:
            name = row[name_idx] if name_idx < len(row) else ''
            rarity = row[rarity_idx].strip().lower() if rarity_idx < len(row) else 'unknown'
            typ = row[type_idx] if type_idx < len(row) and row[type_idx].strip() else 'Unknown'
            value = get_item_value(rarity)
            attunement = row[attune_idx] if attune_idx < len(row) else ''
            text = row[text_idx] if text_idx < len(row) else ''
            shop_data.append([name, rarity, typ, value, attunement, text])
        write_csv_shop(shop_header, shop_data, out_path)
        return f'Shop inventory saved to {out_path}'
    elif mode == 'Loot':
        loot_header = ['Name', 'Rarity', 'Type', 'Attunement', 'Text']
        loot_data = []
        for row in selected:
            name = row[name_idx] if name_idx < len(row) else ''
            rarity = row[rarity_idx].strip().lower() if rarity_idx < len(row) else 'unknown'
            typ = row[type_idx] if type_idx < len(row) and row[type_idx].strip() else 'Unknown'
            attunement = row[attune_idx] if attune_idx < len(row) else ''
            text = row[text_idx] if text_idx < len(row) else ''
            loot_data.append([name, rarity, typ, attunement, text])
        write_csv_loot(loot_header, loot_data, out_path)
        return f'Loot table saved to {out_path}'
    else:
        raise Exception('Invalid mode.')

def select_items_by_value(items, total_value):
    selected = []
    pool = items[:]
    random.shuffle(pool)
    current_value = 0
    while pool and current_value < total_value:
        item = pool.pop()
        rarity = get_rarity(item)
        value = get_item_value(rarity)
        if current_value + value <= total_value:
            selected.append(item)
            current_value += value
        elif not selected:
            selected.append(item)
            break
    return selected

class MagicItemGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Magic Item Generator')
        self.resize(1000, 700)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.csv_data = {'header': [], 'rows': [], 'file_path': None}
        self.init_generator_tab()
        self.init_viewer_tab()
        self.init_character_creator_tab()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def init_generator_tab(self):
        gen_tab = QWidget()
        gen_layout = QGridLayout()
        gen_tab.setLayout(gen_layout)
        self.tabs.addTab(gen_tab, 'Generator')
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['Shop', 'Loot'])
        gen_layout.addWidget(QLabel('Mode:'), 0, 0)
        gen_layout.addWidget(self.mode_combo, 0, 1)
        self.method_combo = QComboBox()
        self.method_combo.addItems(['By character level', 'By total gold value'])
        gen_layout.addWidget(QLabel('Loot Generation Method:'), 1, 0)
        gen_layout.addWidget(self.method_combo, 1, 1)
        self.out_name_edit = QLineEdit()
        gen_layout.addWidget(QLabel('Output file name (no .csv):'), 2, 0)
        gen_layout.addWidget(self.out_name_edit, 2, 1)
        self.max_items_spin = QSpinBox()
        self.max_items_spin.setRange(1, 1000)
        self.max_items_spin.setValue(10)
        gen_layout.addWidget(QLabel('Max items:'), 3, 0)
        gen_layout.addWidget(self.max_items_spin, 3, 1)
        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 20)
        self.level_spin.setValue(1)
        gen_layout.addWidget(QLabel('Character level (1-20):'), 4, 0)
        gen_layout.addWidget(self.level_spin, 4, 1)
        self.value_spin = QSpinBox()
        self.value_spin.setRange(1, 1000000)
        self.value_spin.setValue(1000)
        gen_layout.addWidget(QLabel('Total gold value (GP):'), 5, 0)
        gen_layout.addWidget(self.value_spin, 5, 1)
        self.method_combo.currentIndexChanged.connect(self.update_fields)
        self.update_fields()
        generate_btn = QPushButton('Generate')
        generate_btn.clicked.connect(self.on_generate)
        gen_layout.addWidget(generate_btn, 6, 0, 1, 2)

    def update_fields(self):
        if self.method_combo.currentIndex() == 0:
            self.level_spin.setEnabled(True)
            self.value_spin.setEnabled(False)
        else:
            self.level_spin.setEnabled(False)
            self.value_spin.setEnabled(True)

    def on_generate(self):
        mode = self.mode_combo.currentText()
        method = 'level' if self.method_combo.currentIndex() == 0 else 'value'
        out_name = self.out_name_edit.text().strip()
        max_items = self.max_items_spin.value()
        level = self.level_spin.value()
        value = self.value_spin.value()
        if not out_name or not max_items or (method == 'level' and not level) or (method == 'value' and not value):
            QMessageBox.critical(self, 'Error', 'Please fill in all required fields.')
            return
        try:
            if method == 'level':
                msg = run_generation(mode, method, out_name, max_items, level=level)
            else:
                msg = run_generation(mode, method, out_name, max_items, value=value)
            QMessageBox.information(self, 'Success', msg)
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def init_viewer_tab(self):
        viewer_tab = QWidget()
        viewer_layout = QVBoxLayout()
        viewer_tab.setLayout(viewer_layout)
        self.tabs.addTab(viewer_tab, 'CSV Viewer')

        # --- Top bar: Open, Save, Delete, Dark Mode ---
        top_bar = QHBoxLayout()
        open_btn = QPushButton('Open CSV File')
        open_btn.clicked.connect(self.load_csv)
        save_btn = QPushButton('Save CSV')
        save_btn.clicked.connect(self.save_csv)
        del_btn = QPushButton('Delete Selected Item(s)')
        del_btn.clicked.connect(self.delete_selected)
        dark_btn = QPushButton('Toggle Dark Mode')
        dark_btn.setCheckable(True)
        dark_btn.toggled.connect(self.toggle_dark_mode)
        top_bar.addWidget(open_btn)
        top_bar.addWidget(save_btn)
        top_bar.addWidget(del_btn)
        top_bar.addWidget(dark_btn)
        top_bar.addStretch()
        viewer_layout.addLayout(top_bar)

        # --- Search/filter bar ---
        filter_bar = QHBoxLayout()
        filter_label = QLabel('Search:')
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText('Type to filter...')
        self.filter_edit.textChanged.connect(self.update_table)
        clear_filter_btn = QPushButton('Clear')
        clear_filter_btn.clicked.connect(lambda: self.filter_edit.setText(''))
        filter_bar.addWidget(filter_label)
        filter_bar.addWidget(self.filter_edit)
        filter_bar.addWidget(clear_filter_btn)
        filter_bar.addStretch()
        viewer_layout.addLayout(filter_bar)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.itemSelectionChanged.connect(self.update_preview)
        self.table.itemChanged.connect(self.on_table_item_changed)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet('QTableWidget { font-size: 13pt; font-family: Segoe UI, Arial, sans-serif; } QHeaderView::section { padding: 8px; font-weight: bold; } QTableWidget::item { padding: 6px; }')
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        viewer_layout.addWidget(self.table)

        # --- Add Potions/Gemstones ---
        add_pg_bar = QHBoxLayout()
        add_pg_bar.addWidget(QLabel('Add Potions/Gemstones:'))
        add_pg_bar.addWidget(QLabel('Number of Potions:'))
        self.num_potions_spin = QSpinBox()
        self.num_potions_spin.setRange(1, 100)
        self.num_potions_spin.setValue(1)
        add_pg_bar.addWidget(self.num_potions_spin)
        add_potion_btn = QPushButton('Add Potions')
        add_potion_btn.clicked.connect(self.add_potions)
        add_pg_bar.addWidget(add_potion_btn)
        add_pg_bar.addWidget(QLabel('Gemstone Value:'))
        self.gem_value_spin = QSpinBox()
        self.gem_value_spin.setRange(1, 100000)
        self.gem_value_spin.setValue(100)
        add_pg_bar.addWidget(self.gem_value_spin)
        add_gem_btn = QPushButton('Add Gemstones')
        add_gem_btn.clicked.connect(self.add_gemstones)
        add_pg_bar.addWidget(add_gem_btn)
        add_pg_bar.addStretch()
        viewer_layout.addLayout(add_pg_bar)

        # --- Add Item by Rarity/Name ---
        add_item_bar = QHBoxLayout()
        add_item_bar.addWidget(QLabel('Add Item by Rarity/Name:'))
        self.additem_rarity_combo = QComboBox()
        self.additem_rarity_combo.addItems([r.title() for r in RARITY_LIST])
        add_item_bar.addWidget(self.additem_rarity_combo)
        add_item_bar.addWidget(QLabel('(optional) Name:'))
        self.additem_name_edit = QLineEdit()
        add_item_bar.addWidget(self.additem_name_edit)
        additem_btn = QPushButton('Add Item')
        additem_btn.clicked.connect(self.add_item_by_rarity)
        add_item_bar.addWidget(additem_btn)
        add_item_bar.addStretch()
        viewer_layout.addLayout(add_item_bar)

        # --- Add Custom Item ---
        add_custom_bar = QGridLayout()
        add_custom_bar.addWidget(QLabel('Add Custom Item:'), 0, 0)
        add_custom_bar.addWidget(QLabel('Name:'), 0, 1)
        self.custom_name_edit = QLineEdit()
        add_custom_bar.addWidget(self.custom_name_edit, 0, 2)
        add_custom_bar.addWidget(QLabel('Type:'), 0, 3)
        self.custom_type_edit = QLineEdit()
        add_custom_bar.addWidget(self.custom_type_edit, 0, 4)
        add_custom_bar.addWidget(QLabel('Rarity:'), 0, 5)
        self.custom_rarity_combo = QComboBox()
        self.custom_rarity_combo.addItems([r.title() for r in RARITY_LIST])
        add_custom_bar.addWidget(self.custom_rarity_combo, 0, 6)
        add_custom_bar.addWidget(QLabel('Text:'), 1, 1)
        self.custom_text_edit = QLineEdit()
        add_custom_bar.addWidget(self.custom_text_edit, 1, 2, 1, 3)
        add_custom_bar.addWidget(QLabel('Value:'), 1, 5)
        self.custom_value_edit = QLineEdit()
        add_custom_bar.addWidget(self.custom_value_edit, 1, 6)
        addcustom_btn = QPushButton('Add Custom Item')
        addcustom_btn.clicked.connect(self.add_custom_item)
        add_custom_bar.addWidget(addcustom_btn, 0, 7, 2, 1)
        viewer_layout.addLayout(add_custom_bar)

        # --- Text Preview ---
        self.preview_label = QLabel('Text Preview:')
        self.preview_label.setStyleSheet('font-weight: bold; font-size: 12pt; margin-top: 8px;')
        viewer_layout.addWidget(self.preview_label)
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setStyleSheet('font-size: 12pt; font-family: Segoe UI, Arial, sans-serif; background: #f8f8f8; padding: 8px;')
        viewer_layout.addWidget(self.preview_text)

        # --- Keyboard shortcuts ---
        self.table.installEventFilter(self)
        self.shortcut_actions = {
            (Qt.ControlModifier, Qt.Key_S): self.save_csv,
            (Qt.NoModifier, Qt.Key_Delete): self.delete_selected,
            (Qt.ControlModifier, Qt.Key_F): lambda: self.filter_edit.setFocus(),
        }

    def eventFilter(self, obj, event):
        if obj is self.table and event.type() == QEvent.KeyPress:
            key = event.key()
            mods = event.modifiers()
            for (mod, k), action in self.shortcut_actions.items():
                if mods == mod and key == k:
                    action()
                    return True
        return super().eventFilter(obj, event)

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv)')
        if not file_path:
            return
        try:
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if not rows:
                    QMessageBox.critical(self, 'Error', 'CSV file is empty.')
                    return
                header = rows[0]
                data = rows[1:]
            self.csv_data['header'] = header
            self.csv_data['rows'] = data
            self.csv_data['file_path'] = file_path
            self.update_table()
            self.status_bar.showMessage(f"Loaded {file_path} ({len(data)} items)")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load CSV: {e}')
            self.status_bar.showMessage('Failed to load CSV.')

    def save_csv(self):
        if not self.csv_data['file_path'] or not self.csv_data['header']:
            QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
            return
        try:
            with open(self.csv_data['file_path'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.csv_data['header'])
                for row in self.csv_data['rows']:
                    writer.writerow(row)
            self.status_bar.showMessage('CSV saved.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save CSV: {e}')
            self.status_bar.showMessage('Failed to save CSV.')

    def update_table(self):
        header = self.csv_data.get('header', [])
        rows = self.csv_data.get('rows', [])
        query = self.filter_edit.text().strip().lower()
        if query:
            filtered = [row for row in rows if any(query in str(cell).lower() for cell in row)]
        else:
            filtered = rows
        self.filtered_rows = filtered
        self.table.blockSignals(True)
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        self.table.setRowCount(len(filtered))
        for i, row in enumerate(filtered):
            for j, val in enumerate(row):
                item = QTableWidgetItem(val)
                self.table.setItem(i, j, item)
        self.table.blockSignals(False)
        self.status_bar.showMessage(f"{len(filtered)} / {len(rows)} items shown.")
        self.update_preview()

    def update_preview(self):
        selected = self.table.selectedItems()
        if not selected or not self.filtered_rows:
            self.preview_text.setPlainText('')
            return
        row_idx = selected[0].row()
        row = self.filtered_rows[row_idx]
        text_idx = None
        for i, col in enumerate(self.csv_data['header']):
            if col.strip().lower() == 'text':
                text_idx = i
                break
        if text_idx is not None and row[text_idx]:
            self.preview_text.setPlainText(row[text_idx])
        else:
            self.preview_text.setPlainText('')

    def on_table_item_changed(self, item):
        # Update the underlying data when a cell is edited
        row_idx = item.row()
        col_idx = item.column()
        if 0 <= row_idx < len(self.filtered_rows):
            # Find the actual row in self.csv_data['rows']
            actual_row = self.filtered_rows[row_idx]
            actual_idx = self.csv_data['rows'].index(actual_row)
            self.csv_data['rows'][actual_idx][col_idx] = item.text()
            self.status_bar.showMessage('Cell updated.')

    def delete_selected(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return
        idxs = sorted([s.row() for s in selected], reverse=True)
        count = 0
        for idx in idxs:
            if 0 <= idx < len(self.filtered_rows):
                actual_row = self.filtered_rows[idx]
                if actual_row in self.csv_data['rows']:
                    self.csv_data['rows'].remove(actual_row)
                    count += 1
        self.update_table()
        self.status_bar.showMessage(f"Deleted {count} item(s).")

    def add_potions(self):
        if not self.csv_data['header']:
            QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
            return
        n = self.num_potions_spin.value()
        try:
            with open('magic items.csv', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                magic_header = next(reader)
                magic_data = list(reader)
        except Exception:
            QMessageBox.critical(self, 'Error', 'Could not load magic items.csv.')
            return
        # Find column indices by header
        def col_idx(col_name):
            for i, col in enumerate(magic_header):
                if col.strip().lower() == col_name:
                    return i
            return None
        type_idx = col_idx('type') or 4
        rarity_idx = col_idx('rarity') or 3
        name_idx = col_idx('name') or 0
        attune_idx = col_idx('attunement') or 5
        text_idx = col_idx('text') or 11
        potions = [row for row in magic_data if type_idx < len(row) and 'potion' in row[type_idx].lower() and rarity_idx < len(row) and row[rarity_idx].strip().lower() in ['common', 'uncommon']]
        if not potions:
            QMessageBox.warning(self, 'Warning', 'No potions found in magic items.csv.')
            return
        chosen = random.sample(potions, min(n, len(potions)))
        for row in chosen:
            new_row = []
            rarity_val = row[rarity_idx].strip().lower() if rarity_idx < len(row) else ''
            for col in self.csv_data['header']:
                col_l = col.strip().lower()
                if col_l == 'name':
                    new_row.append(row[name_idx] if name_idx < len(row) else '')
                elif col_l == 'rarity':
                    new_row.append(row[rarity_idx] if rarity_idx < len(row) else '')
                elif col_l == 'type':
                    new_row.append(row[type_idx] if type_idx < len(row) and row[type_idx].strip() else 'Unknown')
                elif col_l == 'text':
                    new_row.append(row[text_idx] if text_idx < len(row) else '')
                elif col_l == 'value':
                    new_row.append(str(get_item_value(rarity_val)))
                elif col_l == 'attunement':
                    new_row.append(row[attune_idx] if attune_idx < len(row) else '')
                else:
                    new_row.append('')
            self.csv_data['rows'].append(new_row)
        self.update_table()
        self.status_bar.showMessage(f'Added {len(chosen)} potion(s).')

    def add_gemstones(self):
        if not self.csv_data['header']:
            QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
            return
        target_value = self.gem_value_spin.value()
        min_total = int(target_value * 0.9)
        max_total = int(target_value * 1.1)
        total = 0
        gems = []
        tries = 0
        import random
        while total < min_total and tries < 1000:
            gem = random.choice(list(GEMSTONE_VALUE_LIST.keys()))
            quality = random.choice(list(GEMSTONE_VALUE_LIST[gem].keys()))
            value = GEMSTONE_VALUE_LIST[gem][quality]
            if total + value > max_total:
                tries += 1
                continue
            gems.append((gem, quality, value))
            total += value
            tries += 1
        if not gems:
            QMessageBox.warning(self, 'Warning', 'Could not generate gemstones for value.')
            return
        for gem, quality, value in gems:
            row = ['Gemstone', quality, gem, str(value), '', f'{quality} {gem} ({value} gp)']
            # Pad to match header
            while len(row) < len(self.csv_data['header']):
                row.append('')
            self.csv_data['rows'].append(row)
        self.update_table()
        self.status_bar.showMessage(f'Added {len(gems)} gemstone(s) totaling {total} gp.')

    def fuzzy_match(self, query, candidates):
        matches = [c for c in candidates if query.lower() in c.lower()]
        if matches:
            return matches[0]
        try:
            import difflib
            close = difflib.get_close_matches(query, candidates, n=1)
            return close[0] if close else None
        except ImportError:
            return None

    def add_item_by_rarity(self):
        if not self.csv_data['header']:
            QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
            return
        rarity = self.additem_rarity_combo.currentText().strip().lower()
        name_query = self.additem_name_edit.text().strip()
        try:
            with open('magic items.csv', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                magic_header = next(reader)
                magic_data = list(reader)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Could not load magic items.csv: {e}')
            return
        # Find column indices by header
        def col_idx(col_name):
            for i, col in enumerate(magic_header):
                if col.strip().lower() == col_name:
                    return i
            return None
        name_idx = col_idx('name') or 0
        rarity_idx = col_idx('rarity') or 3
        type_idx = col_idx('type') or 4
        attune_idx = col_idx('attunement') or 5
        text_idx = col_idx('text') or 11
        pool = [row for row in magic_data if rarity_idx < len(row) and get_rarity(row, magic_header) == rarity]
        if not pool:
            QMessageBox.warning(self, 'Warning', f'No items of rarity {rarity.title()} found.')
            return
        if name_query:
            names = [row[name_idx] for row in pool if name_idx < len(row)]
            match = self.fuzzy_match(name_query, names)
            if match:
                row = next(row for row in pool if name_idx < len(row) and row[name_idx] == match)
            else:
                QMessageBox.warning(self, 'Warning', f'No item found matching "{name_query}".')
                return
        else:
            row = random.choice(pool)
        new_row = []
        rarity_val = row[rarity_idx].strip().lower() if rarity_idx < len(row) else ''
        for col in self.csv_data['header']:
            col_l = col.strip().lower()
            if col_l == 'name':
                new_row.append(row[name_idx] if name_idx < len(row) else '')
            elif col_l == 'rarity':
                new_row.append(row[rarity_idx] if rarity_idx < len(row) else '')
            elif col_l == 'type':
                new_row.append(row[type_idx] if type_idx < len(row) and row[type_idx].strip() else 'Unknown')
            elif col_l == 'text':
                new_row.append(row[text_idx] if text_idx < len(row) else '')
            elif col_l == 'value':
                new_row.append(str(get_item_value(rarity_val)))
            elif col_l == 'attunement':
                new_row.append(row[attune_idx] if attune_idx < len(row) else '')
            else:
                new_row.append('')
        self.csv_data['rows'].append(new_row)
        self.update_table()
        self.status_bar.showMessage(f'Added item: {new_row[0]} ({rarity.title()})')

    def add_custom_item(self):
        if not self.csv_data['header']:
            QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
            return
        name = self.custom_name_edit.text().strip()
        typ = self.custom_type_edit.text().strip()
        rarity = self.custom_rarity_combo.currentText().strip().lower()
        text = self.custom_text_edit.text().strip()
        value = self.custom_value_edit.text().strip()
        if not name or not typ or not rarity:
            QMessageBox.warning(self, 'Warning', 'Name, Type, and Rarity are required.')
            return
        row = []
        for col in self.csv_data['header']:
            if col.strip().lower() == 'name':
                row.append(name)
            elif col.strip().lower() == 'type':
                row.append(typ)
            elif col.strip().lower() == 'rarity':
                row.append(rarity)
            elif col.strip().lower() == 'text':
                row.append(text)
            elif col.strip().lower() == 'value':
                row.append(value)
            else:
                row.append('')
        self.csv_data['rows'].append(row)
        self.update_table()
        self.status_bar.showMessage(f'Added custom item: {name} ({rarity.title()})')

    def keyPressEvent(self, event):
        # Keyboard shortcuts: Ctrl+S (save), Delete (delete), Ctrl+F (focus filter)
        if event.matches(QKeySequence.Save):
            self.save_csv()
            event.accept()
        elif event.key() == Qt.Key_Delete:
            self.delete_selected()
            event.accept()
        elif event.matches(QKeySequence.Find):
            self.filter_edit.setFocus()
            event.accept()
        else:
            super().keyPressEvent(event)

    def toggle_dark_mode(self, enabled):
        if enabled:
            dark_stylesheet = """
                QWidget { background: #232629; color: #e0e0e0; }
                QTableWidget { background: #2b2b2b; color: #e0e0e0; alternate-background-color: #232629; }
                QHeaderView::section { background: #232629; color: #e0e0e0; }
                QLineEdit, QTextEdit { background: #232629; color: #e0e0e0; border: 1px solid #444; }
                QPushButton { background: #353535; color: #e0e0e0; border: 1px solid #444; padding: 6px; }
                QPushButton:checked { background: #444; }
                QComboBox, QSpinBox { background: #232629; color: #e0e0e0; border: 1px solid #444; }
                QStatusBar { background: #232629; color: #e0e0e0; }
            """
            self.setStyleSheet(dark_stylesheet)
        else:
            self.setStyleSheet("")

    def make_collapsible_section(self, title, content_widget):
        # Returns a QWidget with a toggle button and collapsible content
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        toggle = QToolButton()
        toggle.setText(title)
        toggle.setCheckable(True)
        toggle.setChecked(False)
        toggle.setStyleSheet('QToolButton { font-weight: bold; font-size: 12pt; text-align: left; }')
        toggle.setToolButtonStyle(Qt.ToolButtonTextOnly)
        toggle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        frame = QFrame()
        frame.setFrameShape(QFrame.NoFrame)
        frame.setLayout(QVBoxLayout())
        frame.layout().addWidget(content_widget)
        frame.setVisible(False)
        def on_toggle(checked):
            frame.setVisible(checked)
        toggle.toggled.connect(on_toggle)
        layout.addWidget(toggle)
        layout.addWidget(frame)
        return container

    def init_character_creator_tab(self):
        char_tab = QWidget()
        char_layout = QVBoxLayout()
        char_tab.setLayout(char_layout)

        # Initialize required attributes
        self.required_race_skills = 0
        self.allowed_race_skills = []
        self.required_class_skills = 0
        self.allowed_class_skills = []

        # --- Race Dropdown ---
        race_bar = QHBoxLayout()
        race_label = QLabel('Race:')
        self.race_combo = QComboBox()
        # Load races from races.csv and store full data for info display
        self.race_data = []
        races = []
        try:
            with open('races.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row['name'].strip()
                    if name:
                        races.append(name)
                        self.race_data.append(row)
        except Exception:
            pass
        unique_races = sorted(set(races))
        self.race_combo.addItems(unique_races)
        race_bar.addWidget(race_label)
        race_bar.addWidget(self.race_combo)
        race_bar.addStretch()
        char_layout.addLayout(race_bar)

        # --- Race Info Display ---
        self.race_info_label = QLabel()
        self.race_info_label.setWordWrap(True)
        self.race_info_label.setStyleSheet('font-size: 11pt; background: #f8f8f8; padding: 8px; border: 1px solid #ccc;')
        race_scroll = QScrollArea()
        race_scroll.setWidgetResizable(True)
        race_scroll.setMinimumHeight(60)
        race_scroll.setMaximumHeight(200)
        race_scroll.setWidget(self.race_info_label)
        race_info_section = self.make_collapsible_section('Show Race Details', race_scroll)
        char_layout.addWidget(race_info_section)

        self.race_combo.currentTextChanged.connect(self.update_race_info)
        self.update_race_info(self.race_combo.currentText())

        # --- Background Dropdown ---
        bg_bar = QHBoxLayout()
        bg_label = QLabel('Background:')
        self.bg_combo = QComboBox()
        self.background_data = []
        backgrounds = []
        try:
            with open('backgrounds.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row['name'].strip()
                    if name:
                        backgrounds.append(name)
                        self.background_data.append(row)
        except Exception:
            pass
        unique_bgs = sorted(set(backgrounds))
        self.bg_combo.addItems(unique_bgs)
        bg_bar.addWidget(bg_label)
        bg_bar.addWidget(self.bg_combo)
        bg_bar.addStretch()
        char_layout.addLayout(bg_bar)

        # --- Background Info Display ---
        self.bg_info_label = QLabel()
        self.bg_info_label.setWordWrap(True)
        self.bg_info_label.setStyleSheet('font-size: 11pt; background: #f8f8f8; padding: 8px; border: 1px solid #ccc;')
        bg_scroll = QScrollArea()
        bg_scroll.setWidgetResizable(True)
        bg_scroll.setMinimumHeight(60)
        bg_scroll.setMaximumHeight(200)
        bg_scroll.setWidget(self.bg_info_label)
        bg_info_section = self.make_collapsible_section('Show Background Details', bg_scroll)
        char_layout.addWidget(bg_info_section)

        self.bg_combo.currentTextChanged.connect(self.update_bg_info)
        self.update_bg_info(self.bg_combo.currentText())

        # --- Class Dropdown ---
        class_bar = QHBoxLayout()
        class_label = QLabel('Class:')
        self.class_combo = QComboBox()
        import json
        self.class_data = []
        classes = []
        try:
            with open('classes.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for entry in data.get('classes', []):
                    name = entry.get('name', '').strip()
                    if name:
                        classes.append(name)
                        self.class_data.append(entry)
        except Exception:
            pass
        unique_classes = sorted(set(classes))
        self.class_combo.addItems(unique_classes)
        class_bar.addWidget(class_label)
        class_bar.addWidget(self.class_combo)
        class_bar.addStretch()
        char_layout.addLayout(class_bar)

        # --- Class Info Display ---
        self.class_info_label = QLabel()
        self.class_info_label.setWordWrap(True)
        self.class_info_label.setStyleSheet('font-size: 12pt; background: #f8f8f8; padding: 10px; border: 2px solid #888;')
        # Put class info label in a scroll area
        class_scroll = QScrollArea()
        class_scroll.setWidgetResizable(True)
        class_scroll.setMinimumHeight(200)
        class_scroll.setMaximumHeight(500)
        class_scroll.setWidget(self.class_info_label)
        class_info_section = self.make_collapsible_section('Show Class Details', class_scroll)
        # Add class section with stretch to make it dominant
        char_layout.addWidget(class_info_section, stretch=2)

        self.class_combo.currentTextChanged.connect(self.update_class_info)
        self.update_class_info(self.class_combo.currentText())

        # --- Stat Generation Section ---
        stat_gen_bar = QHBoxLayout()
        stat_label = QLabel('Stat Generation:')
        stat_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
        stat_gen_bar.addWidget(stat_label)

        # --- Stat Section (Unified Row per Stat) ---
        stat_names = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']
        stat_grid = QGridLayout()
        stat_grid.addWidget(QLabel('<b>Stat</b>'), 0, 0)
        stat_grid.addWidget(QLabel('<b>Value</b>'), 0, 1)
        stat_grid.addWidget(QLabel('<b>Score Increases</b>'), 0, 2)
        stat_grid.addWidget(QLabel('<b>Total</b>'), 0, 3)
        self.stat_spinboxes = []
        self.stat_increase_labels = []
        self.stat_total_labels = []
        self.stat_combos = []
        for i, stat in enumerate(stat_names):
            stat_grid.addWidget(QLabel(stat), i+1, 0)
            spin = QSpinBox()
            spin.setRange(1, 20)
            spin.setValue(10)
            stat_grid.addWidget(spin, i+1, 1)
            inc_label = QLabel('0')
            inc_label.setMinimumWidth(24)
            inc_label.setAlignment(Qt.AlignLeft)
            stat_grid.addWidget(inc_label, i+1, 2)
            total_label = QLabel('10')
            total_label.setMinimumWidth(24)
            total_label.setAlignment(Qt.AlignLeft)
            stat_grid.addWidget(total_label, i+1, 3)
            self.stat_spinboxes.append(spin)
            self.stat_increase_labels.append(inc_label)
            self.stat_total_labels.append(total_label)
        stat_grid.setHorizontalSpacing(12)
        stat_grid.setVerticalSpacing(4)

        # --- ASI Source Selection (Radio Buttons) ---
        from PySide6.QtWidgets import QRadioButton, QButtonGroup
        asi_radio_bar = QHBoxLayout()
        asi_radio_bar.addWidget(QLabel('Apply Ability Score Increases from:'))
        self.asi_group = QButtonGroup()
        self.asi_race_radio = QRadioButton('Race')
        self.asi_bg_radio = QRadioButton('Background')
        self.asi_both_radio = QRadioButton('Both')
        self.asi_neither_radio = QRadioButton('Neither')
        self.asi_race_radio.setChecked(True)
        self.asi_group.addButton(self.asi_race_radio, 0)
        self.asi_group.addButton(self.asi_bg_radio, 1)
        self.asi_group.addButton(self.asi_both_radio, 2)
        self.asi_group.addButton(self.asi_neither_radio, 3)
        asi_radio_bar.addWidget(self.asi_race_radio)
        asi_radio_bar.addWidget(self.asi_bg_radio)
        asi_radio_bar.addWidget(self.asi_both_radio)
        asi_radio_bar.addWidget(self.asi_neither_radio)
        asi_radio_bar.addStretch()
        self.asi_group.buttonClicked.connect(self.update_stat_totals)
        self.asi_group.buttonClicked.connect(self.on_asi_source_changed)

        # --- Stat Generation Parameters ---
        param_bar = QHBoxLayout()
        self.lowest_stat_min_spin = QSpinBox()
        self.lowest_stat_min_spin.setRange(1, 20)
        self.lowest_stat_min_spin.setValue(7)
        param_bar.addWidget(QLabel('Lowest Stat Min:'))
        param_bar.addWidget(self.lowest_stat_min_spin)
        self.lowest_stat_max_spin = QSpinBox()
        self.lowest_stat_max_spin.setRange(1, 20)
        self.lowest_stat_max_spin.setValue(9)
        param_bar.addWidget(QLabel('Lowest Stat Max:'))
        param_bar.addWidget(self.lowest_stat_max_spin)
        self.highest_stat_min_spin = QSpinBox()
        self.highest_stat_min_spin.setRange(1, 20)
        self.highest_stat_min_spin.setValue(15)
        param_bar.addWidget(QLabel('Highest Stat Min:'))
        param_bar.addWidget(self.highest_stat_min_spin)
        self.highest_stat_max_spin = QSpinBox()
        self.highest_stat_max_spin.setRange(1, 20)
        self.highest_stat_max_spin.setValue(17)
        param_bar.addWidget(QLabel('Highest Stat Max:'))
        param_bar.addWidget(self.highest_stat_max_spin)
        self.average_min_spin = QDoubleSpinBox()
        self.average_min_spin.setRange(1, 20)
        self.average_min_spin.setDecimals(2)
        self.average_min_spin.setValue(12)
        param_bar.addWidget(QLabel('Average Min:'))
        param_bar.addWidget(self.average_min_spin)
        self.average_max_spin = QDoubleSpinBox()
        self.average_max_spin.setRange(1, 20)
        self.average_max_spin.setDecimals(2)
        self.average_max_spin.setValue(13.50)
        param_bar.addWidget(QLabel('Average Max:'))
        param_bar.addWidget(self.average_max_spin)
        param_bar.addStretch()

        # --- Generate Button ---
        stat_controls_bar = QHBoxLayout()
        gen_btn = QPushButton('Generate Stats')
        gen_btn.clicked.connect(self.generate_stats)
        stat_controls_bar.addWidget(gen_btn)
        stat_controls_bar.addStretch()

        # Add to layout
        char_layout.addLayout(race_bar)
        char_layout.addWidget(race_info_section)
        char_layout.addLayout(bg_bar)
        char_layout.addWidget(bg_info_section)
        char_layout.addLayout(class_bar)
        char_layout.addWidget(class_info_section)
        char_layout.addLayout(asi_radio_bar)
        char_layout.addLayout(stat_grid)
        char_layout.addLayout(stat_controls_bar)
        char_layout.addLayout(param_bar)        # --- Character Info Inputs (Name, Alignment, Player Name) ---
        info_bar = QHBoxLayout()
        info_bar.addWidget(QLabel('Character Name:'))
        self.char_name_edit = QLineEdit()
        info_bar.addWidget(self.char_name_edit)
        info_bar.addWidget(QLabel('Alignment:'))
        self.alignment_combo = QComboBox()
        self.alignment_combo.addItems([
            'Lawful Good', 'Neutral Good', 'Chaotic Good',
            'Lawful Neutral', 'True Neutral', 'Chaotic Neutral',
            'Lawful Evil', 'Neutral Evil', 'Chaotic Evil'
        ])
        info_bar.addWidget(self.alignment_combo)
        info_bar.addWidget(QLabel('Player Name:'))
        self.player_name_edit = QLineEdit()
        info_bar.addWidget(self.player_name_edit)
        info_bar.addStretch()
        char_layout.insertLayout(0, info_bar)
        
        # Connect stat spinboxes to update totals (no prompt)
        for spin in self.stat_spinboxes:
            spin.valueChanged.connect(self.update_stat_totals)
        # Connect ASI radio group to prompt+update
        self.asi_group.buttonClicked.disconnect()
        self.asi_group.buttonClicked.connect(self.on_asi_source_changed)        # --- Character Level and Progression Section ---
        level_section = QWidget()
        level_layout = QVBoxLayout(level_section)
        
        # Level controls
        level_controls = QHBoxLayout()
        level_controls.addWidget(QLabel('Character Level:'))
        
        # Create character level spinner (separate from generator level spinner)
        self.char_level_spin = QSpinBox()
        self.char_level_spin.setRange(1, 20)
        self.char_level_spin.setValue(1)
        level_controls.addWidget(self.char_level_spin)
        
        # Level progression controls
        level_up_btn = QPushButton('Level Up')
        level_down_btn = QPushButton('Level Down')
        level_up_btn.clicked.connect(lambda: self.char_level_spin.setValue(min(20, self.char_level_spin.value() + 1)))
        level_down_btn.clicked.connect(lambda: self.char_level_spin.setValue(max(1, self.char_level_spin.value() - 1)))
        level_controls.addWidget(level_up_btn)
        level_controls.addWidget(level_down_btn)
        
        level_controls.addStretch()
        level_layout.addLayout(level_controls)
        
        # Character stats display
        stats_grid = QGridLayout()
        stats_grid.addWidget(QLabel('<b>Level</b>'), 0, 0)
        stats_grid.addWidget(QLabel('<b>Hit Points</b>'), 0, 1)
        stats_grid.addWidget(QLabel('<b>Proficiency Bonus</b>'), 0, 2)
        stats_grid.addWidget(QLabel('<b>Hit Die</b>'), 0, 3)
        
        self.level_display = QLabel('1')
        self.hit_points_display = QLabel('--')
        self.proficiency_display = QLabel('+2')
        self.hit_die_display = QLabel('--')
        
        stats_grid.addWidget(self.level_display, 1, 0)
        stats_grid.addWidget(self.hit_points_display, 1, 1)
        stats_grid.addWidget(self.proficiency_display, 1, 2)
        stats_grid.addWidget(self.hit_die_display, 1, 3)
        
        level_layout.addLayout(stats_grid)
        
        # Class Features Section
        self.class_features_widget = QWidget()
        self.class_features_layout = QVBoxLayout(self.class_features_widget)
        
        self.class_features_label = QLabel('Class Features:')
        self.class_features_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
        self.class_features_layout.addWidget(self.class_features_label)
        
        # Scrollable area for class features
        self.features_scroll = QScrollArea()
        self.features_scroll.setWidgetResizable(True)
        self.features_scroll.setMinimumHeight(150)
        self.features_scroll.setMaximumHeight(300)
        
        self.features_content = QLabel()
        self.features_content.setWordWrap(True)
        self.features_content.setStyleSheet('font-size: 11pt; background: #f8f8f8; padding: 8px; border: 1px solid #ccc;')
        self.features_content.setAlignment(Qt.AlignTop)
        self.features_scroll.setWidget(self.features_content)
        
        self.class_features_layout.addWidget(self.features_scroll)
        level_layout.addWidget(self.class_features_widget)
        
        # Spell Slot Progression for Casters
        self.spell_slots_widget = QWidget()
        self.spell_slots_layout = QVBoxLayout(self.spell_slots_widget)
        
        self.spell_slots_label = QLabel('Spell Slots:')
        self.spell_slots_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
        self.spell_slots_layout.addWidget(self.spell_slots_label)
        
        # Create grid for spell slot display
        self.spell_slots_grid = QGridLayout()
        self.spell_slots_layout.addLayout(self.spell_slots_grid)
        level_layout.addWidget(self.spell_slots_widget)
        
        # Ability Score Improvements tracking
        self.asi_widget = QWidget()
        self.asi_layout = QVBoxLayout(self.asi_widget)
        
        self.asi_label = QLabel('Ability Score Improvements Available:')
        self.asi_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
        self.asi_layout.addWidget(self.asi_label)
        
        self.asi_display = QLabel('Next ASI at level 4')
        self.asi_display.setStyleSheet('font-size: 11pt; padding: 4px;')
        self.asi_layout.addWidget(self.asi_display)
        level_layout.addWidget(self.asi_widget)
        
        # Make the whole level section collapsible
        level_collapsible = self.make_collapsible_section('Character Level & Progression', level_section)
        char_layout.addWidget(level_collapsible)
        
        # Connect level changes to update displays
        self.char_level_spin.valueChanged.connect(self.update_level_displays)
        self.class_combo.currentTextChanged.connect(self.update_level_displays)
        
        # Initialize displays
        QTimer.singleShot(100, self.update_level_displays)

    def update_level_displays(self):
        """Update the level progression displays"""
        level = self.char_level_spin.value()
        class_name = self.class_combo.currentText()
        
        # Update level, hit points, proficiency bonus, and hit die displays
        self.level_display.setText(str(level))
        
        # Calculate proficiency bonus based on character level
        proficiency_bonus = 2  # Level 1-4
        if level >= 5:
            proficiency_bonus = 3  # Level 5-8
        if level >= 9:
            proficiency_bonus = 4  # Level 9-12
        if level >= 13:
            proficiency_bonus = 5  # Level 13-16
        if level >= 17:
            proficiency_bonus = 6  # Level 17-20
        self.proficiency_display.setText(f'+{proficiency_bonus}')
        
        # Get hit die for the class
        hit_die = '--'
        for entry in self.class_data:
            if entry.get('name', '').strip() == class_name:
                hit_die = entry.get('hit_die', '--')
                break
        self.hit_die_display.setText(hit_die)
        
        # Calculate hit points
        hp_max = 0
        if hit_die != '--':
            # Roll for HP: max at 1st level + roll for each additional level
            import random
            first_level_hp = int(hit_die.split('d')[1]) + mods['CON']
            hp_max = first_level_hp
            
            if level > 1:
                rolled_hp = []
                for i in range(level - 1):
                    roll = random.randint(1, int(hit_die.split('d')[1]))
                    rolled_hp.append(roll)
                    hp_max += roll + mods['CON']
                
                # Show the user what was rolled
                rolls_text = ', '.join(map(str, rolled_hp))
                QMessageBox.information(self, 'HP Rolls', 
                    f'Rolled {rolls_text} for levels 2-{level}\n'
                    f'Total HP: {hp_max} (includes CON modifier)')
        
        self.hit_points_display.setText(str(hp_max))
        
        # Update class features based on level
        features = ''
        for entry in self.class_data:
            if entry.get('name', '').strip() == class_name:
                # Get features for the current level
                level_features = entry.get('features', {}).get(str(level), [])
                if level_features:
                    features += f"Level {level} Features:\n"
                    for feature in level_features:
                        features += f"- {feature.get('name', '')}\n"
                break
        self.features_content.setText(features.strip())
        
        # Update spell slots display
        self.update_spell_slots_display(class_name, level)

    def update_spell_slots_display(self, class_name, level):
        """Update the spell slots display based on class and level"""
        caster_type = self.get_caster_type(class_name)
        spell_slots = self.get_spell_slots(caster_type, level)
        
        # Clear existing spell slot rows
        for i in range(self.spell_slots_grid.rowCount()):
            for j in range(self.spell_slots_grid.columnCount()):
                item = self.spell_slots_grid.itemAt(i, j)
                if item:
                    self.spell_slots_grid.removeItem(item)
        
        if not spell_slots:
            return
        
        # Add headers
        self.spell_slots_grid.addWidget(QLabel('Level'), 0, 0)
        self.spell_slots_grid.addWidget(QLabel('Slots'), 0, 1)
        
        # Add spell slot rows
        for i, (slot_level, count) in enumerate(spell_slots.items()):
            row = i + 1
            self.spell_slots_grid.addWidget(QLabel(slot_level.title()), row, 0)
            self.spell_slots_grid.addWidget(QLabel(str(count)), row, 1)

    def select_items_by_value(items, total_value):
        selected = []
        pool = items[:]
        random.shuffle(pool)
        current_value = 0
        while pool and current_value < total_value:
            item = pool.pop()
            rarity = get_rarity(item)
            value = get_item_value(rarity)
            if current_value + value <= total_value:
                selected.append(item)
                current_value += value
            elif not selected:
                selected.append(item)
                break
        return selected

    class MagicItemGenerator(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Magic Item Generator')
            self.resize(1000, 700)
            self.tabs = QTabWidget()
            self.setCentralWidget(self.tabs)
            self.csv_data = {'header': [], 'rows': [], 'file_path': None}
            self.init_generator_tab()
            self.init_viewer_tab()
            self.init_character_creator_tab()
            self.status_bar = QStatusBar()
            self.setStatusBar(self.status_bar)

        def init_generator_tab(self):
            gen_tab = QWidget()
            gen_layout = QGridLayout()
            gen_tab.setLayout(gen_layout)
            self.tabs.addTab(gen_tab, 'Generator')
            self.mode_combo = QComboBox()
            self.mode_combo.addItems(['Shop', 'Loot'])
            gen_layout.addWidget(QLabel('Mode:'), 0, 0)
            gen_layout.addWidget(self.mode_combo, 0, 1)
            self.method_combo = QComboBox()
            self.method_combo.addItems(['By character level', 'By total gold value'])
            gen_layout.addWidget(QLabel('Loot Generation Method:'), 1, 0)
            gen_layout.addWidget(self.method_combo, 1, 1)
            self.out_name_edit = QLineEdit()
            gen_layout.addWidget(QLabel('Output file name (no .csv):'), 2, 0)
            gen_layout.addWidget(self.out_name_edit, 2, 1)
            self.max_items_spin = QSpinBox()
            self.max_items_spin.setRange(1, 1000)
            self.max_items_spin.setValue(10)
            gen_layout.addWidget(QLabel('Max items:'), 3, 0)
            gen_layout.addWidget(self.max_items_spin, 3, 1)
            self.level_spin = QSpinBox()
            self.level_spin.setRange(1, 20)
            self.level_spin.setValue(1)
            gen_layout.addWidget(QLabel('Character level (1-20):'), 4, 0)
            gen_layout.addWidget(self.level_spin, 4, 1)
            self.value_spin = QSpinBox()
            self.value_spin.setRange(1, 1000000)
            self.value_spin.setValue(1000)
            gen_layout.addWidget(QLabel('Total gold value (GP):'), 5, 0)
            gen_layout.addWidget(self.value_spin, 5, 1)
            self.method_combo.currentIndexChanged.connect(self.update_fields)
            self.update_fields()
            generate_btn = QPushButton('Generate')
            generate_btn.clicked.connect(self.on_generate)
            gen_layout.addWidget(generate_btn, 6, 0, 1, 2)

        def update_fields(self):
            if self.method_combo.currentIndex() == 0:
                self.level_spin.setEnabled(True)
                self.value_spin.setEnabled(False)
            else:
                self.level_spin.setEnabled(False)
                self.value_spin.setEnabled(True)

        def on_generate(self):
            mode = self.mode_combo.currentText()
            method = 'level' if self.method_combo.currentIndex() == 0 else 'value'
            out_name = self.out_name_edit.text().strip()
            max_items = self.max_items_spin.value()
            level = self.level_spin.value()
            value = self.value_spin.value()
            if not out_name or not max_items or (method == 'level' and not level) or (method == 'value' and not value):
                QMessageBox.critical(self, 'Error', 'Please fill in all required fields.')
                return
            try:
                if method == 'level':
                    msg = run_generation(mode, method, out_name, max_items, level=level)
                else:
                    msg = run_generation(mode, method, out_name, max_items, value=value)
                QMessageBox.information(self, 'Success', msg)
            except Exception as e:
                QMessageBox.critical(self, 'Error', str(e))

        def init_viewer_tab(self):
            viewer_tab = QWidget()
            viewer_layout = QVBoxLayout()
            viewer_tab.setLayout(viewer_layout)
            self.tabs.addTab(viewer_tab, 'CSV Viewer')

            # --- Top bar: Open, Save, Delete, Dark Mode ---
            top_bar = QHBoxLayout()
            open_btn = QPushButton('Open CSV File')
            open_btn.clicked.connect(self.load_csv)
            save_btn = QPushButton('Save CSV')
            save_btn.clicked.connect(self.save_csv)
            del_btn = QPushButton('Delete Selected Item(s)')
            del_btn.clicked.connect(self.delete_selected)
            dark_btn = QPushButton('Toggle Dark Mode')
            dark_btn.setCheckable(True)
            dark_btn.toggled.connect(self.toggle_dark_mode)
            top_bar.addWidget(open_btn)
            top_bar.addWidget(save_btn)
            top_bar.addWidget(del_btn)
            top_bar.addWidget(dark_btn)
            top_bar.addStretch()
            viewer_layout.addLayout(top_bar)

            # --- Search/filter bar ---
            filter_bar = QHBoxLayout()
            filter_label = QLabel('Search:')
            self.filter_edit = QLineEdit()
            self.filter_edit.setPlaceholderText('Type to filter...')
            self.filter_edit.textChanged.connect(self.update_table)
            clear_filter_btn = QPushButton('Clear')
            clear_filter_btn.clicked.connect(lambda: self.filter_edit.setText(''))
            filter_bar.addWidget(filter_label)
            filter_bar.addWidget(self.filter_edit)
            filter_bar.addWidget(clear_filter_btn)
            filter_bar.addStretch()
            viewer_layout.addLayout(filter_bar)

            # --- Table ---
            self.table = QTableWidget()
            self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
            self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.table.itemSelectionChanged.connect(self.update_preview)
            self.table.itemChanged.connect(self.on_table_item_changed)
            self.table.setSortingEnabled(True)
            self.table.setAlternatingRowColors(True)
            self.table.setStyleSheet('QTableWidget { font-size: 13pt; font-family: Segoe UI, Arial, sans-serif; } QHeaderView::section { padding: 8px; font-weight: bold; } QTableWidget::item { padding: 6px; }')
            self.table.horizontalHeader().setStretchLastSection(True)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            viewer_layout.addWidget(self.table)

            # --- Add Potions/Gemstones ---
            add_pg_bar = QHBoxLayout()
            add_pg_bar.addWidget(QLabel('Add Potions/Gemstones:'))
            add_pg_bar.addWidget(QLabel('Number of Potions:'))
            self.num_potions_spin = QSpinBox()
            self.num_potions_spin.setRange(1, 100)
            self.num_potions_spin.setValue(1)
            add_pg_bar.addWidget(self.num_potions_spin)
            add_potion_btn = QPushButton('Add Potions')
            add_potion_btn.clicked.connect(self.add_potions)
            add_pg_bar.addWidget(add_potion_btn)
            add_pg_bar.addWidget(QLabel('Gemstone Value:'))
            self.gem_value_spin = QSpinBox()
            self.gem_value_spin.setRange(1, 100000)
            self.gem_value_spin.setValue(100)
            add_pg_bar.addWidget(self.gem_value_spin)
            add_gem_btn = QPushButton('Add Gemstones')
            add_gem_btn.clicked.connect(self.add_gemstones)
            add_pg_bar.addWidget(add_gem_btn)
            add_pg_bar.addStretch()
            viewer_layout.addLayout(add_pg_bar)

            # --- Add Item by Rarity/Name ---
            add_item_bar = QHBoxLayout()
            add_item_bar.addWidget(QLabel('Add Item by Rarity/Name:'))
            self.additem_rarity_combo = QComboBox()
            self.additem_rarity_combo.addItems([r.title() for r in RARITY_LIST])
            add_item_bar.addWidget(self.additem_rarity_combo)
            add_item_bar.addWidget(QLabel('(optional) Name:'))
            self.additem_name_edit = QLineEdit()
            add_item_bar.addWidget(self.additem_name_edit)
            additem_btn = QPushButton('Add Item')
            additem_btn.clicked.connect(self.add_item_by_rarity)
            add_item_bar.addWidget(additem_btn)
            add_item_bar.addStretch()
            viewer_layout.addLayout(add_item_bar)

            # --- Add Custom Item ---
            add_custom_bar = QGridLayout()
            add_custom_bar.addWidget(QLabel('Add Custom Item:'), 0, 0)
            add_custom_bar.addWidget(QLabel('Name:'), 0, 1)
            self.custom_name_edit = QLineEdit()
            add_custom_bar.addWidget(self.custom_name_edit, 0, 2)
            add_custom_bar.addWidget(QLabel('Type:'), 0, 3)
            self.custom_type_edit = QLineEdit()
            add_custom_bar.addWidget(self.custom_type_edit, 0, 4)
            add_custom_bar.addWidget(QLabel('Rarity:'), 0, 5)
            self.custom_rarity_combo = QComboBox()
            self.custom_rarity_combo.addItems([r.title() for r in RARITY_LIST])
            add_custom_bar.addWidget(self.custom_rarity_combo, 0, 6)
            add_custom_bar.addWidget(QLabel('Text:'), 1, 1)
            self.custom_text_edit = QLineEdit()
            add_custom_bar.addWidget(self.custom_text_edit, 1, 2, 1, 3)
            add_custom_bar.addWidget(QLabel('Value:'), 1, 5)
            self.custom_value_edit = QLineEdit()
            add_custom_bar.addWidget(self.custom_value_edit, 1, 6)
            addcustom_btn = QPushButton('Add Custom Item')
            addcustom_btn.clicked.connect(self.add_custom_item)
            add_custom_bar.addWidget(addcustom_btn, 0, 7, 2, 1)
            viewer_layout.addLayout(add_custom_bar)

            # --- Text Preview ---
            self.preview_label = QLabel('Text Preview:')
            self.preview_label.setStyleSheet('font-weight: bold; font-size: 12pt; margin-top: 8px;')
            viewer_layout.addWidget(self.preview_label)
            self.preview_text = QTextEdit()
            self.preview_text.setReadOnly(True)
            self.preview_text.setStyleSheet('font-size: 12pt; font-family: Segoe UI, Arial, sans-serif; background: #f8f8f8; padding: 8px;')
            viewer_layout.addWidget(self.preview_text)

            # --- Keyboard shortcuts ---
            self.table.installEventFilter(self)
            self.shortcut_actions = {
                (Qt.ControlModifier, Qt.Key_S): self.save_csv,
                (Qt.NoModifier, Qt.Key_Delete): self.delete_selected,
                (Qt.ControlModifier, Qt.Key_F): lambda: self.filter_edit.setFocus(),
            }

        def eventFilter(self, obj, event):
            if obj is self.table and event.type() == QEvent.KeyPress:
                key = event.key()
                mods = event.modifiers()
                for (mod, k), action in self.shortcut_actions.items():
                    if mods == mod and key == k:
                        action()
                        return True
            return super().eventFilter(obj, event)

        def load_csv(self):
            file_path, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv)')
            if not file_path:
                return
            try:
                with open(file_path, newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                    if not rows:
                        QMessageBox.critical(self, 'Error', 'CSV file is empty.')
                        return
                    header = rows[0]
                    data = rows[1:]
                self.csv_data['header'] = header
                self.csv_data['rows'] = data
                self.csv_data['file_path'] = file_path
                self.update_table()
                self.status_bar.showMessage(f"Loaded {file_path} ({len(data)} items)")
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to load CSV: {e}')
                self.status_bar.showMessage('Failed to load CSV.')

        def save_csv(self):
            if not self.csv_data['file_path'] or not self.csv_data['header']:
                QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
                return
            try:
                with open(self.csv_data['file_path'], 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.csv_data['header'])
                    for row in self.csv_data['rows']:
                        writer.writerow(row)
                self.status_bar.showMessage('CSV saved.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save CSV: {e}')
                self.status_bar.showMessage('Failed to save CSV.')

        def update_table(self):
            header = self.csv_data.get('header', [])
            rows = self.csv_data.get('rows', [])
            query = self.filter_edit.text().strip().lower()
            if query:
                filtered = [row for row in rows if any(query in str(cell).lower() for cell in row)]
            else:
                filtered = rows
            self.filtered_rows = filtered
            self.table.blockSignals(True)
            self.table.setColumnCount(len(header))
            self.table.setHorizontalHeaderLabels(header)
            self.table.setRowCount(len(filtered))
            for i, row in enumerate(filtered):
                for j, val in enumerate(row):
                    item = QTableWidgetItem(val)
                    self.table.setItem(i, j, item)
            self.table.blockSignals(False)
            self.status_bar.showMessage(f"{len(filtered)} / {len(rows)} items shown.")
            self.update_preview()

        def update_preview(self):
            selected = self.table.selectedItems()
            if not selected or not self.filtered_rows:
                self.preview_text.setPlainText('')
                return
            row_idx = selected[0].row()
            row = self.filtered_rows[row_idx]
            text_idx = None
            for i, col in enumerate(self.csv_data['header']):
                if col.strip().lower() == 'text':
                    text_idx = i
                    break
            if text_idx is not None and row[text_idx]:
                self.preview_text.setPlainText(row[text_idx])
            else:
                self.preview_text.setPlainText('')

        def on_table_item_changed(self, item):
            # Update the underlying data when a cell is edited
            row_idx = item.row()
            col_idx = item.column()
            if 0 <= row_idx < len(self.filtered_rows):
                # Find the actual row in self.csv_data['rows']
                actual_row = self.filtered_rows[row_idx]
                actual_idx = self.csv_data['rows'].index(actual_row)
                self.csv_data['rows'][actual_idx][col_idx] = item.text()
                self.status_bar.showMessage('Cell updated.')

        def delete_selected(self):
            selected = self.table.selectionModel().selectedRows()
            if not selected:
                return
            idxs = sorted([s.row() for s in selected], reverse=True)
            count = 0
            for idx in idxs:
                if 0 <= idx < len(self.filtered_rows):
                    actual_row = self.filtered_rows[idx]
                    if actual_row in self.csv_data['rows']:
                        self.csv_data['rows'].remove(actual_row)
                        count += 1
            self.update_table()
            self.status_bar.showMessage(f"Deleted {count} item(s).")

        def add_potions(self):
            if not self.csv_data['header']:
                QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
                return
            n = self.num_potions_spin.value()
            try:
                with open('magic items.csv', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    magic_header = next(reader)
                    magic_data = list(reader)
            except Exception:
                QMessageBox.critical(self, 'Error', 'Could not load magic items.csv.')
                return
            # Find column indices by header
            def col_idx(col_name):
                for i, col in enumerate(magic_header):
                    if col.strip().lower() == col_name:
                        return i
                return None
            type_idx = col_idx('type') or 4
            rarity_idx = col_idx('rarity') or 3
            name_idx = col_idx('name') or 0
            attune_idx = col_idx('attunement') or 5
            text_idx = col_idx('text') or 11
            potions = [row for row in magic_data if type_idx < len(row) and 'potion' in row[type_idx].lower() and rarity_idx < len(row) and row[rarity_idx].strip().lower() in ['common', 'uncommon']]
            if not potions:
                QMessageBox.warning(self, 'Warning', 'No potions found in magic items.csv.')
                return
            chosen = random.sample(potions, min(n, len(potions)))
            for row in chosen:
                new_row = []
                rarity_val = row[rarity_idx].strip().lower() if rarity_idx < len(row) else ''
                for col in self.csv_data['header']:
                    col_l = col.strip().lower()
                    if col_l == 'name':
                        new_row.append(row[name_idx] if name_idx < len(row) else '')
                    elif col_l == 'rarity':
                        new_row.append(row[rarity_idx] if rarity_idx < len(row) else '')
                    elif col_l == 'type':
                        new_row.append(row[type_idx] if type_idx < len(row) and row[type_idx].strip() else 'Unknown')
                    elif col_l == 'text':
                        new_row.append(row[text_idx] if text_idx < len(row) else '')
                    elif col_l == 'value':
                        new_row.append(str(get_item_value(rarity_val)))
                    elif col_l == 'attunement':
                        new_row.append(row[attune_idx] if attune_idx < len(row) else '')
                    else:
                        new_row.append('')
                self.csv_data['rows'].append(new_row)
            self.update_table()
            self.status_bar.showMessage(f'Added {len(chosen)} potion(s).')

        def add_gemstones(self):
            if not self.csv_data['header']:
                QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
                return
            target_value = self.gem_value_spin.value()
            min_total = int(target_value * 0.9)
            max_total = int(target_value * 1.1)
            total = 0
            gems = []
            tries = 0
            import random
            while total < min_total and tries < 1000:
                gem = random.choice(list(GEMSTONE_VALUE_LIST.keys()))
                quality = random.choice(list(GEMSTONE_VALUE_LIST[gem].keys()))
                value = GEMSTONE_VALUE_LIST[gem][quality]
                if total + value > max_total:
                    tries += 1
                    continue
                gems.append((gem, quality, value))
                total += value
                tries += 1
            if not gems:
                QMessageBox.warning(self, 'Warning', 'Could not generate gemstones for value.')
                return
            for gem, quality, value in gems:
                row = ['Gemstone', quality, gem, str(value), '', f'{quality} {gem} ({value} gp)']
                # Pad to match header
                while len(row) < len(self.csv_data['header']):
                    row.append('')
                self.csv_data['rows'].append(row)
            self.update_table()
            self.status_bar.showMessage(f'Added {len(gems)} gemstone(s) totaling {total} gp.')

        def fuzzy_match(self, query, candidates):
            matches = [c for c in candidates if query.lower() in c.lower()]
            if matches:
                return matches[0]
            try:
                import difflib
                close = difflib.get_close_matches(query, candidates, n=1)
                return close[0] if close else None
            except ImportError:
                return None

        def add_item_by_rarity(self):
            if not self.csv_data['header']:
                QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
                return
            rarity = self.additem_rarity_combo.currentText().strip().lower()
            name_query = self.additem_name_edit.text().strip()
            try:
                with open('magic items.csv', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    magic_header = next(reader)
                    magic_data = list(reader)
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not load magic items.csv: {e}')
                return
            # Find column indices by header
            def col_idx(col_name):
                for i, col in enumerate(magic_header):
                    if col.strip().lower() == col_name:
                        return i
                return None
            name_idx = col_idx('name') or 0
            rarity_idx = col_idx('rarity') or 3
            type_idx = col_idx('type') or 4
            attune_idx = col_idx('attunement') or 5
            text_idx = col_idx('text') or 11
            pool = [row for row in magic_data if rarity_idx < len(row) and get_rarity(row, magic_header) == rarity]
            if not pool:
                QMessageBox.warning(self, 'Warning', f'No items of rarity {rarity.title()} found.')
                return
            if name_query:
                names = [row[name_idx] for row in pool if name_idx < len(row)]
                match = self.fuzzy_match(name_query, names)
                if match:
                    row = next(row for row in pool if name_idx < len(row) and row[name_idx] == match)
                else:
                    QMessageBox.warning(self, 'Warning', f'No item found matching "{name_query}".')
                    return
            else:
                row = random.choice(pool)
            new_row = []
            rarity_val = row[rarity_idx].strip().lower() if rarity_idx < len(row) else ''
            for col in self.csv_data['header']:
                col_l = col.strip().lower()
                if col_l == 'name':
                    new_row.append(row[name_idx] if name_idx < len(row) else '')
                elif col_l == 'rarity':
                    new_row.append(row[rarity_idx] if rarity_idx < len(row) else '')
                elif col_l == 'type':
                    new_row.append(row[type_idx] if type_idx < len(row) and row[type_idx].strip() else 'Unknown')
                elif col_l == 'text':
                    new_row.append(row[text_idx] if text_idx < len(row) else '')
                elif col_l == 'value':
                    new_row.append(str(get_item_value(rarity_val)))
                elif col_l == 'attunement':
                    new_row.append(row[attune_idx] if attune_idx < len(row) else '')
                else:
                    new_row.append('')
            self.csv_data['rows'].append(new_row)
            self.update_table()
            self.status_bar.showMessage(f'Added item: {new_row[0]} ({rarity.title()})')

        def add_custom_item(self):
            if not self.csv_data['header']:
                QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
                return
            name = self.custom_name_edit.text().strip()
            typ = self.custom_type_edit.text().strip()
            rarity = self.custom_rarity_combo.currentText().strip().lower()
            text = self.custom_text_edit.text().strip()
            value = self.custom_value_edit.text().strip()
            if not name or not typ or not rarity:
                QMessageBox.warning(self, 'Warning', 'Name, Type, and Rarity are required.')
                return
            row = []
            for col in self.csv_data['header']:
                if col.strip().lower() == 'name':
                    row.append(name)
                elif col.strip().lower() == 'type':
                    row.append(typ)
                elif col.strip().lower() == 'rarity':
                    row.append(rarity)
                elif col.strip().lower() == 'text':
                    row.append(text)
                elif col.strip().lower() == 'value':
                    row.append(value)
                else:
                    row.append('')
            self.csv_data['rows'].append(row)
            self.update_table()
            self.status_bar.showMessage(f'Added custom item: {name} ({rarity.title()})')

        def keyPressEvent(self, event):
            # Keyboard shortcuts: Ctrl+S (save), Delete (delete), Ctrl+F (focus filter)
            if event.matches(QKeySequence.Save):
                self.save_csv()
                event.accept()
            elif event.key() == Qt.Key_Delete:
                self.delete_selected()
                event.accept()
            elif event.matches(QKeySequence.Find):
                self.filter_edit.setFocus()
                event.accept()
            else:
                super().keyPressEvent(event)

        def toggle_dark_mode(self, enabled):
            if enabled:
                dark_stylesheet = """
                    QWidget { background: #232629; color: #e0e0e0; }
                    QTableWidget { background: #2b2b2b; color: #e0e0e0; alternate-background-color: #232629; }
                    QHeaderView::section { background: #232629; color: #e0e0e0; }
                    QLineEdit, QTextEdit { background: #232629; color: #e0e0e0; border: 1px solid #444; }
                    QPushButton { background: #353535; color: #e0e0e0; border: 1px solid #444; padding: 6px; }
                    QPushButton:checked { background: #444; }
                    QComboBox, QSpinBox { background: #232629; color: #e0e0e0; border: 1px solid #444; }
                    QStatusBar { background: #232629; color: #e0e0e0; }
                """
                self.setStyleSheet(dark_stylesheet)
            else:
                self.setStyleSheet("")

        def make_collapsible_section(self, title, content_widget):
            # Returns a QWidget with a toggle button and collapsible content
            container = QWidget()
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            toggle = QToolButton()
            toggle.setText(title)
            toggle.setCheckable(True)
            toggle.setChecked(False)
            toggle.setStyleSheet('QToolButton { font-weight: bold; font-size: 12pt; text-align: left; }')
            toggle.setToolButtonStyle(Qt.ToolButtonTextOnly)
            toggle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            frame = QFrame()
            frame.setFrameShape(QFrame.NoFrame)
            frame.setLayout(QVBoxLayout())
            frame.layout().addWidget(content_widget)
            frame.setVisible(False)
            def on_toggle(checked):
                frame.setVisible(checked)
            toggle.toggled.connect(on_toggle)
            layout.addWidget(toggle)
            layout.addWidget(frame)
            return container

        def init_character_creator_tab(self):
            char_tab = QWidget()
            char_layout = QVBoxLayout()
            char_tab.setLayout(char_layout)

            # Initialize required attributes
            self.required_race_skills = 0
            self.allowed_race_skills = []
            self.required_class_skills = 0
            self.allowed_class_skills = []

            # --- Race Dropdown ---
            race_bar = QHBoxLayout()
            race_label = QLabel('Race:')
            self.race_combo = QComboBox()
            # Load races from races.csv and store full data for info display
            self.race_data = []
            races = []
            try:
                with open('races.csv', 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        name = row['name'].strip()
                        if name:
                            races.append(name)
                            self.race_data.append(row)
            except Exception:
                pass
            unique_races = sorted(set(races))
            self.race_combo.addItems(unique_races)
            race_bar.addWidget(race_label)
            race_bar.addWidget(self.race_combo)
            race_bar.addStretch()
            char_layout.addLayout(race_bar)

            # --- Race Info Display ---
            self.race_info_label = QLabel()
            self.race_info_label.setWordWrap(True)
            self.race_info_label.setStyleSheet('font-size: 11pt; background: #f8f8f8; padding: 8px; border: 1px solid #ccc;')
            race_scroll = QScrollArea()
            race_scroll.setWidgetResizable(True)
            race_scroll.setMinimumHeight(60)
            race_scroll.setMaximumHeight(200)
            race_scroll.setWidget(self.race_info_label)
            race_info_section = self.make_collapsible_section('Show Race Details', race_scroll)
            char_layout.addWidget(race_info_section)

            self.race_combo.currentTextChanged.connect(self.update_race_info)
            self.update_race_info(self.race_combo.currentText())

            # --- Background Dropdown ---
            bg_bar = QHBoxLayout()
            bg_label = QLabel('Background:')
            self.bg_combo = QComboBox()
            self.background_data = []
            backgrounds = []
            try:
                with open('backgrounds.csv', 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        name = row['name'].strip()
                        if name:
                            backgrounds.append(name)
                            self.background_data.append(row)
            except Exception:
                pass
            unique_bgs = sorted(set(backgrounds))
            self.bg_combo.addItems(unique_bgs)
            bg_bar.addWidget(bg_label)
            bg_bar.addWidget(self.bg_combo)
            bg_bar.addStretch()
            char_layout.addLayout(bg_bar)

            # --- Background Info Display ---
            self.bg_info_label = QLabel()
            self.bg_info_label.setWordWrap(True)
            self.bg_info_label.setStyleSheet('font-size: 11pt; background: #f8f8f8; padding: 8px; border: 1px solid #ccc;')
            bg_scroll = QScrollArea()
            bg_scroll.setWidgetResizable(True)
            bg_scroll.setMinimumHeight(60)
            bg_scroll.setMaximumHeight(200)
            bg_scroll.setWidget(self.bg_info_label)
            bg_info_section = self.make_collapsible_section('Show Background Details', bg_scroll)
            char_layout.addWidget(bg_info_section)

            self.bg_combo.currentTextChanged.connect(self.update_bg_info)
            self.update_bg_info(self.bg_combo.currentText())

            # --- Class Dropdown ---
            class_bar = QHBoxLayout()
            class_label = QLabel('Class:')
            self.class_combo = QComboBox()
            import json
            self.class_data = []
            classes = []
            try:
                with open('classes.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for entry in data.get('classes', []):
                        name = entry.get('name', '').strip()
                        if name:
                            classes.append(name)
                            self.class_data.append(entry)
            except Exception:
                pass
            unique_classes = sorted(set(classes))
            self.class_combo.addItems(unique_classes)
            class_bar.addWidget(class_label)
            class_bar.addWidget(self.class_combo)
            class_bar.addStretch()
            char_layout.addLayout(class_bar)

            # --- Class Info Display ---
            self.class_info_label = QLabel()
            self.class_info_label.setWordWrap(True)
            self.class_info_label.setStyleSheet('font-size: 12pt; background: #f8f8f8; padding: 10px; border: 2px solid #888;')
            # Put class info label in a scroll area
            class_scroll = QScrollArea()
            class_scroll.setWidgetResizable(True)
            class_scroll.setMinimumHeight(200)
            class_scroll.setMaximumHeight(500)
            class_scroll.setWidget(self.class_info_label)
            class_info_section = self.make_collapsible_section('Show Class Details', class_scroll)
            # Add class section with stretch to make it dominant
            char_layout.addWidget(class_info_section, stretch=2)

            self.class_combo.currentTextChanged.connect(self.update_class_info)
            self.update_class_info(self.class_combo.currentText())

            # --- Stat Generation Section ---
            stat_gen_bar = QHBoxLayout()
            stat_label = QLabel('Stat Generation:')
            stat_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
            stat_gen_bar.addWidget(stat_label)

            # --- Stat Section (Unified Row per Stat) ---
            stat_names = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']
            stat_grid = QGridLayout()
            stat_grid.addWidget(QLabel('<b>Stat</b>'), 0, 0)
            stat_grid.addWidget(QLabel('<b>Value</b>'), 0, 1)
            stat_grid.addWidget(QLabel('<b>Score Increases</b>'), 0, 2)
            stat_grid.addWidget(QLabel('<b>Total</b>'), 0, 3)
            self.stat_spinboxes = []
            self.stat_increase_labels = []
            self.stat_total_labels = []
            self.stat_combos = []
            for i, stat in enumerate(stat_names):
                stat_grid.addWidget(QLabel(stat), i+1, 0)
                spin = QSpinBox()
                spin.setRange(1, 20)
                spin.setValue(10)
                stat_grid.addWidget(spin, i+1, 1)
                inc_label = QLabel('0')
                inc_label.setMinimumWidth(24)
                inc_label.setAlignment(Qt.AlignLeft)
                stat_grid.addWidget(inc_label, i+1, 2)
                total_label = QLabel('10')
                total_label.setMinimumWidth(24)
                total_label.setAlignment(Qt.AlignLeft)
                stat_grid.addWidget(total_label, i+1, 3)
                self.stat_spinboxes.append(spin)
                self.stat_increase_labels.append(inc_label)
                self.stat_total_labels.append(total_label)
            stat_grid.setHorizontalSpacing(12)
            stat_grid.setVerticalSpacing(4)

            # --- ASI Source Selection (Radio Buttons) ---
            from PySide6.QtWidgets import QRadioButton, QButtonGroup
            asi_radio_bar = QHBoxLayout()
            asi_radio_bar.addWidget(QLabel('Apply Ability Score Increases from:'))
            self.asi_group = QButtonGroup()
            self.asi_race_radio = QRadioButton('Race')
            self.asi_bg_radio = QRadioButton('Background')
            self.asi_both_radio = QRadioButton('Both')
            self.asi_neither_radio = QRadioButton('Neither')
            self.asi_race_radio.setChecked(True)
            self.asi_group.addButton(self.asi_race_radio, 0)
            self.asi_group.addButton(self.asi_bg_radio, 1)
            self.asi_group.addButton(self.asi_both_radio, 2)
            self.asi_group.addButton(self.asi_neither_radio, 3)
            asi_radio_bar.addWidget(self.asi_race_radio)
            asi_radio_bar.addWidget(self.asi_bg_radio)
            asi_radio_bar.addWidget(self.asi_both_radio)
            asi_radio_bar.addWidget(self.asi_neither_radio)
            asi_radio_bar.addStretch()
            self.asi_group.buttonClicked.connect(self.update_stat_totals)
            self.asi_group.buttonClicked.connect(self.on_asi_source_changed)

            # --- Stat Generation Parameters ---
            param_bar = QHBoxLayout()
            self.lowest_stat_min_spin = QSpinBox()
            self.lowest_stat_min_spin.setRange(1, 20)
            self.lowest_stat_min_spin.setValue(7)
            param_bar.addWidget(QLabel('Lowest Stat Min:'))
            param_bar.addWidget(self.lowest_stat_min_spin)
            self.lowest_stat_max_spin = QSpinBox()
            self.lowest_stat_max_spin.setRange(1, 20)
            self.lowest_stat_max_spin.setValue(9)
            param_bar.addWidget(QLabel('Lowest Stat Max:'))
            param_bar.addWidget(self.lowest_stat_max_spin)
            self.highest_stat_min_spin = QSpinBox()
            self.highest_stat_min_spin.setRange(1, 20)
            self.highest_stat_min_spin.setValue(15)
            param_bar.addWidget(QLabel('Highest Stat Min:'))
            param_bar.addWidget(self.highest_stat_min_spin)
            self.highest_stat_max_spin = QSpinBox()
            self.highest_stat_max_spin.setRange(1, 20)
            self.highest_stat_max_spin.setValue(17)
            param_bar.addWidget(QLabel('Highest Stat Max:'))
            param_bar.addWidget(self.highest_stat_max_spin)
            self.average_min_spin = QDoubleSpinBox()
            self.average_min_spin.setRange(1, 20)
            self.average_min_spin.setDecimals(2)
            self.average_min_spin.setValue(12)
            param_bar.addWidget(QLabel('Average Min:'))
            param_bar.addWidget(self.average_min_spin)
            self.average_max_spin = QDoubleSpinBox()
            self.average_max_spin.setRange(1, 20)
            self.average_max_spin.setDecimals(2)
            self.average_max_spin.setValue(13.50)
            param_bar.addWidget(QLabel('Average Max:'))
            param_bar.addWidget(self.average_max_spin)
            param_bar.addStretch()

            # --- Generate Button ---
            stat_controls_bar = QHBoxLayout()
            gen_btn = QPushButton('Generate Stats')
            gen_btn.clicked.connect(self.generate_stats)
            stat_controls_bar.addWidget(gen_btn)
            stat_controls_bar.addStretch()

            # Add to layout
            char_layout.addLayout(race_bar)
            char_layout.addWidget(race_info_section)
            char_layout.addLayout(bg_bar)
            char_layout.addWidget(bg_info_section)
            char_layout.addLayout(class_bar)
            char_layout.addWidget(class_info_section)
            char_layout.addLayout(asi_radio_bar)
            char_layout.addLayout(stat_grid)
            char_layout.addLayout(stat_controls_bar)
            char_layout.addLayout(param_bar)        # --- Character Info Inputs (Name, Alignment, Player Name) ---
            info_bar = QHBoxLayout()
            info_bar.addWidget(QLabel('Character Name:'))
            self.char_name_edit = QLineEdit()
            info_bar.addWidget(self.char_name_edit)
            info_bar.addWidget(QLabel('Alignment:'))
            self.alignment_combo = QComboBox()
            self.alignment_combo.addItems([
                'Lawful Good', 'Neutral Good', 'Chaotic Good',
                'Lawful Neutral', 'True Neutral', 'Chaotic Neutral',
                'Lawful Evil', 'Neutral Evil', 'Chaotic Evil'
            ])
            info_bar.addWidget(self.alignment_combo)
            info_bar.addWidget(QLabel('Player Name:'))
            self.player_name_edit = QLineEdit()
            info_bar.addWidget(self.player_name_edit)
            info_bar.addStretch()
            char_layout.insertLayout(0, info_bar)
            
            # Connect stat spinboxes to update totals (no prompt)
            for spin in self.stat_spinboxes:
                spin.valueChanged.connect(self.update_stat_totals)
            # Connect ASI radio group to prompt+update
            self.asi_group.buttonClicked.disconnect()
            self.asi_group.buttonClicked.connect(self.on_asi_source_changed)        # --- Character Level and Progression Section ---
            level_section = QWidget()
            level_layout = QVBoxLayout(level_section)
            
            # Level controls
            level_controls = QHBoxLayout()
            level_controls.addWidget(QLabel('Character Level:'))
            
            # Create character level spinner (separate from generator level spinner)
            self.char_level_spin = QSpinBox()
            self.char_level_spin.setRange(1, 20)
            self.char_level_spin.setValue(1)
            level_controls.addWidget(self.char_level_spin)
            
            # Level progression controls
            level_up_btn = QPushButton('Level Up')
            level_down_btn = QPushButton('Level Down')
            level_up_btn.clicked.connect(lambda: self.char_level_spin.setValue(min(20, self.char_level_spin.value() + 1)))
            level_down_btn.clicked.connect(lambda: self.char_level_spin.setValue(max(1, self.char_level_spin.value() - 1)))
            level_controls.addWidget(level_up_btn)
            level_controls.addWidget(level_down_btn)
            
            level_controls.addStretch()
            level_layout.addLayout(level_controls)
            
            # Character stats display
            stats_grid = QGridLayout()
            stats_grid.addWidget(QLabel('<b>Level</b>'), 0, 0)
            stats_grid.addWidget(QLabel('<b>Hit Points</b>'), 0, 1)
            stats_grid.addWidget(QLabel('<b>Proficiency Bonus</b>'), 0, 2)
            stats_grid.addWidget(QLabel('<b>Hit Die</b>'), 0, 3)
            
            self.level_display = QLabel('1')
            self.hit_points_display = QLabel('--')
            self.proficiency_display = QLabel('+2')
            self.hit_die_display = QLabel('--')
            
            stats_grid.addWidget(self.level_display, 1, 0)
            stats_grid.addWidget(self.hit_points_display, 1, 1)
            stats_grid.addWidget(self.proficiency_display, 1, 2)
            stats_grid.addWidget(self.hit_die_display, 1, 3)
            
            level_layout.addLayout(stats_grid)
            
            # Class Features Section
            self.class_features_widget = QWidget()
            self.class_features_layout = QVBoxLayout(self.class_features_widget)
            
            self.class_features_label = QLabel('Class Features:')
            self.class_features_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
            self.class_features_layout.addWidget(self.class_features_label)
            
            # Scrollable area for class features
            self.features_scroll = QScrollArea()
            self.features_scroll.setWidgetResizable(True)
            self.features_scroll.setMinimumHeight(150)
            self.features_scroll.setMaximumHeight(300)
            
            self.features_content = QLabel()
            self.features_content.setWordWrap(True)
            self.features_content.setStyleSheet('font-size: 11pt; background: #f8f8f8; padding: 8px; border: 1px solid #ccc;')
            self.features_content.setAlignment(Qt.AlignTop)
            self.features_scroll.setWidget(self.features_content)
            
            self.class_features_layout.addWidget(self.features_scroll)
            level_layout.addWidget(self.class_features_widget)
            
            # Spell Slot Progression for Casters
            self.spell_slots_widget = QWidget()
            self.spell_slots_layout = QVBoxLayout(self.spell_slots_widget)
            
            self.spell_slots_label = QLabel('Spell Slots:')
            self.spell_slots_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
            self.spell_slots_layout.addWidget(self.spell_slots_label)
            
            # Create grid for spell slot display
            self.spell_slots_grid = QGridLayout()
            self.spell_slots_layout.addLayout(self.spell_slots_grid)
            level_layout.addWidget(self.spell_slots_widget)
            
            # Ability Score Improvements tracking
            self.asi_widget = QWidget()
            self.asi_layout = QVBoxLayout(self.asi_widget)
            
            self.asi_label = QLabel('Ability Score Improvements Available:')
            self.asi_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
            self.asi_layout.addWidget(self.asi_label)
            
            self.asi_display = QLabel('Next ASI at level 4')
            self.asi_display.setStyleSheet('font-size: 11pt; padding: 4px;')
            self.asi_layout.addWidget(self.asi_display)
            level_layout.addWidget(self.asi_widget)
            
            # Make the whole level section collapsible
            level_collapsible = self.make_collapsible_section('Character Level & Progression', level_section)
            char_layout.addWidget(level_collapsible)
            
            # Connect level changes to update displays
            self.char_level_spin.valueChanged.connect(self.update_level_displays)
            self.class_combo.currentTextChanged.connect(self.update_level_displays)
            
            # Initialize displays
            QTimer.singleShot(100, self.update_level_displays)

        def update_level_displays(self):
            """Update the level progression displays"""
            level = self.char_level_spin.value()
            class_name = self.class_combo.currentText()
            
            # Update level, hit points, proficiency bonus, and hit die displays
            self.level_display.setText(str(level))
            
            # Calculate proficiency bonus based on character level
            proficiency_bonus = 2  # Level 1-4
            if level >= 5:
                proficiency_bonus = 3  # Level 5-8
            if level >= 9:
                proficiency_bonus = 4  # Level 9-12
            if level >= 13:
                proficiency_bonus = 5  # Level 13-16
            if level >= 17:
                proficiency_bonus = 6  # Level 17-20
            self.proficiency_display.setText(f'+{proficiency_bonus}')
            
            # Get hit die for the class
            hit_die = '--'
            for entry in self.class_data:
                if entry.get('name', '').strip() == class_name:
                    hit_die = entry.get('hit_die', '--')
                    break
            self.hit_die_display.setText(hit_die)
            
            # Calculate hit points
            hp_max = 0
            if hit_die != '--':
                # Roll for HP: max at 1st level + roll for each additional level
                import random
                first_level_hp = int(hit_die.split('d')[1]) + mods['CON']
                hp_max = first_level_hp
                
                if level > 1:
                    rolled_hp = []
                    for i in range(level - 1):
                        roll = random.randint(1, int(hit_die.split('d')[1]))
                        rolled_hp.append(roll)
                        hp_max += roll + mods['CON']
                    
                    # Show the user what was rolled
                    rolls_text = ', '.join(map(str, rolled_hp))
                    QMessageBox.information(self, 'HP Rolls', 
                        f'Rolled {rolls_text} for levels 2-{level}\n'
                        f'Total HP: {hp_max} (includes CON modifier)')
            
            self.hit_points_display.setText(str(hp_max))
            
            # Update class features based on level
            features = ''
            for entry in self.class_data:
                if entry.get('name', '').strip() == class_name:
                    # Get features for the current level
                    level_features = entry.get('features', {}).get(str(level), [])
                    if level_features:
                        features += f"Level {level} Features:\n"
                        for feature in level_features:
                            features += f"- {feature.get('name', '')}\n"
                    break
            self.features_content.setText(features.strip())
            
            # Update spell slots display
            self.update_spell_slots_display(class_name, level)

        def update_spell_slots_display(self, class_name, level):
            """Update the spell slots display based on class and level"""
            caster_type = self.get_caster_type(class_name)
            spell_slots = self.get_spell_slots(caster_type, level)
            
            # Clear existing spell slot rows
            for i in range(self.spell_slots_grid.rowCount()):
                for j in range(self.spell_slots_grid.columnCount()):
                    item = self.spell_slots_grid.itemAt(i, j)
                    if item:
                        self.spell_slots_grid.removeItem(item)
            
            if not spell_slots:
                return
            
            # Add headers
            self.spell_slots_grid.addWidget(QLabel('Level'), 0, 0)
            self.spell_slots_grid.addWidget(QLabel('Slots'), 0, 1)
            
            # Add spell slot rows
            for i, (slot_level, count) in enumerate(spell_slots.items()):
                row = i + 1
                self.spell_slots_grid.addWidget(QLabel(slot_level.title()), row, 0)
                self.spell_slots_grid.addWidget(QLabel(str(count)), row, 1)

        def select_items_by_value(items, total_value):
            selected = []
            pool = items[:]
            random.shuffle(pool)
            current_value = 0
            while pool and current_value < total_value:
                item = pool.pop()
                rarity = get_rarity(item)
                value = get_item_value(rarity)
                if current_value + value <= total_value:
                    selected.append(item)
                    current_value += value
                elif not selected:
                    selected.append(item)
                    break
            return selected

        class MagicItemGenerator(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle('Magic Item Generator')
                self.resize(1000, 700)
                self.tabs = QTabWidget()
                self.setCentralWidget(self.tabs)
                self.csv_data = {'header': [], 'rows': [], 'file_path': None}
                self.init_generator_tab()
                self.init_viewer_tab()
                self.init_character_creator_tab()
                self.status_bar = QStatusBar()
                self.setStatusBar(self.status_bar)

            def init_generator_tab(self):
                gen_tab = QWidget()
                gen_layout = QGridLayout()
                gen_tab.setLayout(gen_layout)
                self.tabs.addTab(gen_tab, 'Generator')
                self.mode_combo = QComboBox()
                self.mode_combo.addItems(['Shop', 'Loot'])
                gen_layout.addWidget(QLabel('Mode:'), 0, 0)
                gen_layout.addWidget(self.mode_combo, 0, 1)
                self.method_combo = QComboBox()
                self.method_combo.addItems(['By character level', 'By total gold value'])
                gen_layout.addWidget(QLabel('Loot Generation Method:'), 1, 0)
                gen_layout.addWidget(self.method_combo, 1, 1)
                self.out_name_edit = QLineEdit()
                gen_layout.addWidget(QLabel('Output file name (no .csv):'), 2, 0)
                gen_layout.addWidget(self.out_name_edit, 2, 1)
                self.max_items_spin = QSpinBox()
                self.max_items_spin.setRange(1, 1000)
                self.max_items_spin.setValue(10)
                gen_layout.addWidget(QLabel('Max items:'), 3, 0)
                gen_layout.addWidget(self.max_items_spin, 3, 1)
                self.level_spin = QSpinBox()
                self.level_spin.setRange(1, 20)
                self.level_spin.setValue(1)
                gen_layout.addWidget(QLabel('Character level (1-20):'), 4, 0)
                gen_layout.addWidget(self.level_spin, 4, 1)
                self.value_spin = QSpinBox()
                self.value_spin.setRange(1, 1000000)
                self.value_spin.setValue(1000)
                gen_layout.addWidget(QLabel('Total gold value (GP):'), 5, 0)
                gen_layout.addWidget(self.value_spin, 5, 1)
                self.method_combo.currentIndexChanged.connect(self.update_fields)
                self.update_fields()
                generate_btn = QPushButton('Generate')
                generate_btn.clicked.connect(self.on_generate)
                gen_layout.addWidget(generate_btn, 6, 0, 1, 2)

            def update_fields(self):
                if self.method_combo.currentIndex() == 0:
                    self.level_spin.setEnabled(True)
                    self.value_spin.setEnabled(False)
                else:
                    self.level_spin.setEnabled(False)
                    self.value_spin.setEnabled(True)

            def on_generate(self):
                mode = self.mode_combo.currentText()
                method = 'level' if self.method_combo.currentIndex() == 0 else 'value'
                out_name = self.out_name_edit.text().strip()
                max_items = self.max_items_spin.value()
                level = self.level_spin.value()
                value = self.value_spin.value()
                if not out_name or not max_items or (method == 'level' and not level) or (method == 'value' and not value):
                    QMessageBox.critical(self, 'Error', 'Please fill in all required fields.')
                    return
                try:
                    if method == 'level':
                        msg = run_generation(mode, method, out_name, max_items, level=level)
                    else:
                        msg = run_generation(mode, method, out_name, max_items, value=value)
                    QMessageBox.information(self, 'Success', msg)
                except Exception as e:
                    QMessageBox.critical(self, 'Error', str(e))

            def init_viewer_tab(self):
                viewer_tab = QWidget()
                viewer_layout = QVBoxLayout()
                viewer_tab.setLayout(viewer_layout)
                self.tabs.addTab(viewer_tab, 'CSV Viewer')

                # --- Top bar: Open, Save, Delete, Dark Mode ---
                top_bar = QHBoxLayout()
                open_btn = QPushButton('Open CSV File')
                open_btn.clicked.connect(self.load_csv)
                save_btn = QPushButton('Save CSV')
                save_btn.clicked.connect(self.save_csv)
                del_btn = QPushButton('Delete Selected Item(s)')
                del_btn.clicked.connect(self.delete_selected)
                dark_btn = QPushButton('Toggle Dark Mode')
                dark_btn.setCheckable(True)
                dark_btn.toggled.connect(self.toggle_dark_mode)
                top_bar.addWidget(open_btn)
                top_bar.addWidget(save_btn)
                top_bar.addWidget(del_btn)
                top_bar.addWidget(dark_btn)
                top_bar.addStretch()
                viewer_layout.addLayout(top_bar)

                # --- Search/filter bar ---
                filter_bar = QHBoxLayout()
                filter_label = QLabel('Search:')
                self.filter_edit = QLineEdit()
                self.filter_edit.setPlaceholderText('Type to filter...')
                self.filter_edit.textChanged.connect(self.update_table)
                clear_filter_btn = QPushButton('Clear')
                clear_filter_btn.clicked.connect(lambda: self.filter_edit.setText(''))
                filter_bar.addWidget(filter_label)
                filter_bar.addWidget(self.filter_edit)
                filter_bar.addWidget(clear_filter_btn)
                filter_bar.addStretch()
                viewer_layout.addLayout(filter_bar)

                # --- Table ---
                self.table = QTableWidget()
                self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
                self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
                self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
                self.table.itemSelectionChanged.connect(self.update_preview)
                self.table.itemChanged.connect(self.on_table_item_changed)
                self.table.setSortingEnabled(True)
                self.table.setAlternatingRowColors(True)
                self.table.setStyleSheet('QTableWidget { font-size: 13pt; font-family: Segoe UI, Arial, sans-serif; } QHeaderView::section { padding: 8px; font-weight: bold; } QTableWidget::item { padding: 6px; }')
                self.table.horizontalHeader().setStretchLastSection(True)
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                viewer_layout.addWidget(self.table)

                # --- Add Potions/Gemstones ---
                add_pg_bar = QHBoxLayout()
                add_pg_bar.addWidget(QLabel('Add Potions/Gemstones:'))
                add_pg_bar.addWidget(QLabel('Number of Potions:'))
                self.num_potions_spin = QSpinBox()
                self.num_potions_spin.setRange(1, 100)
                self.num_potions_spin.setValue(1)
                add_pg_bar.addWidget(self.num_potions_spin)
                add_potion_btn = QPushButton('Add Potions')
                add_potion_btn.clicked.connect(self.add_potions)
                add_pg_bar.addWidget(add_potion_btn)
                add_pg_bar.addWidget(QLabel('Gemstone Value:'))
                self.gem_value_spin = QSpinBox()
                self.gem_value_spin.setRange(1, 100000)
                self.gem_value_spin.setValue(100)
                add_pg_bar.addWidget(self.gem_value_spin)
                add_gem_btn = QPushButton('Add Gemstones')
                add_gem_btn.clicked.connect(self.add_gemstones)
                add_pg_bar.addWidget(add_gem_btn)
                add_pg_bar.addStretch()
                viewer_layout.addLayout(add_pg_bar)

                # --- Add Item by Rarity/Name ---
                add_item_bar = QHBoxLayout()
                add_item_bar.addWidget(QLabel('Add Item by Rarity/Name:'))
                self.additem_rarity_combo = QComboBox()
                self.additem_rarity_combo.addItems([r.title() for r in RARITY_LIST])
                add_item_bar.addWidget(self.additem_rarity_combo)
                add_item_bar.addWidget(QLabel('(optional) Name:'))
                self.additem_name_edit = QLineEdit()
                add_item_bar.addWidget(self.additem_name_edit)
                additem_btn = QPushButton('Add Item')
                additem_btn.clicked.connect(self.add_item_by_rarity)
                add_item_bar.addWidget(additem_btn)
                add_item_bar.addStretch()
                viewer_layout.addLayout(add_item_bar)

                # --- Add Custom Item ---
                add_custom_bar = QGridLayout()
                add_custom_bar.addWidget(QLabel('Add Custom Item:'), 0, 0)
                add_custom_bar.addWidget(QLabel('Name:'), 0, 1)
                self.custom_name_edit = QLineEdit()
                add_custom_bar.addWidget(self.custom_name_edit, 0, 2)
                add_custom_bar.addWidget(QLabel('Type:'), 0, 3)
                self.custom_type_edit = QLineEdit()
                add_custom_bar.addWidget(self.custom_type_edit, 0, 4)
                add_custom_bar.addWidget(QLabel('Rarity:'), 0, 5)
                self.custom_rarity_combo = QComboBox()
                self.custom_rarity_combo.addItems([r.title() for r in RARITY_LIST])
                add_custom_bar.addWidget(self.custom_rarity_combo, 0, 6)
                add_custom_bar.addWidget(QLabel('Text:'), 1, 1)
                self.custom_text_edit = QLineEdit()
                add_custom_bar.addWidget(self.custom_text_edit, 1, 2, 1, 3)
                add_custom_bar.addWidget(QLabel('Value:'), 1, 5)
                self.custom_value_edit = QLineEdit()
                add_custom_bar.addWidget(self.custom_value_edit, 1, 6)
                addcustom_btn = QPushButton('Add Custom Item')
                addcustom_btn.clicked.connect(self.add_custom_item)
                add_custom_bar.addWidget(addcustom_btn, 0, 7, 2, 1)
                viewer_layout.addLayout(add_custom_bar)

                # --- Text Preview ---
                self.preview_label = QLabel('Text Preview:')
                self.preview_label.setStyleSheet('font-weight: bold; font-size: 12pt; margin-top: 8px;')
                viewer_layout.addWidget(self.preview_label)
                self.preview_text = QTextEdit()
                self.preview_text.setReadOnly(True)
                self.preview_text.setStyleSheet('font-size: 12pt; font-family: Segoe UI, Arial, sans-serif; background: #f8f8f8; padding: 8px;')
                viewer_layout.addWidget(self.preview_text)

                # --- Keyboard shortcuts ---
                self.table.installEventFilter(self)
                self.shortcut_actions = {
                    (Qt.ControlModifier, Qt.Key_S): self.save_csv,
                    (Qt.NoModifier, Qt.Key_Delete): self.delete_selected,
                    (Qt.ControlModifier, Qt.Key_F): lambda: self.filter_edit.setFocus(),
                }

            def eventFilter(self, obj, event):
                if obj is self.table and event.type() == QEvent.KeyPress:
                    key = event.key()
                    mods = event.modifiers()
                    for (mod, k), action in self.shortcut_actions.items():
                        if mods == mod and key == k:
                            action()
                            return True
                return super().eventFilter(obj, event)

            def load_csv(self):
                file_path, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv)')
                if not file_path:
                    return
                try:
                    with open(file_path, newline='', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        rows = list(reader)
                        if not rows:
                            QMessageBox.critical(self, 'Error', 'CSV file is empty.')
                            return
                        header = rows[0]
                        data = rows[1:]
                    self.csv_data['header'] = header
                    self.csv_data['rows'] = data
                    self.csv_data['file_path'] = file_path
                    self.update_table()
                    self.status_bar.showMessage(f"Loaded {file_path} ({len(data)} items)")
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f'Failed to load CSV: {e}')
                    self.status_bar.showMessage('Failed to load CSV.')

            def save_csv(self):
                if not self.csv_data['file_path'] or not self.csv_data['header']:
                    QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
                    return
                try:
                    with open(self.csv_data['file_path'], 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(self.csv_data['header'])
                        for row in self.csv_data['rows']:
                            writer.writerow(row)
                    self.status_bar.showMessage('CSV saved.')
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f'Failed to save CSV: {e}')
                    self.status_bar.showMessage('Failed to save CSV.')

            def update_table(self):
                header = self.csv_data.get('header', [])
                rows = self.csv_data.get('rows', [])
                query = self.filter_edit.text().strip().lower()
                if query:
                    filtered = [row for row in rows if any(query in str(cell).lower() for cell in row)]
                else:
                    filtered = rows
                self.filtered_rows = filtered
                self.table.blockSignals(True)
                self.table.setColumnCount(len(header))
                self.table.setHorizontalHeaderLabels(header)
                self.table.setRowCount(len(filtered))
                for i, row in enumerate(filtered):
                    for j, val in enumerate(row):
                        item = QTableWidgetItem(val)
                        self.table.setItem(i, j, item)
                self.table.blockSignals(False)
                self.status_bar.showMessage(f"{len(filtered)} / {len(rows)} items shown.")
                self.update_preview()

            def update_preview(self):
                selected = self.table.selectedItems()
                if not selected or not self.filtered_rows:
                    self.preview_text.setPlainText('')
                    return
                row_idx = selected[0].row()
                row = self.filtered_rows[row_idx]
                text_idx = None
                for i, col in enumerate(self.csv_data['header']):
                    if col.strip().lower() == 'text':
                        text_idx = i
                        break
                if text_idx is not None and row[text_idx]:
                    self.preview_text.setPlainText(row[text_idx])
                else:
                    self.preview_text.setPlainText('')

            def on_table_item_changed(self, item):
                # Update the underlying data when a cell is edited
                row_idx = item.row()
                col_idx = item.column()
                if 0 <= row_idx < len(self.filtered_rows):
                    # Find the actual row in self.csv_data['rows']
                    actual_row = self.filtered_rows[row_idx]
                    actual_idx = self.csv_data['rows'].index(actual_row)
                    self.csv_data['rows'][actual_idx][col_idx] = item.text()
                    self.status_bar.showMessage('Cell updated.')

            def delete_selected(self):
                selected = self.table.selectionModel().selectedRows()
                if not selected:
                    return
                idxs = sorted([s.row() for s in selected], reverse=True)
                count = 0
                for idx in idxs:
                    if 0 <= idx < len(self.filtered_rows):
                        actual_row = self.filtered_rows[idx]
                        if actual_row in self.csv_data['rows']:
                            self.csv_data['rows'].remove(actual_row)
                            count += 1
                self.update_table()
                self.status_bar.showMessage(f"Deleted {count} item(s).")

            def add_potions(self):
                if not self.csv_data['header']:
                    QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
                    return
                n = self.num_potions_spin.value()
                try:
                    with open('magic items.csv', newline='', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        magic_header = next(reader)
                        magic_data = list(reader)
                except Exception:
                    QMessageBox.critical(self, 'Error', 'Could not load magic items.csv.')
                    return
                # Find column indices by header
                def col_idx(col_name):
                    for i, col in enumerate(magic_header):
                        if col.strip().lower() == col_name:
                            return i
                    return None
                type_idx = col_idx('type') or 4
                rarity_idx = col_idx('rarity') or 3
                name_idx = col_idx('name') or 0
                attune_idx = col_idx('attunement') or 5
                text_idx = col_idx('text') or 11
                potions = [row for row in magic_data if type_idx < len(row) and 'potion' in row[type_idx].lower() and rarity_idx < len(row) and row[rarity_idx].strip().lower() in ['common', 'uncommon']]
                if not potions:
                    QMessageBox.warning(self, 'Warning', 'No potions found in magic items.csv.')
                    return
                chosen = random.sample(potions, min(n, len(potions)))
                for row in chosen:
                    new_row = []
                    rarity_val = row[rarity_idx].strip().lower() if rarity_idx < len(row) else ''
                    for col in self.csv_data['header']:
                        col_l = col.strip().lower()
                        if col_l == 'name':
                            new_row.append(row[name_idx] if name_idx < len(row) else '')
                        elif col_l == 'rarity':
                            new_row.append(row[rarity_idx] if rarity_idx < len(row) else '')
                        elif col_l == 'type':
                            new_row.append(row[type_idx] if type_idx < len(row) and row[type_idx].strip() else 'Unknown')
                        elif col_l == 'text':
                            new_row.append(row[text_idx] if text_idx < len(row) else '')
                        elif col_l == 'value':
                            new_row.append(str(get_item_value(rarity_val)))
                        elif col_l == 'attunement':
                            new_row.append(row[attune_idx] if attune_idx < len(row) else '')
                        else:
                            new_row.append('')
                    self.csv_data['rows'].append(new_row)
                self.update_table()
                self.status_bar.showMessage(f'Added {len(chosen)} potion(s).')

            def add_gemstones(self):
                if not self.csv_data['header']:
                    QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
                    return
                target_value = self.gem_value_spin.value()
                min_total = int(target_value * 0.9)
                max_total = int(target_value * 1.1)
                total = 0
                gems = []
                tries = 0
                import random
                while total < min_total and tries < 1000:
                    gem = random.choice(list(GEMSTONE_VALUE_LIST.keys()))
                    quality = random.choice(list(GEMSTONE_VALUE_LIST[gem].keys()))
                    value = GEMSTONE_VALUE_LIST[gem][quality]
                    if total + value > max_total:
                        tries += 1
                        continue
                    gems.append((gem, quality, value))
                    total += value
                    tries += 1
                if not gems:
                    QMessageBox.warning(self, 'Warning', 'Could not generate gemstones for value.')
                    return
                for gem, quality, value in gems:
                    row = ['Gemstone', quality, gem, str(value), '', f'{quality} {gem} ({value} gp)']
                    # Pad to match header
                    while len(row) < len(self.csv_data['header']):
                        row.append('')
                    self.csv_data['rows'].append(row)
                self.update_table()
                self.status_bar.showMessage(f'Added {len(gems)} gemstone(s) totaling {total} gp.')

            def fuzzy_match(self, query, candidates):
                matches = [c for c in candidates if query.lower() in c.lower()]
                if matches:
                    return matches[0]
                try:
                    import difflib
                    close = difflib.get_close_matches(query, candidates, n=1)
                    return close[0] if close else None
                except ImportError:
                    return None

            def add_item_by_rarity(self):
                if not self.csv_data['header']:
                    QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
                    return
                rarity = self.additem_rarity_combo.currentText().strip().lower()
                name_query = self.additem_name_edit.text().strip()
                try:
                    with open('magic items.csv', newline='', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        magic_header = next(reader)
                        magic_data = list(reader)
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f'Could not load magic items.csv: {e}')
                    return
                # Find column indices by header
                def col_idx(col_name):
                    for i, col in enumerate(magic_header):
                        if col.strip().lower() == col_name:
                            return i
                    return None
                name_idx = col_idx('name') or 0
                rarity_idx = col_idx('rarity') or 3
                type_idx = col_idx('type') or 4
                attune_idx = col_idx('attunement') or 5
                text_idx = col_idx('text') or 11
                pool = [row for row in magic_data if rarity_idx < len(row) and get_rarity(row, magic_header) == rarity]
                if not pool:
                    QMessageBox.warning(self, 'Warning', f'No items of rarity {rarity.title()} found.')
                    return
                if name_query:
                    names = [row[name_idx] for row in pool if name_idx < len(row)]
                    match = self.fuzzy_match(name_query, names)
                    if match:
                        row = next(row for row in pool if name_idx < len(row) and row[name_idx] == match)
                    else:
                        QMessageBox.warning(self, 'Warning', f'No item found matching "{name_query}".')
                        return
                else:
                    row = random.choice(pool)
                new_row = []
                rarity_val = row[rarity_idx].strip().lower() if rarity_idx < len(row) else ''
                for col in self.csv_data['header']:
                    col_l = col.strip().lower()
                    if col_l == 'name':
                        new_row.append(row[name_idx] if name_idx < len(row) else '')
                    elif col_l == 'rarity':
                        new_row.append(row[rarity_idx] if rarity_idx < len(row) else '')
                    elif col_l == 'type':
                        new_row.append(row[type_idx] if type_idx < len(row) and row[type_idx].strip() else 'Unknown')
                    elif col_l == 'text':
                        new_row.append(row[text_idx] if text_idx < len(row) else '')
                    elif col_l == 'value':
                        new_row.append(str(get_item_value(rarity_val)))
                    elif col_l == 'attunement':
                        new_row.append(row[attune_idx] if attune_idx < len(row) else '')
                    else:
                        new_row.append('')
                self.csv_data['rows'].append(new_row)
                self.update_table()
                self.status_bar.showMessage(f'Added item: {new_row[0]} ({rarity.title()})')

            def add_custom_item(self):
                if not self.csv_data['header']:
                    QMessageBox.warning(self, 'Warning', 'No CSV loaded.')
                    return
                name = self.custom_name_edit.text().strip()
                typ = self.custom_type_edit.text().strip()
                rarity = self.custom_rarity_combo.currentText().strip().lower()
                text = self.custom_text_edit.text().strip()
                value = self.custom_value_edit.text().strip()
                if not name or not typ or not rarity:
                    QMessageBox.warning(self, 'Warning', 'Name, Type, and Rarity are required.')
                    return
                row = []
                for col in self.csv_data['header']:
                    if col.strip().lower() == 'name':
                        row.append(name)
                    elif col.strip().lower() == 'type':
                        row.append(typ)
                    elif col.strip().lower() == 'rarity':
                        row.append(rarity)
                    elif col.strip().lower() == 'text':
                        row.append(text)
                    elif col.strip().lower() == 'value':
                        row.append(value)
                    else:
                        row.append('')
                self.csv_data['rows'].append(row)
                self.update_table()
                self.status_bar.showMessage(f'Added custom item: {name} ({rarity.title()})')

            def keyPressEvent(self, event):
                # Keyboard shortcuts: Ctrl+S (save), Delete (delete), Ctrl+F (focus filter)
                if event.matches(QKeySequence.Save):
                    self.save_csv()
                    event.accept()
                elif event.key() == Qt.Key_Delete:
                    self.delete_selected()
                    event.accept()
                elif event.matches(QKeySequence.Find):
                    self.filter_edit.setFocus()
                    event.accept()
                else:
                    super().keyPressEvent(event)

            def toggle_dark_mode(self, enabled):
                if enabled:
                    dark_stylesheet = """
                        QWidget { background: #232629; color: #e0e0e0; }
                        QTableWidget { background: #2b2b2b; color: #e0e0e0; alternate-background-color: #232629; }
                        QHeaderView::section { background: #232629; color: #e0e0e0; }
                        QLineEdit, QTextEdit { background: #232629; color: #e0e0e0; border: 1px solid #444; }
                        QPushButton { background: #353535; color: #e0e0e0; border: 1px solid #444; padding: 6px; }
                        QPushButton:checked { background: #444; }
                        QComboBox, QSpinBox { background: #232629; color: #e0e0e0; border: 1px solid #444; }
                        QStatusBar { background: #232629; color: #e0e0e0; }
                    """
                    self.setStyleSheet(dark_stylesheet)
                else:
                    self.setStyleSheet("")

            def make_collapsible_section(self, title, content_widget):
                # Returns a QWidget with a toggle button and collapsible content
                container = QWidget()
                layout = QVBoxLayout(container)
                layout.setContentsMargins(0, 0, 0, 0)
                toggle = QToolButton()
                toggle.setText(title)
                toggle.setCheckable(True)
                toggle.setChecked(False)
                toggle.setStyleSheet('QToolButton { font-weight: bold; font-size: 12pt; text-align: left; }')
                toggle.setToolButtonStyle(Qt.ToolButtonTextOnly)
                toggle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                frame = QFrame()
                frame.setFrameShape(QFrame.NoFrame)
                frame.setLayout(QVBoxLayout())
                frame.layout().addWidget(content_widget)
                frame.setVisible(False)
                def on_toggle(checked):
                    frame.setVisible(checked)
                toggle.toggled.connect(on_toggle)
                layout.addWidget(toggle)
                layout.addWidget(frame)
                return container

            def init_character_creator_tab(self):
                char_tab = QWidget()
                char_layout = QVBoxLayout()
                char_tab.setLayout(char_layout)

                # Initialize required attributes
                self.required_race_skills = 0
                self.allowed_race_skills = []
                self.required_class_skills = 0
                self.allowed_class_skills = []

                # --- Race Dropdown ---
                race_bar = QHBoxLayout()
                race_label = QLabel('Race:')
                self.race_combo = QComboBox()
                # Load races from races.csv and store full data for info display
                self.race_data = []
                races = []
                try:
                    with open('races.csv', 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            name = row['name'].strip()
                            if name:
                                races.append(name)
                                self.race_data.append(row)
                except Exception:
                    pass
                unique_races = sorted(set(races))
                self.race_combo.addItems(unique_races)
                race_bar.addWidget(race_label)
                race_bar.addWidget(self.race_combo)
                race_bar.addStretch()
                char_layout.addLayout(race_bar)

                # --- Race Info Display ---
                self.race_info_label = QLabel()
                self.race_info_label.setWordWrap(True)
                self.race_info_label.setStyleSheet('font-size: 11pt; background: #f8f8f8; padding: 8px; border: 1px solid #ccc;')
                race_scroll = QScrollArea()
                race_scroll.setWidgetResizable(True)
                race_scroll.setMinimumHeight(60)
                race_scroll.setMaximumHeight(200)
                race_scroll.setWidget(self.race_info_label)
                race_info_section = self.make_collapsible_section('Show Race Details', race_scroll)
                char_layout.addWidget(race_info_section)

                self.race_combo.currentTextChanged.connect(self.update_race_info)
                self.update_race_info(self.race_combo.currentText())

                # --- Background Dropdown ---
                bg_bar = QHBoxLayout()
                bg_label = QLabel('Background:')
                self.bg_combo = QComboBox()
                self.background_data = []
                backgrounds = []
                try:
                    with open('backgrounds.csv', 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            name = row['name'].strip()
                            if name:
                                backgrounds.append(name)
                                self.background_data.append(row)
                except Exception:
                    pass
                unique_bgs = sorted(set(backgrounds))
                self.bg_combo.addItems(unique_bgs)
                bg_bar.addWidget(bg_label)
                bg_bar.addWidget(self.bg_combo)
                bg_bar.addStretch()
                char_layout.addLayout(bg_bar)

                # --- Background Info Display ---
                self.bg_info_label = QLabel()
                self.bg_info_label.setWordWrap(True)
                self.bg_info_label.setStyleSheet('font-size: 11pt; background: #f8f8f8; padding: 8px; border: 1px solid #ccc;')
                bg_scroll = QScrollArea()
                bg_scroll.setWidgetResizable(True)
                bg_scroll.setMinimumHeight(60)
                bg_scroll.setMaximumHeight(200)
                bg_scroll.setWidget(self.bg_info_label)
                bg_info_section = self.make_collapsible_section('Show Background Details', bg_scroll)
                char_layout.addWidget(bg_info_section)

                self.bg_combo.currentTextChanged.connect(self.update_bg_info)
                self.update_bg_info(self.bg_combo.currentText())

                # --- Class Dropdown ---
                class_bar = QHBoxLayout()
                class_label = QLabel('Class:')
                self.class_combo = QComboBox()
                import json
                self.class_data = []
                classes = []
                try:
                    with open('classes.json', 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for entry in data.get('classes', []):
                            name = entry.get('name', '').strip()
                            if name:
                                classes.append(name)
                                self.class_data.append(entry)
                except Exception:
                    pass
                unique_classes = sorted(set(classes))
                self.class_combo.addItems(unique_classes)
                class_bar.addWidget(class_label)
                class_bar.addWidget(self.class_combo)
                class_bar.addStretch()
                char_layout.addLayout(class_bar)

                # --- Class Info Display ---
                self.class_info_label = QLabel()
                self.class_info_label.setWordWrap(True)
                self.class_info_label.setStyleSheet('font-size: 12pt; background: #f8f8f8; padding: 10px; border: 2px solid #888;')
                # Put class info label in a scroll area
                class_scroll = QScrollArea()
                class_scroll.setWidgetResizable(True)
                class_scroll.setMinimumHeight(200)
                class_scroll.setMaximumHeight(500)
                class_scroll.setWidget(self.class_info_label)
                class_info_section = self.make_collapsible_section('Show Class Details', class_scroll)
                # Add class section with stretch to make it dominant
                char_layout.addWidget(class_info_section, stretch=2)

                self.class_combo.currentTextChanged.connect(self.update_class_info)
                self.update_class_info(self.class_combo.currentText())

                # --- Stat Generation Section ---
                stat_gen_bar = QHBoxLayout()
                stat_label = QLabel('Stat Generation:')
                stat_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
                stat_gen_bar.addWidget(stat_label)

                # --- Stat Section (Unified Row per Stat) ---
                stat_names = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']
                stat_grid = QGridLayout()
                stat_grid.addWidget(QLabel('<b>Stat</b>'), 0, 0)
                stat_grid.addWidget(QLabel('<b>Value</b>'), 0, 1)
                stat_grid.addWidget(QLabel('<b>Score Increases</b>'), 0, 2)
                stat_grid.addWidget(QLabel('<b>Total</b>'), 0, 3)
                self.stat_spinboxes = []
                self.stat_increase_labels = []
                self.stat_total_labels = []
                self.stat_combos = []
                for i, stat in enumerate(stat_names):
                    stat_grid.addWidget(QLabel(stat), i+1, 0)
                    spin = QSpinBox()
                    spin.setRange(1, 20)
                    spin.setValue(10)
                    stat_grid.addWidget(spin, i+1, 1)
                    inc_label = QLabel('0')
                    inc_label.setMinimumWidth(24)
                    inc_label.setAlignment(Qt.AlignLeft)
                    stat_grid.addWidget(inc_label, i+1, 2)
                    total_label = QLabel('10')
                    total_label.setMinimumWidth(24)
                    total_label.setAlignment(Qt.AlignLeft)
                    stat_grid.addWidget(total_label, i+1, 3)
                    self.stat_spinboxes.append(spin)
                    self.stat_increase_labels.append(inc_label)
                    self.stat_total_labels.append(total_label)
                stat_grid.setHorizontalSpacing(12)
                stat_grid.setVerticalSpacing(4)

                # --- ASI Source Selection (Radio Buttons) ---
                from PySide6.QtWidgets import QRadioButton, QButtonGroup
                asi_radio_bar = QHBoxLayout()
                asi_radio_bar.addWidget(QLabel('Apply Ability Score Increases from:'))
                self.asi_group = QButtonGroup()
                self.asi_race_radio = QRadioButton('Race')
                self.asi_bg_radio = QRadioButton('Background')
                self.asi_both_radio = QRadioButton('Both')
                self.asi_neither_radio = QRadioButton('Neither')
                self.asi_race_radio.setChecked(True)
                self.asi_group.addButton(self.asi_race_radio, 0)
                self.asi_group.addButton(self.asi_bg_radio, 1)
                self.asi_group.addButton(self.asi_both_radio, 2)
                self.asi_group.addButton(self.asi_neither_radio, 3)
                asi_radio_bar.addWidget(self.asi_race_radio)
                asi_radio_bar.addWidget(self.asi_bg_radio)
                asi_radio_bar.addWidget(self.asi_both_radio)
                asi_radio_bar.addWidget(self.asi_neither_radio)
                asi_radio_bar.addStretch()
                self.asi_group.buttonClicked.connect(self.update_stat_totals)
                self.asi_group.buttonClicked.connect(self.on_asi_source_changed)

                # --- Stat Generation Parameters ---
                param_bar = QHBoxLayout()
                self.lowest_stat_min_spin = QSpinBox()
                self.lowest_stat_min_spin.setRange(1, 20)
                self.lowest_stat_min_spin.setValue(7)
                param_bar.addWidget(QLabel('Lowest Stat Min:'))
                param_bar.addWidget(self.lowest_stat_min_spin)
                self.lowest_stat_max_spin = QSpinBox()
                self.lowest_stat_max_spin.setRange(1, 20)
                self.lowest_stat_max_spin.setValue(9)
                param_bar.addWidget(QLabel('Lowest Stat Max:'))
                param_bar.addWidget(self.lowest_stat_max_spin)
                self.highest_stat_min_spin = QSpinBox()
                self.highest_stat_min_spin.setRange(1, 20)
                self.highest_stat_min_spin.setValue(15)
                param_bar.addWidget(QLabel('Highest Stat Min:'))
                param_bar.addWidget(self.highest_stat_min_spin)
                self.highest_stat_max_spin = QSpinBox()
                self.highest_stat_max_spin.setRange(1, 20)
                self.highest_stat_max_spin.setValue(17)
                param_bar.addWidget(QLabel('Highest Stat Max:'))
                param_bar.addWidget(self.highest_stat_max_spin)
                self.average_min_spin = QDoubleSpinBox()
                self.average_min_spin.setRange(1, 20)
                self.average_min_spin.setDecimals(2)
                self.average_min_spin.setValue(12)
                param_bar.addWidget(QLabel('Average Min:'))
                param_bar.addWidget(self.average_min_spin)
                self.average_max_spin = QDoubleSpinBox()
                self.average_max_spin.setRange(1, 20)
                self.average_max_spin.setDecimals(2)
                self.average_max_spin.setValue(13.50)
                param_bar.addWidget(QLabel('Average Max:'))
                param_bar.addWidget(self.average_max_spin)
                param_bar.addStretch()

                # --- Generate Button ---
                stat_controls_bar = QHBoxLayout()
                gen_btn = QPushButton('Generate Stats')
                gen_btn.clicked.connect(self.generate_stats)
                stat_controls_bar.addWidget(gen_btn)
                stat_controls_bar.addStretch()

                # Add to layout
                char_layout.addLayout(race_bar)
                char_layout.addWidget(race_info_section)
                char_layout.addLayout(bg_bar)
                char_layout.addWidget(bg_info_section)
                char_layout.addLayout(class_bar)
                char_layout.addWidget(class_info_section)
                char_layout.addLayout(asi_radio_bar)
                char_layout.addLayout(stat_grid)
                char_layout.addLayout(stat_controls_bar)
                char_layout.addLayout(param_bar)        # --- Character Info Inputs (Name, Alignment, Player Name) ---
                info_bar = QHBoxLayout()
                info_bar.addWidget(QLabel('Character Name:'))
                self.char_name_edit = QLineEdit()
                info_bar.addWidget(self.char_name_edit)
                info_bar.addWidget(QLabel('Alignment:'))
                self.alignment_combo = QComboBox()
                self.alignment_combo.addItems([
                    'Lawful Good', 'Neutral Good', 'Chaotic Good',
                    'Lawful Neutral', 'True Neutral', 'Chaotic Neutral',