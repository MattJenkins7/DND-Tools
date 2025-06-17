import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QTextEdit,
    QFileDialog, QMessageBox, QSpinBox, QDoubleSpinBox, QStatusBar, QAbstractItemView, QHeaderView,
    QScrollArea, QToolButton, QSizePolicy, QFrame, QListWidget, QCheckBox
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
        char_layout.addLayout(param_bar)

        # --- Character Info Inputs (Name, Alignment, Player Name) ---
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
        self.asi_group.buttonClicked.connect(self.on_asi_source_changed)

        # --- Wrap the whole tab in a scroll area ---
        outer_scroll = QScrollArea()
        outer_scroll.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(char_layout)
        outer_scroll.setWidget(container)
        self.tabs.addTab(outer_scroll, 'Character Creator')

        # --- Skills Generation Section ---
        skill_gen_bar = QHBoxLayout()
        skill_label = QLabel('Skill Generation:')
        skill_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
        skill_gen_bar.addWidget(skill_label)        # --- Proficiency Selection Section (with dropdowns for allowed skills) ---
        self.proficiency_widget = QWidget()
        self.proficiency_layout = QVBoxLayout()
        self.proficiency_widget.setLayout(self.proficiency_layout)
        self.proficiency_dropdowns = []
        # Place the proficiency_widget directly in the character layout, after skills generation
        char_layout.addWidget(QLabel('Race Skill Proficiencies:'))
        char_layout.addWidget(self.proficiency_widget)

        def update_proficiency_dropdowns(race_name):
            # Clear old dropdowns
            for dropdown in self.proficiency_dropdowns:
                self.proficiency_layout.removeWidget(dropdown)
                dropdown.deleteLater()
            self.proficiency_dropdowns.clear()
            self.required_race_skills = 0
            self.allowed_race_skills = []
            if not race_name or race_name == 'None':
                return
            for row in self.race_data:
                if row['name'].strip() == race_name:
                    prof_choice = row.get('SkillProfToChooseFrom/Choose', '').strip()
                    if prof_choice and prof_choice != '/0':
                        if '/' in prof_choice:
                            skills_part, num_part = prof_choice.rsplit('/', 1)
                            try:
                                num_to_choose = int(num_part)
                            except ValueError:
                                num_to_choose = 0
                            skills = [s.strip() for s in skills_part.split(',') if s.strip()]
                            self.required_race_skills = num_to_choose
                            self.allowed_race_skills = skills
                            # Create dropdowns equal to the number of skills to choose
                            for i in range(num_to_choose):
                                dropdown = QComboBox()
                                dropdown.addItem("-- Select Skill --")
                                dropdown.addItems(skills)
                                dropdown.currentTextChanged.connect(prevent_duplicate_selections)
                                self.proficiency_layout.addWidget(dropdown)
                                self.proficiency_dropdowns.append(dropdown)
                        else:
                            # Fixed skill, show as disabled dropdown with only that option
                            dropdown = QComboBox()
                            dropdown.addItem(prof_choice)
                            dropdown.setEnabled(False)
                            self.proficiency_layout.addWidget(dropdown)
                            self.proficiency_dropdowns.append(dropdown)
                            self.required_race_skills = 1
                            self.allowed_race_skills = [prof_choice]
                    break

        def prevent_duplicate_selections():
            # Prevent the same skill from being selected in multiple dropdowns
            selected_skills = [dropdown.currentText() for dropdown in self.proficiency_dropdowns 
                             if dropdown.currentText() != "-- Select Skill --"]
            for dropdown in self.proficiency_dropdowns:
                current_selection = dropdown.currentText()
                dropdown.blockSignals(True)
                dropdown.clear()
                dropdown.addItem("-- Select Skill --")
                # Add skills that aren't selected elsewhere, or the current selection
                for skill in self.allowed_race_skills:
                    if skill not in selected_skills or skill == current_selection:
                        dropdown.addItem(skill)
                dropdown.setCurrentText(current_selection)
                dropdown.blockSignals(False)

        def get_selected_race_skills():
            return [dropdown.currentText() for dropdown in self.proficiency_dropdowns 
                   if dropdown.currentText() != "-- Select Skill --"]

        self.update_proficiency_dropdowns = update_proficiency_dropdowns
        self.get_selected_race_skills = get_selected_race_skills
        self.race_combo.currentTextChanged.connect(self.update_proficiency_dropdowns)
        self.update_proficiency_dropdowns(self.race_combo.currentText())

        # --- Class Skill Proficiencies Section ---
        self.class_proficiency_widget = QWidget()
        self.class_proficiency_layout = QVBoxLayout()
        self.class_proficiency_widget.setLayout(self.class_proficiency_layout)
        self.class_proficiency_dropdowns = []
        char_layout.addWidget(QLabel('Class Skill Proficiencies:'))
        char_layout.addWidget(self.class_proficiency_widget)

        def update_class_proficiency_dropdowns(class_name):
            # Clear old dropdowns
            for dropdown in self.class_proficiency_dropdowns:
                self.class_proficiency_layout.removeWidget(dropdown)
                dropdown.deleteLater()
            self.class_proficiency_dropdowns.clear()
            self.required_class_skills = 0
            self.allowed_class_skills = []
            if not class_name or class_name == 'None':
                print('[DEBUG] No class selected for class proficiencies')
                return
            for entry in self.class_data:
                if entry.get('name', '').strip() == class_name:
                    proficiencies = entry.get('proficiencies', {})
                    skills_field = proficiencies.get('skills', [])
                    print(f'[DEBUG] Found class: {class_name}, skills_field: {skills_field}')
                    if skills_field and isinstance(skills_field, list) and len(skills_field) > 1:
                        try:
                            num_to_choose = int(skills_field[0])
                        except Exception:
                            num_to_choose = 2 # fallback to 2 if not valid
                        skills = [s for s in skills_field[1:]]
                        self.required_class_skills = num_to_choose
                        self.allowed_class_skills = skills
                        for i in range(num_to_choose):
                            dropdown = QComboBox()
                            dropdown.addItem('-- Select Skill --')
                            dropdown.addItems(skills)
                            dropdown.currentTextChanged.connect(prevent_duplicate_class_selections)
                            self.class_proficiency_layout.addWidget(dropdown)
                            self.class_proficiency_dropdowns.append(dropdown)
                        print(f'[DEBUG] Created {num_to_choose} class skill dropdowns with options: {skills}')
                    else:
                        print(f'[DEBUG] No valid skills_field for class: {class_name}')
                    break

        def prevent_duplicate_class_selections():
            selected_skills = [dropdown.currentText() for dropdown in self.class_proficiency_dropdowns 
                             if dropdown.currentText() != '-- Select Skill --']
            for dropdown in self.class_proficiency_dropdowns:
                current_selection = dropdown.currentText()
                dropdown.blockSignals(True)
                dropdown.clear()
                dropdown.addItem('-- Select Skill --')
                for skill in self.allowed_class_skills:
                    if skill not in selected_skills or skill == current_selection:
                        dropdown.addItem(skill)
                dropdown.setCurrentText(current_selection)
                dropdown.blockSignals(False)

        def get_selected_class_skills():
            return [dropdown.currentText() for dropdown in self.class_proficiency_dropdowns 
                   if dropdown.currentText() != '-- Select Skill --']

        self.update_class_proficiency_dropdowns = update_class_proficiency_dropdowns
        self.get_selected_class_skills = get_selected_class_skills
        self.class_combo.currentTextChanged.connect(self.update_class_proficiency_dropdowns)
        # Call after UI is fully constructed
        QTimer.singleShot(0, lambda: self.update_class_proficiency_dropdowns(self.class_combo.currentText()))

        # --- Export to PDF Button (moved to bottom) ---
        export_pdf_btn = QPushButton('Export to PDF')
        export_pdf_btn.clicked.connect(self.export_character_to_pdf)
        char_layout.addWidget(export_pdf_btn)

    def update_stat_totals(self):
        stat_names = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']
        values = [spin.value() for spin in self.stat_spinboxes]
        race = self.asi_race_radio.isChecked() or self.asi_both_radio.isChecked()
        background = self.asi_bg_radio.isChecked() or self.asi_both_radio.isChecked()
        asi = {k: 0 for k in stat_names}
        if race:
            race_name = self.race_combo.currentText()
            for row in self.race_data:
                if row['name'].strip() == race_name:
                    asi_str = row.get('Ability Score Increase', '')
                    asi_result, _ = self.parse_asi_string_with_prompt(asi_str, 'Race')
                    for k, v in asi_result.items():
                        asi[k] += v
                    break
        if background:
            bg_name = self.bg_combo.currentText()
            for row in self.background_data:
                if row['name'].strip() == bg_name:
                    asi_str = row.get('ability', '')
                    asi_result, _ = self.parse_asi_string_with_prompt(asi_str, 'Background')
                    for k, v in asi_result.items():
                        asi[k] += v
                    break
        for i, stat in enumerate(stat_names):
            self.stat_increase_labels[i].setText(str(asi.get(stat, 0)))
            self.stat_total_labels[i].setText(str(values[i] + asi.get(stat, 0)))

    def on_asi_source_changed(self):
        # Only prompt for ASI choices when the user changes the ASI source (radio buttons)
        stat_names = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']
        race = self.asi_race_radio.isChecked() or self.asi_both_radio.isChecked()
        background = self.asi_bg_radio.isChecked() or self.asi_both_radio.isChecked()
        asi = {k: 0 for k in stat_names}
        asi_prompts = []
        if race:
            race_name = self.race_combo.currentText()
            for row in self.race_data:
                if row['name'].strip() == race_name:
                    asi_str = row.get('Ability Score Increase', '')
                    asi_result, prompt = self.parse_asi_string_with_prompt(asi_str, 'Race')
                    for k, v in asi_result.items():
                        asi[k] += v
                    if prompt:
                        asi_prompts.append(prompt)
                    break
        if background:
            bg_name = self.bg_combo.currentText()
            for row in self.background_data:
                if row['name'].strip() == bg_name:
                    asi_str = row.get('ability', '')
                    asi_result, prompt = self.parse_asi_string_with_prompt(asi_str, 'Background')
                    for k, v in asi_result.items():
                        asi[k] += v
                    if prompt:
                        asi_prompts.append(prompt)
                    break
        if asi_prompts:
            asi_choices = self.prompt_asi_choices(asi_prompts)
            for k, v in asi_choices.items():
                asi[k] += v
        values = [spin.value() for spin in self.stat_spinboxes]
        for i, stat in enumerate(stat_names):
            self.stat_increase_labels[i].setText(str(asi.get(stat, 0)))
            self.stat_total_labels[i].setText(str(values[i] + asi.get(stat, 0)))

    def generate_stats(self):
        import random
        lowest_stat_min = self.lowest_stat_min_spin.value()
        lowest_stat_max = self.lowest_stat_max_spin.value()
        highest_stat_min = self.highest_stat_min_spin.value()
        highest_stat_max = self.highest_stat_max_spin.value()
        average_min = self.average_min_spin.value()
        average_max = self.average_max_spin.value()
        x = 4
        y = 6
        numbers = []
        tries = 0
        while True:
            numbers.clear()
            for j in range(y):
                # Standard 4d6 drop lowest
                rolls = [random.randint(1, 6) for _ in range(x)]
                total = sum(rolls) - min(rolls)
                numbers.append(total)
            tries += 1
            if (
                min(numbers) >= lowest_stat_min and
                max(numbers) <= highest_stat_max and
                min(numbers) <= lowest_stat_max and
                max(numbers) >= highest_stat_min and
                average_min <= sum(numbers) / y <= average_max
            ):
                break
            if tries > 10000:
                break
        for i, spin in enumerate(self.stat_spinboxes):
            spin.blockSignals(True)
            spin.setValue(numbers[i])
            spin.blockSignals(False)
        # Auto-select 'Neither' for ASI source after generating stats
        self.asi_neither_radio.setChecked(True)
        self.update_stat_totals()

    def handle_stat_swap(self, changed_idx, *args):
        changed_combo = self.stat_combos[changed_idx]
        selected_idx = changed_combo.currentIndex()
        # Check for duplicate in other combos
        for i, combo in enumerate(self.stat_combos):
            if i != changed_idx and combo.currentIndex() == selected_idx:
                # Swap the indices
                combo.blockSignals(True)
                changed_combo.blockSignals(True)
                combo.setCurrentIndex(self.stat_combos[changed_idx].property('lastIndex') if combo.property('lastIndex') is not None else changed_idx)
                changed_combo.setCurrentIndex(selected_idx)
                combo.blockSignals(False)
                changed_combo.blockSignals(False)
                break
        # Store the last index for each combo
        for i, combo in enumerate(self.stat_combos):
            combo.setProperty('lastIndex', combo.currentIndex())

    def update_stat_dropdowns(self):
        pass  # No disabling needed anymore

    def update_race_info(self, race_name):
        # Find the first matching race row
        for row in self.race_data:
            if row['name'].strip() == race_name:
                info = []
                for key, val in row.items():
                    if key is not None and val and key != 'name':
                        if key.strip().lower() == 'features':
                            # Handle literal \n and real newlines
                            features = str(val).replace('\\n', '\n')  # Convert literal \n to real newline
                            features = features.replace('\r\n', '\n').replace('\r', '\n')
                            features = features.strip()
                            # Split on real newlines
                            feature_lines = [f for f in features.split('\n') if f.strip()]
                            features_html = '<br>'.join(f"• {f.strip()}" for f in feature_lines)
                            info.append(f"<b>{str(key).title().replace('_', ' ')}:</b><br>{features_html}")
                        else:
                            info.append(f"<b>{str(key).title().replace('_', ' ')}:</b> {val}")
                self.race_info_label.setText('<br>'.join(info))
                return
        self.race_info_label.setText('')

    def update_bg_info(self, bg_name):
        # Find the first matching background row
        for row in self.background_data:
            if row['name'].strip() == bg_name:
                info = []
                for key, val in row.items():
                    if key is not None and val and key != 'name':
                        info.append(f"<b>{str(key).title().replace('_', ' ')}:</b> {val}")
                self.bg_info_label.setText('<br>'.join(info))
                return
        self.bg_info_label.setText('')

    def update_class_info(self, class_name):
        # Find the first matching class row
        for row in self.class_data:
            if row['name'].strip() == class_name:
                info = []
                # Basic info
                if 'hit_die' in row:
                    info.append(f"<b>Hit Die:</b> {row['hit_die']}")
                if 'primary_abilities' in row:
                    abilities = ', '.join(row['primary_abilities'])
                    info.append(f"<b>Primary Abilities:</b> {abilities}")
                if 'subclass_pick_level' in row:
                    info.append(f"<b>Subclass Pick Level:</b> {row['subclass_pick_level']}")
                if 'caster_type' in row and row['caster_type'] != 'none':
                    info.append(f"<b>Caster Type:</b> {row['caster_type'].capitalize()}")
                # Features by level (names only)
                features = row.get('features', {})
                if features:
                    feature_lines = []
                    for lvl in sorted(features, key=lambda x: int(x)):
                        names = ', '.join(f["name"] for f in features[lvl] if "name" in f)
                        if names:
                            feature_lines.append(f"<b>Level {lvl}:</b> {names}")
                    if feature_lines:
                        info.append("<b>Features by Level:</b><br>" + '<br>'.join(feature_lines))
                # Subclasses
                subclasses = row.get('subclasses', [])
                if subclasses:
                    subclass_names = ', '.join(sc['name'] for sc in subclasses if 'name' in sc)
                    info.append(f"<b>Subclasses:</b> {subclass_names}")
                self.class_info_label.setText('<br>'.join(info))
                return
        self.class_info_label.setText('')

    def prompt_and_apply_asi(self):
        # Prompt user for source of ability score increases
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle('Apply Ability Score Increases')
        msg.setText('Apply ability score increases from:')
        race_btn = msg.addButton('Race', QMessageBox.ActionRole)
        bg_btn = msg.addButton('Background', QMessageBox.ActionRole)
        both_btn = msg.addButton('Both', QMessageBox.ActionRole)
        cancel_btn = msg.addButton('Cancel', QMessageBox.RejectRole)
        msg.exec()
        if msg.clickedButton() == race_btn:
            self.apply_asi(race=True, background=False)
        elif msg.clickedButton() == bg_btn:
            self.apply_asi(race=False, background=True)
        elif msg.clickedButton() == both_btn:
            self.apply_asi(race=True, background=True)
        else:
            return

    def apply_asi(self, race=True, background=True):
        stat_names = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']
        stat_values = [spin.value() for spin in self.stat_spinboxes]
        print(f"[DEBUG] Current stat values before ASI: {dict(zip(stat_names, stat_values))}")
        asi = {name: 0 for name in stat_names}
        # Parse race ASI
        if race:
            race_name = self.race_combo.currentText()
            print(f"[DEBUG] Selected race: {race_name}")
            for row in self.race_data:
                if row['name'].strip() == race_name:
                    # Use correct field name for races.csv
                    asi_str = row.get('Ability Score Increase', '')
                    print(f"[DEBUG] Race ASI string: {asi_str}")
                    asi_result, _ = self.parse_asi_string_with_prompt(asi_str, 'Race')
                    print(f"[DEBUG] Race ASI parsed: {asi_result}")
                    for k, v in asi_result.items():
                        asi[k] += v
                    break
        # Parse background ASI
        if background:
            bg_name = self.bg_combo.currentText()
            print(f"[DEBUG] Selected background: {bg_name}")
            for row in self.background_data:
                if row['name'].strip() == bg_name:
                    # Use correct field name for backgrounds.csv
                    asi_str = row.get('ability', '')
                    print(f"[DEBUG] Background ASI string: {asi_str}")
                    asi_result, _ = self.parse_asi_string_with_prompt(asi_str, 'Background')
                    print(f"[DEBUG] Background ASI parsed: {asi_result}")
                    for k, v in asi_result.items():
                        asi[k] += v
                    break
        # Add ASI to stats
        for i, stat in enumerate(stat_names):
            print(f"[DEBUG] Adding {asi.get(stat, 0)} to {stat} (was {stat_values[i]})")
            self.stat_spinboxes[i].setValue(stat_values[i] + asi.get(stat, 0))
        self.update_stat_totals()

    def parse_asi_string_with_prompt(self, asi_str, source_label):
        print(f"[DEBUG] Parsing ASI string: '{asi_str}' from {source_label}")
        """
        Returns: (asi_dict, prompt_dict or None)
        asi_dict: {stat: value} for direct assignments
        prompt_dict: { 'type': ..., 'source': ..., ... } for user input if needed
        """
        import re
        stat_names = {'STR': 'STR', 'DEX': 'DEX', 'CON': 'CON', 'WIS': 'WIS', 'INT': 'INT', 'CHA': 'CHA',
                      'STRENGTH': 'STR', 'DEXTERITY': 'DEX', 'CONSTITUTION': 'CON', 'WISDOM': 'WIS', 'INTELLIGENCE': 'INT', 'CHARISMA': 'CHA',
                      'CHA': 'CHA', 'CON': 'CON', 'WIS': 'WIS', 'INT': 'INT'}
        asi = {k: 0 for k in ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']}
        asi_str = asi_str.strip()
        if not asi_str:
            return asi, None
        # --- Minor issue 1 fix: handle multiple comma-separated bonuses for backgrounds ---
        # Direct assignments: e.g. "Cha +2, Dex +1" or "+1 DEX, +1 INT"
        # --- Fix: handle '+1 wis, +1 cha' and similar forms robustly ---
        # Accept forms like '+1 wis, +1 cha', 'wis +1, cha +1', etc.
        direct_pattern = r'([+-]?\d+)\s*(STR|DEX|CON|WIS|INT|CHA|STRENGTH|DEXTERITY|CONSTITUTION|WISDOM|INTELLIGENCE|CHARISMA)|' \
                        r'(STR|DEX|CON|WIS|INT|CHA|STRENGTH|DEXTERITY|CONSTITUTION|WISDOM|INTELLIGENCE|CHARISMA)\s*([+-]?\d+)'
        direct_matches = re.findall(direct_pattern, asi_str.upper())
        if direct_matches:
            for m in direct_matches:
                # m is a tuple of 4 elements, only one pair will be filled
                if m[0] and m[1]:
                    val, stat = m[0], m[1]
                elif m[2] and m[3]:
                    stat, val = m[2], m[3]
                else:
                    continue
                stat = stat_names.get(stat, stat)
                if stat in asi:
                    try:
                        asi[stat] += int(val)
                    except Exception:
                        pass
            if not re.search(r'choose|point|option|among|other|one of', asi_str, re.IGNORECASE):
                return asi, None
        # Handle choose/points/option/among/other/one of
        # Examples:
        #   "Choose any +2"
        #   "Choose any +2, Choose any other +1"
        #   "Choose one of: (a) Choose any +2; choose any other +1 (b) Choose three different +1"
        #   "3 points among Wis, Cha, Int"
        prompt = {'type': None, 'source': source_label, 'raw': asi_str}
        if re.search(r'choose one of', asi_str, re.IGNORECASE):
            prompt['type'] = 'points_among'
            prompt['points'] = 3
            prompt['allowed'] = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']
            return asi, prompt
        elif re.search(r'choose any', asi_str, re.IGNORECASE):
            prompt['type'] = 'choose_any'
            # e.g. "Choose any +2, Choose any other +1"
            choose_matches = re.findall(r'choose any[^\d+-]*([+-]?\d+)', asi_str, re.IGNORECASE)
            prompt['amounts'] = [int(x) for x in choose_matches]
            # Check for "other" for secondary pick
            if re.search(r'other', asi_str, re.IGNORECASE):
                prompt['other'] = True
        elif re.search(r'points among', asi_str, re.IGNORECASE):
            prompt['type'] = 'points_among'
            pts = re.search(r'(\d+)\s*points?', asi_str)
            if pts:
                prompt['points'] = int(pts.group(1))
            allowed_stats = re.findall(r'(STR|DEX|CON|WIS|INT|CHA|STRENGTH|DEXTERITY|CONSTITUTION|WISDOM|INTELLIGENCE|CHARISMA)', asi_str.upper())
            prompt['allowed'] = list({stat_names.get(s, s) for s in allowed_stats})
        elif re.search(r'choose any', asi_str, re.IGNORECASE):
            prompt['type'] = 'choose_any'
            # fallback
        else:
            prompt['type'] = 'unknown'
        return asi, prompt

    def prompt_asi_choices(self, asi_prompts):
        # For each prompt, show a dialog to the user to select stats and distribution
        # Returns a dict {stat: value}
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem
        stat_names = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']
        asi_result = {k: 0 for k in stat_names}
        for prompt in asi_prompts:
            dlg = QDialog()
            dlg.setWindowTitle(f"Select Ability Score Increases ({prompt['source']})")
            layout = QVBoxLayout()
            layout.addWidget(QLabel(f"{prompt['raw']}"))
            if prompt['type'] == 'choose_any':
                picks = []
                used = set()
                for idx, amt in enumerate(prompt.get('amounts', [])):
                    row = QHBoxLayout()
                    label = QLabel(f"Choose stat for +{amt}: ")
                    combo = QComboBox()
                    combo.addItems([s for s in stat_names if s not in used])
                    row.addWidget(label)
                    row.addWidget(combo)
                    layout.addLayout(row)
                    picks.append((combo, amt))
                    def on_change(idx=idx):
                        # Update other combos to prevent duplicate selection
                        selected = [c.currentText() for c, _ in picks]
                        for i, (c, _) in enumerate(picks):
                            c.blockSignals(True)
                            c.clear()
                            c.addItems([s for s in stat_names if s not in selected or s == selected[i]])
                            c.setCurrentText(selected[i])
                            c.blockSignals(False)
                    combo.currentIndexChanged.connect(on_change)
                btn = QPushButton('OK')
                btn.clicked.connect(dlg.accept)
                layout.addWidget(btn)
                dlg.setLayout(layout)
                dlg.exec()
                for c, amt in picks:
                    asi_result[c.currentText()] += amt
            elif prompt['type'] == 'points_among':
                allowed = prompt.get('allowed', stat_names)
                points = prompt.get('points', 3)
                spinboxes = []
                row = QHBoxLayout()
                row.addWidget(QLabel(f"Distribute {points} points among: "))
                for stat in allowed:
                    spin = QSpinBox()
                    spin.setRange(0, points)
                    spin.setValue(0)
                    row.addWidget(QLabel(stat))
                    row.addWidget(spin)
                    spinboxes.append((stat, spin))
                layout.addLayout(row)
                btn = QPushButton('OK')
                layout.addWidget(btn)
                def accept_if_valid():
                    total = sum(spin.value() for _, spin in spinboxes)
                    if total == points:
                        dlg.accept()
                btn.clicked.connect(accept_if_valid)
                dlg.setLayout(layout)
                dlg.exec()
                for stat, spin in spinboxes:
                    asi_result[stat] += spin.value()
            elif prompt['type'] == 'choose_one_of':
                # Let user pick one option, then recursively prompt for that
                combo = QComboBox()
                combo.addItems(prompt.get('options', []))
                layout.addWidget(QLabel('Choose one option:'))
                layout.addWidget(combo)
                btn = QPushButton('OK')
                btn.clicked.connect(dlg.accept)
                layout.addWidget(btn)
                dlg.setLayout(layout)
                dlg.exec()
                chosen = combo.currentText()
                # Recursively parse and prompt for the chosen option
                asi_sub, subprompt = self.parse_asi_string_with_prompt(chosen, prompt['source'])
                for k, v in asi_sub.items():
                    asi_result[k] += v
                if subprompt:
                    subresult = self.prompt_asi_choices([subprompt])
                    for k, v in subresult.items():
                        asi_result[k] += v
            else:
                # fallback: do nothing
                pass
        return asi_result    
    
    def export_character_to_pdf(self):
        import re # Ensure re module is available in this scope
        # Check that the required number of race skill proficiencies are selected
        selected_skills = self.get_selected_race_skills()
        if self.required_race_skills and len(selected_skills) < self.required_race_skills:
            QMessageBox.critical(self, 'Error', f'Please select {self.required_race_skills} skill proficiency(ies) for your race before exporting.')
            return
        
        try:
            from pdfrw import PdfReader, PdfWriter
        except ImportError:
            QMessageBox.critical(self, 'Error', 'pdfrw is not installed. Please run: pip install pdfrw')
            return
        # Gather data from UI
        char_name = self.char_name_edit.text().strip() or 'Unnamed'
        alignment = self.alignment_combo.currentText()
        player_name = self.player_name_edit.text().strip()
        class_name = self.class_combo.currentText()
        level = self.level_spin.value()
        background = self.bg_combo.currentText()
        race = self.race_combo.currentText()
        # Example stat extraction
        stats = {stat: self.stat_spinboxes[i].value() for i, stat in enumerate(['STR','DEX','CON','WIS','INT','CHA'])}
        # Calculate modifiers
        def ability_mod(score):
            # D&D 5e: (score - 10) // 2
            return (score - 10) // 2
        mods = {stat: ability_mod(val) for stat, val in stats.items()}
        # Gather features for Features and Traits and AttacksSpellcasting
        attack_keywords = ['attack', 'strike', 'weapon', 'melee', 'ranged', 'shoot', 'hit']
        def is_attack_feature(text):
            t = text.lower()
            return any(word in t for word in attack_keywords)
        race_features = []
        race_attacks = []
        for row in self.race_data:
            if row['name'].strip() == race:
                for key, val in row.items():
                    if key and val and key.strip().lower() == 'features':
                        features = str(val).replace('\\\\n', '\\n').replace('\\r\\n', '\\n').replace('\\r', '\\n').strip()
                        for f in [f.strip() for f in features.split('\\n') if f.strip()]:
                            if is_attack_feature(f):
                                race_attacks.append(f)
                            else:
                                race_features.append(f)
                        break
        bg_features = []
        bg_attacks = []
        # Load feats data
        feats_data = []
        try:
            with open('feats.csv', 'r', encoding='utf-8') as f_feats:
                reader_feats = csv.DictReader(f_feats)
                feats_data = list(reader_feats)
        except Exception as e:
            print(f"Error loading feats.csv: {e}") # Or handle more gracefully

        for row in self.background_data:
            if row['name'].strip() == background:
                print(f"[DEBUG] Selected background for PDF export: {background}") # DEBUG
                for key, val in row.items():
                    if key and val and key.strip().lower() == 'description':
                        description_text = str(val).replace('\\\\n', '\\n').replace('\\r\\n', '\\n').replace('\\r', '\\n').strip()
                        print(f"[DEBUG] Raw background description text: '{description_text}'") # DEBUG
                        description_lines = [line.strip() for line in description_text.split('\\n') if line.strip()]
                        feat_to_add = None
                        feat_description_to_add = ""

                        for line in description_lines:
                            print(f"[DEBUG] Processing line: '{line}'") # DEBUG
                            # MODIFIED: Check if "origin feat:" is IN the line, not just at the start
                            if "origin feat:" in line.lower():
                                print(f"[DEBUG] Line CONTAINS 'origin feat:': '{line}'") # DEBUG
                                # Corrected regex
                                feat_name_match = re.search(r"origin feat: *\\*?([^\\*]+)\\*?", line, re.IGNORECASE)
                                if feat_name_match:
                                    feat_to_add = feat_name_match.group(1).strip()
                                    print(f"[DEBUG] Regex matched. Extracted feat_to_add: '{feat_to_add}'") # DEBUG
                                    
                                    feat_description_to_add = "" # Reset for current feat
                                    for feat_row in feats_data:
                                        if feat_row.get('Feat', '').strip().lower() == feat_to_add.lower():
                                            feat_description_to_add = feat_row.get('Description', '').strip()
                                            print(f"[DEBUG] Found matching feat in feats.csv. Description: '{feat_description_to_add}'") # DEBUG
                                            break
                                    else:
                                        print(f"[DEBUG] No matching feat found in feats.csv for '{feat_to_add}'") # DEBUG

                                    if feat_to_add: # This is the original debug location
                                        print(f"[DEBUG] Origin Feat Found (final check): {feat_to_add}")
                                        print(f"[DEBUG] Feat Description (final check): {feat_description_to_add}")
                                    else:
                                        print(f"[DEBUG] feat_to_add is None or empty after regex match and description lookup.") # DEBUG
                                else:
                                    print(f"[DEBUG] Regex did NOT match for line starting with 'origin feat:': '{line}'") # DEBUG
                                # Remove the "Origin Feat:" line from being added as a normal feature
                                continue # Skip adding this line to bg_features
                            
                            # Process other lines as regular features or attacks
                            if is_attack_feature(line):
                                bg_attacks.append(line)
                            else:
                                bg_features.append(line)
                        
                        if feat_to_add:
                            feat_text = f"Feat: {feat_to_add}"
                            if feat_description_to_add:
                                feat_text += f" - {feat_description_to_add}"
                            bg_features.append(feat_text) # Add the formatted feat string
                        break # Found background description
                break # Found background

        # CORRECTED LOGIC:
        # Iterate over copies of race_features and bg_features to find lines for ProficienciesLang
        # This ensures the original lists used for 'Features and Traits' are not modified.
        prof_lang_keywords = ["proficiency", "proficiencies", "language", "languages"]
        extracted_lines_for_prof_lang = []

        # Populate from a copy of race_features
        if 'race_features' in locals() and isinstance(race_features, list):
            for feature_line in list(race_features): # Iterate over a copy
                for keyword in prof_lang_keywords:
                    if keyword in feature_line.lower():
                        extracted_lines_for_prof_lang.append(feature_line)
                        break 
        
        # Populate from a copy of bg_features
        if 'bg_features' in locals() and isinstance(bg_features, list):
            for feature_line in list(bg_features): # Iterate over a copy
                for keyword in prof_lang_keywords:
                    if keyword in feature_line.lower(): # Check the whole line
                        extracted_lines_for_prof_lang.append(feature_line)
                        break
        # END CORRECTED LOGIC

        features_and_traits = ''
        if race_features:
            features_and_traits += f"Race Features ({race}):\n" + '\n\n'.join(race_features)
        if bg_features:
            if features_and_traits:
                features_and_traits += '\n\n'
            features_and_traits += f"Background Features ({background}):\n" + '\n\n'.join(bg_features)

        # Explicitly append extracted proficiency/language lines to features_and_traits
        if 'extracted_lines_for_prof_lang' in locals() and isinstance(extracted_lines_for_prof_lang, list) and extracted_lines_for_prof_lang:
            if features_and_traits:
                features_and_traits += '\n\n'
            # Clean each line before joining, similar to ProficienciesLang handling
            cleaned_extracted_lines = [str(line).strip() for line in extracted_lines_for_prof_lang]

        attacks_spellcasting = ''
        if race_attacks:
            attacks_spellcasting += f"Race Attacks ({race}):\n" + '\n\n'.join(race_attacks)
        if bg_attacks:
            if attacks_spellcasting:
                attacks_spellcasting += '\n\n'
            attacks_spellcasting += f"Background Attacks ({background}):\n" + '\n\n'.join(bg_attacks)
        # Map to PDF field names (expand coverage)
        # Gather languages from race
        race_languages = ''
        for row in self.race_data:
            if row['name'].strip() == race:
                for key, val in row.items():
                    if key and val and key.strip().lower() == 'languages':
                        race_languages = val
                        break        # Get selected race skill proficiencies
        selected_race_skills = self.get_selected_race_skills()

        # Get background skill proficiencies
        background_skills = []
        for row in self.background_data:
            if row['name'].strip() == background:
                skills_field = row.get('skills', '') # Corrected to lowercase 'skills'
                if skills_field:
                    # Split on semicolon or comma, strip whitespace, ignore empty
                    import re
                    background_skills = [s.strip() for s in re.split(r'[;,]', skills_field) if s.strip()]
                break
        # Merge all proficiencies (race + background, no duplicates)
        all_proficiencies = set(selected_race_skills)
        all_proficiencies.update(background_skills)

        # Calculate proficiency bonus based on character level (placeholder - using level 1)
        proficiency_bonus = 2  # Level 1-4 = +2, could be calculated based on actual level

        # Skill to ability mapping
        skill_ability_map = {
            'Acrobatics': 'DEX',
            'Animal Handling': 'WIS', 
            'Arcana': 'INT',
            'Athletics': 'STR',
            'Deception': 'CHA',
            'History': 'INT',
            'Insight': 'WIS',
            'Intimidation': 'CHA',
            'Investigation': 'INT',
            'Medicine': 'WIS',
            'Nature': 'INT',
            'Perception': 'WIS',
            'Performance': 'CHA',
            'Persuasion': 'CHA',
            'Religion': 'INT',
            'Sleight of Hand': 'DEX',
            'Stealth': 'DEX',
            'Survival': 'WIS'
        }
        
        # Build skill data with proficiency
        skill_data = {}
        skill_checkboxes = {}
        for skill, ability in skill_ability_map.items():
            base_mod = mods[ability]
            is_proficient = skill in all_proficiencies
            if is_proficient:
                skill_modifier = base_mod + proficiency_bonus
                skill_checkboxes[skill] = True
            else:
                skill_modifier = base_mod
                skill_checkboxes[skill] = False
            skill_data[skill] = f"{skill_modifier:+d}"

        # Add class skill proficiencies to skill checkboxes
        selected_class_skills = self.get_selected_class_skills() if hasattr(self, 'get_selected_class_skills') else []
        for skill in selected_class_skills:
            if skill in skill_checkboxes:
                skill_checkboxes[skill] = True
            skill_data[skill] = f"{skill_modifier:+d}"

        # Handle equipment start vs gold start choice
        equipment_choice = self.prompt_equipment_choice()
        equipment_list = []
        starting_gold = 0
        
        if equipment_choice == 'equipment':
            # Get starting equipment from class data
            for entry in self.class_data:
                if entry.get('name', '').strip() == class_name:
                    starting_equipment = entry.get('starting_equipment', {})
                    
                    # Add armor
                    armor = starting_equipment.get('armor', [])
                    equipment_list.extend(armor)
                    
                    # Add weapons  
                    weapons = starting_equipment.get('weapons', [])
                    equipment_list.extend(weapons)
                    
                    # Add gear
                    gear = starting_equipment.get('gear', [])
                    equipment_list.extend(gear)
                    
                    # Add starting gold from equipment
                    starting_gold = starting_equipment.get('gold', 0)
                    break
        else:  # gold start
            # Get gold_start amount from class data
            for entry in self.class_data:
                if entry.get('name', '').strip() == class_name:
                    starting_gold = entry.get('gold_start', 0)
                    break

        # Add class skill proficiencies to skill checkboxes
        selected_class_skills = self.get_selected_class_skills() if hasattr(self, 'get_selected_class_skills') else []
        for skill in selected_class_skills:
            if skill in skill_checkboxes:
                skill_checkboxes[skill] = True

        pdf_data = {
            'CharacterName': char_name,
            'ClassLevel': f'{class_name} {level}',
            'Background': background,
            'PlayerName': player_name,
            'Race': race,
            'Alignment': alignment,
            'STRmod': str(stats['STR']),
            'DEXmod ': str(stats['DEX']),
            'CONmod': str(stats['CON']),
            'INTmod': str(stats['INT']),
            'WISmod': str(stats['WIS']),
            'CHamod': str(stats['CHA']),
            'STR': f"{mods['STR']:+d}",
            'DEX': f"{mods['DEX']:+d}",
            'CON': f"{mods['CON']:+d}",
            'INT': f"{mods['INT']:+d}",
            'WIS': f"{mods['WIS']:+d}",
            'CHA': f"{mods['CHA']:+d}",
            # Saving throws (use stat mod for now)
            'ST Strength': f"{mods['STR']:+d}",
            'ST Dexterity': f"{mods['DEX']:+d}",
            'ST Constitution': f"{mods['CON']:+d}",
            'ST Intelligence': f"{mods['INT']:+d}",
            'ST Wisdom': f"{mods['WIS']:+d}",
            'ST Charisma': f"{mods['CHA']:+d}",
            # Skills with proficiency calculations
            'Acrobatics': skill_data['Acrobatics'],
            'Animal': skill_data['Animal Handling'],
            'Arcana': skill_data['Arcana'],
            'Athletics': skill_data['Athletics'],
            'Deception ': skill_data['Deception'],
            'History ': skill_data['History'],
            'Insight': skill_data['Insight'],
            'Intimidation': skill_data['Intimidation'],
            'Investigation ': skill_data['Investigation'],
            'Medicine': skill_data['Medicine'],
            'Nature': skill_data['Nature'],
            'Perception ': skill_data['Perception'],
            'Performance': skill_data['Performance'],
            'Persuasion': skill_data['Persuasion'],
            'Religion': skill_data['Religion'],
            'SleightofHand': skill_data['Sleight of Hand'],
            'Stealth ': skill_data['Stealth'],
            'Survival': skill_data['Survival'],
            # Personality, ideals, bonds, flaws (placeholders, could add UI fields)
            'PersonalityTraits': '',
            'Ideals': '',
            'Bonds': '',
            'Flaws': '',
            # Equipment and features (placeholders, could add UI fields)
            'Equipment': '\n'.join(equipment_list),
            'Features and Traits': features_and_traits,
            'AttacksSpellcasting': attacks_spellcasting,
            'ProficienciesLang': race_languages,
            # Passive Perception (WIS mod + 10)
            'Passive': str(10 + mods['WIS']),
            # AC, Initiative, Speed, HP, etc. (placeholders)
            'AC': '',
            'Initiative': f"{mods['DEX']:+d}",
            'Speed': '',
            'HPMax': '',
            'HPCurrent': '',
            'HPTemp': '',
            # Currency (placeholders)
            'CP': '', 'SP': '', 'EP': '', 'GP': str(starting_gold), 'PP': '',
        }

        # CORRECTED LOGIC for ProficienciesLang content and line breaks:
        # The existing race_languages is the base.
        # Then, append lines extracted from features, ensuring proper newlines.
        
        # Start with race_languages, ensuring it's a string.
        # Replace literal '\\n' from CSV/input with actual newlines if necessary, though pdfrw usually handles '\n'.
        current_prof_lang_text = str(race_languages).replace('\\\\n', '\\n')

        if 'extracted_lines_for_prof_lang' in locals() and isinstance(extracted_lines_for_prof_lang, list) and extracted_lines_for_prof_lang:
            # Join the extracted lines with a single newline character
            additional_text = '\n'.join(extracted_lines_for_prof_lang)
            
            # Append additional_text to current_prof_lang_text
            if current_prof_lang_text and additional_text: # Both have content
                current_prof_lang_text += '\n' + additional_text
            elif additional_text: # Only additional_text has content
                current_prof_lang_text = additional_text
            # If only current_prof_lang_text has content, it's already set.
            # If both are empty, it remains empty.        # Add class proficiencies (armor, weapons, tools) to ProficienciesLang
        class_proficiencies = []
        for entry in self.class_data:
            if entry.get('name', '').strip() == class_name:
                proficiencies = entry.get('proficiencies', {})
                  # Add armor proficiencies with "armor" suffix (except shields)
                armor_profs = proficiencies.get('armor', [])
                for armor in armor_profs:
                    if armor.strip():
                        if armor.lower() == 'shields':
                            class_proficiencies.append(armor.capitalize())
                        else:
                            class_proficiencies.append(f"{armor.capitalize()} armor")
                
                # Add weapon proficiencies with "weapons" suffix
                weapon_profs = proficiencies.get('weapons', [])
                for weapon in weapon_profs:
                    if weapon.strip():
                        if weapon.lower() == 'firearms':
                            class_proficiencies.append(weapon.capitalize())
                        else:
                            class_proficiencies.append(f"{weapon.capitalize()} weapons")
                  # Add tool proficiencies (handle artisanchoice and artisaninstrumentchoice)
                tool_profs = proficiencies.get('tools', [])
                for tool in tool_profs:
                    if tool.strip():
                        if tool.lower() == 'artisanchoice':
                            # Prompt user to choose an artisan's tool
                            selected_artisan_tool = self.prompt_artisan_tool_choice()
                            if selected_artisan_tool:
                                class_proficiencies.append(selected_artisan_tool)
                            else:
                                # User cancelled, show warning and use placeholder
                                QMessageBox.warning(self, 'Warning', 
                                    'No artisan tool selected. Using "Artisan\'s Tools" as placeholder.')
                                class_proficiencies.append("Artisan's Tools")
                        elif tool.lower() == 'artisaninstrumentchoice':
                            # Prompt user to choose between artisan's tools or musical instrument
                            selected_tool_or_instrument = self.prompt_artisan_or_instrument_choice()
                            if selected_tool_or_instrument:
                                class_proficiencies.append(selected_tool_or_instrument)
                            else:
                                # User cancelled, show warning and use placeholder
                                QMessageBox.warning(self, 'Warning', 
                                    'No tool/instrument selected. Using "Artisan\'s Tools or Musical Instrument" as placeholder.')
                                class_proficiencies.append("Artisan's Tools or Musical Instrument")
                        else:
                            class_proficiencies.append(tool.capitalize())
                break
        
        # Add class proficiencies to current_prof_lang_text
        if class_proficiencies:
            class_prof_text = '\n'.join(class_proficiencies)
            if current_prof_lang_text:
                current_prof_lang_text += '\n' + class_prof_text
            else:
                current_prof_lang_text = class_prof_text
        pdf_data['ProficienciesLang'] = current_prof_lang_text
        # END CORRECTED LOGIC

        # Add saving throw proficiencies
        selected_class_name = self.class_combo.currentText()
        class_saving_throws = []
        if hasattr(self, 'class_data'):
            for c_data in self.class_data:
                if c_data.get('name') == selected_class_name:
                    class_saving_throws = [s.lower() for s in c_data.get('saving_throws', [])] # Ensure lowercase for comparison
                    break
        
        saving_throw_map = {
            "strength": "Check Box 11",
            "dexterity": "Check Box 18",
            "constitution": "Check Box 19",
            "intelligence": "Check Box 20",
            "wisdom": "Check Box 21",
            "charisma": "Check Box 22"
        }

        for save_name, pdf_field in saving_throw_map.items():
            if save_name in class_saving_throws:
                pdf_data[pdf_field] = 'Yes'
            else:
                pdf_data[pdf_field] = 'Off'

        # Add correct skill proficiency checkboxes (Check Box 23-40)
        skill_checkbox_order = [
            'Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception', 'History',
            'Insight', 'Intimidation', 'Investigation', 'Medicine', 'Nature', 'Perception',
            'Performance', 'Persuasion', 'Religion', 'Sleight of Hand', 'Stealth', 'Survival'
        ]
        for i, skill in enumerate(skill_checkbox_order, start=23):
            pdf_data[f'Check Box {i}'] = 'Yes' if skill_checkboxes.get(skill, False) else 'Off'
        # Personality, ideals, bonds, flaws (placeholders, could add UI fields)
        # Equipment and features (placeholders, could add UI fields)
        # Currency (placeholders)
        template_path = 'character_sheet_template.pdf'
        output_path = f"{char_name.replace(' ', '_')}.pdf"
        try:
            pdf = PdfReader(template_path)
            for page in pdf.pages:
                annotations = page.Annots
                if annotations:
                    for annotation in annotations:
                        if annotation.Subtype == '/Widget' and annotation.T:
                            key = annotation.T[1:-1]  # Remove parentheses
                            if key in pdf_data:
                                annotation.V = str(pdf_data[key])
                                annotation.AP = ''
            PdfWriter().write(output_path, pdf)
            QMessageBox.information(self, 'PDF Exported', f'Character sheet saved as {output_path}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to export PDF: {e}')

    def prompt_equipment_choice(self):
        """Prompt user to choose between equipment start or gold start"""
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle('Starting Equipment')
        msg.setText('Choose your starting equipment option:')
        equipment_btn = msg.addButton('Equipment Start', QMessageBox.ActionRole)
        gold_btn = msg.addButton('Gold Start', QMessageBox.ActionRole)
        msg.exec()
        
        if msg.clickedButton() == equipment_btn:
            return 'equipment'
        else:
            return 'gold'

    def on_race_changed(self):
        race_name = self.race_combo.currentText()
        chosen = []
        for row in self.race_data:
            if row['name'].strip() == race_name:
                # When processing race skill proficiencies, use the SkillProfToChooseFrom/Choose column from races.csv
                # Example logic:
                #   - If value is "/0" or blank: no skill proficiency from race
                #   - If value is "Skill/1": grant that skill
                #   - If value is "Skill1, Skill2, .../N": prompt user to choose N from the list
                prof_choice = row.get('SkillProfToChooseFrom/Choose', '').strip()
                if prof_choice and prof_choice != '/0':
                    if '/' in prof_choice:
                        # Prompt user to choose
                        from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
                        dlg = QDialog()
                        dlg.setWindowTitle('Choose Skill Proficiencies')
                        layout = QVBoxLayout()
                        layout.addWidget(QLabel(f"Choose {prof_choice.split('/')[-1]} skill proficiencies:"))
                        combo = QComboBox()
                        options = [opt.strip() for opt in prof_choice.split(',')[:-1]]  # Exclude the last empty split
                        combo.addItems(options)
                        layout.addWidget(combo)
                        btn = QPushButton('OK')
                        btn.clicked.connect(dlg.accept)
                        layout.addWidget(btn)
                        dlg.setLayout(layout)
                        dlg.exec()
                        chosen.append(combo.currentText())
                    else:
                        # Grant the single skill
                        chosen.append(prof_choice)
                break
        self.chosen_race_proficiencies = chosen
        # Update proficiency label if present
        if hasattr(self, 'proficiency_label'):
            self.proficiency_label.setText(self.get_all_proficiencies())

    def get_all_proficiencies(self):
        # Combine all chosen proficiencies (race, class, background, static)
        profs = []
        if hasattr(self, 'chosen_race_proficiencies'):
            profs.extend(self.chosen_race_proficiencies)
        # TODO: Add class/background/other profs
        return ', '.join(profs) if profs else 'None'
    
    # --- Skill Proficiency Selection Logic (non-GUI structural update) ---
    def update_skills_selection(self, race_name):
        # Only update the selection logic, not the GUI layout
        self.required_race_skills = 0
        self.allowed_race_skills = []
        self.skills_list.clearSelection()
        if not race_name or race_name == 'None':
            return
        for row in self.race_data:
            if row['name'].strip() == race_name:
                prof_choice = row.get('SkillProfToChooseFrom/Choose', '').strip()
                if prof_choice and prof_choice != '/0':
                    if '/' in prof_choice:
                        skills_part, num_part = prof_choice.rsplit('/', 1)
                        try:
                            num_to_choose = int(num_part)
                        except ValueError:
                            num_to_choose = 0
                        skills = [s.strip() for s in skills_part.split(',') if s.strip()]
                        self.required_race_skills = num_to_choose
                        self.allowed_race_skills = skills
                        # Only allow selection from the allowed skills
                        for i in range(self.skills_list.count()):
                            item = self.skills_list.item(i)
                            item.setSelected(False)
                            item.setHidden(item.text() not in skills)
                    else:
                        # Fixed skill, auto-select and lock
                        for i in range(self.skills_list.count()):
                            item = self.skills_list.item(i)
                            if item.text() == prof_choice:
                                item.setSelected(True)
                                item.setFlags(item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEditable)
                            else:
                                item.setHidden(True)
                        self.required_race_skills = 1
                        self.allowed_race_skills = [prof_choice]
                else:
                    # No skills to choose from
                    for i in range(self.skills_list.count()):
                        self.skills_list.item(i).setHidden(True)
                break

    def enforce_skill_selection_limit(self):
        # Only allow up to the required number of skills to be selected
        selected = [item for item in self.skills_list.selectedItems() if not item.isHidden()]
        if self.required_race_skills and len(selected) > self.required_race_skills:
            for item in selected[self.required_race_skills:]:
                item.setSelected(False)

    def get_selected_race_skills(self):
        # Return the list of selected skills for the race
        return [item.text() for item in self.skills_list.selectedItems() if not item.isHidden()]

    def prompt_artisan_tool_choice(self):
        """Prompt user to choose an artisan's tool from available options"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
        
        artisan_tools = [
            "Alchemist's Supplies",
            "Brewer's Supplies", 
            "Calligrapher's Supplies",
            "Carpenter's Tools",
            "Cartographer's Tools",
            "Cobbler's Tools",
            "Cook's Utensils",
            "Glassblower's Tools",
            "Jeweler's Tools",
            "Leatherworker's Tools",
            "Mason's Tools",
            "Painter's Supplies",
            "Potter's Tools",
            "Smith's Tools",
            "Tinker's Tools",
            "Weaver's Tools",
            "Woodcarver's Tools"
        ]
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Choose Artisan's Tool")
        dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        label = QLabel("Your class grants proficiency with one artisan's tool of your choice.\nPlease select an artisan's tool:")
        layout.addWidget(label)
        
        combo = QComboBox()
        combo.addItems(artisan_tools)
        layout.addWidget(combo)
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        
        def on_ok():
            dialog.accept()
        
        def on_cancel():
            dialog.reject()
            
        ok_button.clicked.connect(on_ok)
        cancel_button.clicked.connect(on_cancel)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.Accepted:
            return combo.currentText()
        else:
            return None

    def prompt_artisan_or_instrument_choice(self):
        """Prompt user to choose between an artisan's tool or musical instrument"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Choose Tool or Instrument")
        dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        label = QLabel("Your class grants proficiency with one artisan's tool or musical instrument of your choice.\nPlease select a tool type:")
        layout.addWidget(label)
        
        type_combo = QComboBox()
        type_combo.addItems(["Artisan's Tool", "Musical Instrument"])
        layout.addWidget(type_combo)
        
        # Tool/instrument selection combo (initially hidden)
        selection_combo = QComboBox()
        layout.addWidget(selection_combo)
        
        artisan_tools = [
            "Alchemist's Supplies",
            "Brewer's Supplies", 
            "Calligrapher's Supplies",
            "Carpenter's Tools",
            "Cartographer's Tools",
            "Cobbler's Tools",
            "Cook's Utensils",
            "Glassblower's Tools",
            "Jeweler's Tools",
            "Leatherworker's Tools",
            "Mason's Tools",
            "Painter's Supplies",
            "Potter's Tools",
            "Smith's Tools",
            "Tinker's Tools",
            "Weaver's Tools",
            "Woodcarver's Tools"
        ]
        
        musical_instruments = [
            "Bagpipes",
            "Drum",
            "Dulcimer",
            "Flute",
            "Lute",
            "Lyre",
            "Horn",
            "Pan Flute",
            "Shawm",
            "Viol"
        ]
        
        def update_selection_options():
            selection_combo.clear()
            if type_combo.currentText() == "Artisan's Tool":
                selection_combo.addItems(artisan_tools)
            else:
                selection_combo.addItems(musical_instruments)
        
        type_combo.currentTextChanged.connect(update_selection_options)
        update_selection_options()  # Initialize
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        
        def on_ok():
            dialog.accept()
        
        def on_cancel():
            dialog.reject()
            
        ok_button.clicked.connect(on_ok)
        cancel_button.clicked.connect(on_cancel)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.Accepted:
            return selection_combo.currentText()
        else:
            return None

def gui_main():
    app = QApplication(sys.argv)
    window = MagicItemGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    gui_main()
