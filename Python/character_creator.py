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

class CharacterCreator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Character Creator')
        self.setGeometry(100, 100, 800, 600)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.init_character_creator_tab()
        self.init_load_character_sheet_tab()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')
        self.setStyleSheet('''
            QMainWindow, QWidget {
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 13px;
                background: #f6faff;
                color: #1a2a4a;
            }
            QLabel {
                font-size: 13px;
                color: #1a2a4a;
                padding: 2px 6px;
            }
            QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit {
                font-size: 13px;
                background: #fff;
                border: 1.5px solid #b0c4de;
                border-radius: 6px;
                padding: 4px 8px;
                min-width: 80px;
                color: #1a2a4a;
            }
            QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {
                border: 2px solid #5a9bd6;
                background: #eaf6ff;
            }
            QCheckBox {
                font-size: 13px;
                color: #1a2a4a;
                min-width: 120px;
                min-height: 28px;
                max-width: 140px;
                max-height: 36px;
                border: 1px solid #b0c4de;
                border-radius: 6px;
                padding: 6px;
                background: #eee;
            }
            QCheckBox:checked {
                background: #aaf;
                border: 2px solid #44f;
            }
            QGroupBox {
                background: #f6faff;
                border-radius: 12px;
                border: 1.5px solid #b0c4de;
                font-size: 14px;
                margin-top: 8px;
                padding: 12px;
            }
            QPushButton {
                font-size: 13px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #eaf6ff, stop:1 #d0eaff);
                color: #1a2a4a;
                border: 1.5px solid #b0c4de;
                border-radius: 8px;
                padding: 8px 18px;
                margin: 4px 0px;
            }
            QPushButton:hover {
                background: #d0eaff;
                border: 2px solid #5a9bd6;
            }
            QPushButton:pressed {
                background: #b0c4de;
                border: 2px solid #226;
            }
            QTabWidget::pane {
                border: 2px solid #b0c4de;
                border-radius: 10px;
                background: #f6faff;
            }
            QTabBar::tab {
                font-size: 14px;
                background: #eaf6ff;
                border: 1.5px solid #b0c4de;
                border-radius: 8px;
                padding: 8px 18px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #d0eaff;
                border: 2px solid #5a9bd6;
            }
            QTabBar::tab:hover {
                background: #f8faff;
                border: 2px solid #5a9bd6;
            }
            QScrollArea {
                background: #f6faff;
                border-radius: 10px;
                border: 1.5px solid #b0c4de;
            }
            QFrame {
                background: #f8faff;
                border-radius: 12px;
                border: 1.5px solid #b0c4de;
                margin-top: 0px;
                margin-bottom: 10px;
                padding: 12px 16px;
            }
        ''' )
    def init_load_character_sheet_tab(self):
        from load_character_sheet import LoadCharacterSheetWidget
        load_tab = LoadCharacterSheetWidget()
        self.tabs.addTab(load_tab, 'Load Character Sheet')

    def make_collapsible_section(self, title, content_widget):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        toggle = QToolButton()
        toggle.setText(title)
        toggle.setCheckable(True)
        toggle.setChecked(False)
        toggle.setStyleSheet('''
            QToolButton {
                font-weight: bold;
                font-size: 14pt;
                text-align: left;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #eaf6ff, stop:1 #d0eaff);
                border: 2px solid #b0c4de;
                border-radius: 12px;
                padding: 10px 20px;
                margin-bottom: 0px;
                letter-spacing: 1px;
            }
            QToolButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d0eaff, stop:1 #eaf6ff);
                border: 2.5px solid #5a9bd6;
            }
        ''')
        toggle.setToolButtonStyle(Qt.ToolButtonTextOnly)
        toggle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet('''
            QFrame {
                background: #f8faff;
                border-radius: 12px;
                border: 1.5px solid #b0c4de;
                margin-top: 0px;
                margin-bottom: 10px;
                padding: 12px 16px;
            }
        ''')
        frame.setLayout(QVBoxLayout())
        frame.layout().addWidget(content_widget)
        frame.setVisible(False)
        def on_toggle(checked):
            frame.setVisible(checked)
        toggle.toggled.connect(on_toggle)
        layout.addWidget(toggle)
        layout.addWidget(frame)
        return container
    
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

    def init_character_creator_tab(self):
        level_bar = QHBoxLayout()
        level_label = QLabel('Level:')
        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 20)
        self.level_spin.setValue(1)
        level_bar.addWidget(level_label)
        level_bar.addWidget(self.level_spin)
        level_bar.addStretch()
        char_tab = QWidget()
        char_layout = QVBoxLayout()
        char_tab.setLayout(char_layout)
        self.required_race_skills = 0
        self.allowed_race_skills = []
        self.required_class_skills = 0
        self.allowed_class_skills = []
        race_bar = QHBoxLayout()
        race_label = QLabel('Race:')
        self.race_combo = QComboBox()
        self.race_data = []
        races = []
        try:
            with open('Data/races.csv', 'r', encoding='utf-8') as f:
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
        self.race_info_label = QLabel()
        self.race_info_label.setWordWrap(True)
        self.race_info_label.setStyleSheet('font-size: 11pt; background: #f8f8f8; padding: 8px; border: 1px solid #ccc;')
        race_scroll = QScrollArea()
        race_scroll.setWidgetResizable(True)
        race_scroll.setMinimumHeight(200)
        race_scroll.setMaximumHeight(500)
        race_scroll.setWidget(self.race_info_label)
        race_info_section = self.make_collapsible_section('Show Race Details', race_scroll)
        # Do not add race_info_section here; it will be added in the grid below
        self.race_combo.currentTextChanged.connect(self.update_race_info)
        self.update_race_info(self.race_combo.currentText())

        # --- Background and class details setup (unchanged) ---
        bg_bar = QHBoxLayout()
        bg_label = QLabel('Background:')
        self.bg_combo = QComboBox()
        self.background_data = []
        backgrounds = []
        try:
            with open('Data/backgrounds.csv', 'r', encoding='utf-8') as f:
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
        self.bg_info_label = QLabel()
        self.bg_info_label.setWordWrap(True)
        self.bg_info_label.setStyleSheet('font-size: 11pt; background: #f8f8f8; padding: 8px; border: 1px solid #ccc;')
        bg_scroll = QScrollArea()
        bg_scroll.setWidgetResizable(True)
        bg_scroll.setMinimumHeight(200)
        bg_scroll.setMaximumHeight(500)
        bg_scroll.setWidget(self.bg_info_label)
        bg_info_section = self.make_collapsible_section('Show Background Details', bg_scroll)
        self.bg_combo.currentTextChanged.connect(self.update_bg_info)
        self.update_bg_info(self.bg_combo.currentText())

        class_bar = QHBoxLayout()
        class_label = QLabel('Class:')
        self.class_combo = QComboBox()
        import json
        self.class_data = []
        classes = []
        try:
            with open('Data/classes.json', 'r', encoding='utf-8') as f:
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
        self.class_info_label = QLabel()
        self.class_info_label.setWordWrap(True)
        self.class_info_label.setStyleSheet('font-size: 12pt; background: #f8f8f8; padding: 10px; border: 2px solid #888;')
        class_scroll = QScrollArea()
        class_scroll.setWidgetResizable(True)
        class_scroll.setMinimumHeight(200)
        class_scroll.setMaximumHeight(500)
        class_scroll.setWidget(self.class_info_label)
        class_info_section = self.make_collapsible_section('Show Class Details', class_scroll)
        self.class_combo.currentTextChanged.connect(self.update_class_info)
        self.update_class_info(self.class_combo.currentText())

        # --- Place all three details sections in a grid, side by side ---
        from PySide6.QtWidgets import QGridLayout
        details_grid = QGridLayout()
        details_grid.setSpacing(12)
        details_grid.addWidget(class_info_section, 0, 2)
        details_grid.addWidget(bg_info_section, 0, 1)
        details_grid.addWidget(race_info_section, 0, 0)
        char_layout.addLayout(details_grid)
        stat_gen_bar = QHBoxLayout()
        # stat_label = QLabel('Stat Generation:')
        # stat_label.setStyleSheet('font-weight: bold; font-size: 14pt; letter-spacing: 1px;')
        # stat_gen_bar.addWidget(stat_label)
        stat_names = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']
        stat_card_layout = QHBoxLayout()
        stat_card_layout.setSpacing(8)
        stat_card_layout.setAlignment(Qt.AlignLeft)
        self.stat_spinboxes = []
        self.stat_increase_labels = []
        self.stat_total_labels = []
        self.stat_combos = []
        for i, stat in enumerate(stat_names):
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet('''
                QFrame { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #eaf6ff, stop:1 #d0eaff); border-radius: 12px; border: 1.5px solid #b0c4de; min-width: 60px; max-width: 100px; min-height: 110px; }
            ''')
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(8, 8, 8, 8)
            stat_title = QLabel(stat)
            stat_title.setAlignment(Qt.AlignCenter)
            stat_title.setStyleSheet('font-size: 15px; font-weight: 600; color: #1a2a4a; letter-spacing: 1px; padding: 0px 6px; min-height: 22px; max-height: 24px;')
            card_layout.addWidget(stat_title)
            spin = QSpinBox()
            spin.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
            spin.setRange(1, 20)
            spin.setValue(10)
            spin.setAlignment(Qt.AlignCenter)
            spin.setStyleSheet('''
                font-size: 18px; font-weight: bold; background: #fff; border-radius: 6px; padding: 0px 6px; min-width: 40px; min-height: 28px; max-height: 32px; border: 2px solid #000;
                QSpinBox::up-button, QSpinBox::down-button { width: 0px; height: 0px; border: none; background: none; }
                QSpinBox::up-arrow, QSpinBox::down-arrow { image: none; width: 0px; height: 0px; }
            ''')
            card_layout.addWidget(spin)
            inc_label = QLabel('Increase: 0')
            inc_label.setAlignment(Qt.AlignCenter)
            inc_label.setStyleSheet('font-size: 12px; color: #2a7; background: #eaffea; border-radius: 4px; padding: 0px 6px; margin-top: 2px; font-weight: 500; min-height: 22px; max-height: 24px;')
            card_layout.addWidget(inc_label)
            total_label = QLabel('Total: 10')
            total_label.setAlignment(Qt.AlignCenter)
            total_label.setStyleSheet('font-size: 13px; color: #226; background: #f0f8ff; border-radius: 4px; padding: 0px 6px; margin-top: 1px; font-weight: 500; min-height: 22px; max-height: 24px;')
            card_layout.addWidget(total_label)
            self.stat_spinboxes.append(spin)
            self.stat_increase_labels.append(inc_label)
            self.stat_total_labels.append(total_label)
            stat_card_layout.addWidget(card)
        stat_gen_bar.addLayout(stat_card_layout)
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
        stat_controls_bar = QHBoxLayout()
        gen_btn = QPushButton('Generate Stats')
        gen_btn.clicked.connect(self.generate_stats)
        stat_controls_bar.addWidget(gen_btn)
        stat_controls_bar.addStretch()
        char_layout.addLayout(race_bar)
        # char_layout.addWidget(race_info_section)
        char_layout.addLayout(bg_bar)
        # Do not add bg_info_section here; it will be added in the grid below
        char_layout.addLayout(class_bar)
        # Do not add class_info_section here; it will be added in the grid below
        char_layout.addLayout(asi_radio_bar)
        char_layout.addLayout(stat_gen_bar)
        char_layout.addLayout(stat_controls_bar)
        char_layout.addLayout(param_bar)
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
        for spin in self.stat_spinboxes:
            spin.valueChanged.connect(self.update_stat_totals)
        self.asi_group.buttonClicked.disconnect()
        self.asi_group.buttonClicked.connect(self.on_asi_source_changed)       
        skill_gen_bar = QHBoxLayout()
        skill_label = QLabel('Skill Generation:')
        skill_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
        skill_gen_bar.addWidget(skill_label)
        self.proficiency_widget = QWidget()
        self.proficiency_layout = QVBoxLayout()
        self.proficiency_widget.setLayout(self.proficiency_layout)
        self.proficiency_dropdowns = [] 
        char_layout.addWidget(QLabel('Race Skill Proficiencies:'))
        self.race_skill_widget = QWidget()
        self.race_skill_layout = QGridLayout()
        self.race_skill_layout.setAlignment(Qt.AlignLeft)
        self.race_skill_widget.setLayout(self.race_skill_layout)
        char_layout.addWidget(self.race_skill_widget)
        self.race_skill_checkboxes = []
        self.required_race_skills = 0
        self.allowed_race_skills = []

        def update_race_skill_checkboxes(race_name):
            for cb in self.race_skill_checkboxes:
                self.race_skill_layout.removeWidget(cb)
                cb.deleteLater()
            self.race_skill_checkboxes.clear()
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
                            for idx, skill in enumerate(skills):
                                cb = QCheckBox(skill)
                                cb.setLayoutDirection(Qt.LeftToRight)
                                cb.setFixedSize(140, 36)
                                cb.setStyleSheet('QCheckBox { text-align: left; min-width: 120px; min-height: 28px; max-width: 140px; max-height: 36px; border: 1px solid #888; border-radius: 6px; padding: 6px; background: #eee; } QCheckBox::indicator { width: 0; height: 0; } QCheckBox:checked { background: #aaf; border: 2px solid #44f; }')
                                cb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                                cb.setMinimumWidth(120)
                                cb.setMaximumWidth(140)
                                cb.setMinimumHeight(28)
                                cb.setMaximumHeight(36)
                                try:
                                    cb.setAlignment(Qt.AlignLeft)
                                except Exception:
                                    pass
                                row_num = idx // 12
                                col_num = idx % 12
                                self.race_skill_layout.addWidget(cb, row_num, col_num)
                                self.race_skill_checkboxes.append(cb)
                            def enforce_limit():
                                checked = [cb for cb in self.race_skill_checkboxes if cb.isChecked()]
                                if len(checked) >= self.required_race_skills:
                                    for cb in self.race_skill_checkboxes:
                                        if not cb.isChecked():
                                            cb.setEnabled(False)
                                else:
                                    for cb in self.race_skill_checkboxes:
                                        cb.setEnabled(True)
                            for cb in self.race_skill_checkboxes:
                                cb.stateChanged.connect(enforce_limit)
                            enforce_limit()
                        else:
                            cb = QCheckBox(prof_choice)
                            cb.setChecked(True)
                            cb.setEnabled(False)
                            cb.setFixedSize(140, 36)
                            cb.setStyleSheet('QCheckBox { text-align: left; min-width: 120px; min-height: 28px; max-width: 140px; max-height: 36px; border: 1px solid #888; border-radius: 6px; padding: 6px; background: #eee; } QCheckBox::indicator { width: 0; height: 0; } QCheckBox:checked { background: #aaf; border: 2px solid #44f; }')
                            cb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                            cb.setMinimumWidth(120)
                            cb.setMaximumWidth(140)
                            cb.setMinimumHeight(28)
                            cb.setMaximumHeight(36)
                            try:
                                cb.setAlignment(Qt.AlignLeft)
                            except Exception:
                                pass
                            self.race_skill_layout.addWidget(cb, 0, 0)
                            self.race_skill_checkboxes.append(cb)
                            self.required_race_skills = 1
                            self.allowed_race_skills = [prof_choice]
                    break

        def get_selected_race_skills():
            return [cb.text() for cb in self.race_skill_checkboxes if cb.isChecked()]

        self.update_race_skill_checkboxes = update_race_skill_checkboxes
        self.get_selected_race_skills = get_selected_race_skills
        self.race_combo.currentTextChanged.connect(self.update_race_skill_checkboxes)
        self.update_race_skill_checkboxes(self.race_combo.currentText())

        char_layout.addWidget(QLabel('Class Skill Proficiencies:'))
        self.class_skill_widget = QWidget()
        self.class_skill_layout = QGridLayout()
        self.class_skill_layout.setAlignment(Qt.AlignLeft)
        self.class_skill_widget.setLayout(self.class_skill_layout)
        char_layout.addWidget(self.class_skill_widget)
        self.class_skill_checkboxes = []
        self.required_class_skills = 0
        self.allowed_class_skills = []

        def update_class_skill_checkboxes(class_name):
            for cb in self.class_skill_checkboxes:
                self.class_skill_layout.removeWidget(cb)
                cb.deleteLater()
            self.class_skill_checkboxes.clear()
            self.required_class_skills = 0
            self.allowed_class_skills = []
            if not class_name or class_name == 'None':
                return
            for entry in self.class_data:
                if entry.get('name', '').strip() == class_name:
                    proficiencies = entry.get('proficiencies', {})
                    skills_field = proficiencies.get('skills', [])
                    if skills_field and isinstance(skills_field, list) and len(skills_field) > 1:
                        try:
                            num_to_choose = int(skills_field[0])
                        except Exception:
                            num_to_choose = 2
                        skills = [s for s in skills_field[1:]]
                        self.required_class_skills = num_to_choose
                        self.allowed_class_skills = skills
                        for idx, skill in enumerate(skills):
                            cb = QCheckBox(skill)
                            cb.setFixedSize(140, 36)
                            cb.setLayoutDirection(Qt.LeftToRight)
                            cb.setStyleSheet('QCheckBox { text-align: left; min-width: 120px; min-height: 28px; max-width: 140px; max-height: 36px; border: 1px solid #888; border-radius: 6px; padding: 6px; background: #eee; } QCheckBox::indicator { width: 0; height: 0; } QCheckBox:checked { background: #aaf; border: 2px solid #44f; }')
                            cb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                            cb.setMinimumWidth(120)
                            cb.setMaximumWidth(140)
                            cb.setMinimumHeight(28)
                            cb.setMaximumHeight(36)
                            try:
                                cb.setAlignment(Qt.AlignLeft)
                            except Exception:
                                pass
                            row = idx // 12
                            col = idx % 12
                            self.class_skill_layout.addWidget(cb, row, col)
                            self.class_skill_checkboxes.append(cb)
                        def enforce_limit():
                            checked = [cb for cb in self.class_skill_checkboxes if cb.isChecked()]
                            if len(checked) >= self.required_class_skills:
                                for cb in self.class_skill_checkboxes:
                                    if not cb.isChecked():
                                        cb.setEnabled(False)
                            else:
                                for cb in self.class_skill_checkboxes:
                                    cb.setEnabled(True)
                        for cb in self.class_skill_checkboxes:
                            cb.stateChanged.connect(enforce_limit)
                        enforce_limit()
                    break

        def get_selected_class_skills():
            return [cb.text() for cb in self.class_skill_checkboxes if cb.isChecked()]

        self.update_class_skill_checkboxes = update_class_skill_checkboxes
        self.get_selected_class_skills = get_selected_class_skills
        self.class_combo.currentTextChanged.connect(self.update_class_skill_checkboxes)
        QTimer.singleShot(0, lambda: self.update_class_skill_checkboxes(self.class_combo.currentText()))
        self.spell_data = []
        self.selected_spells = {}
        self.spell_widgets = {}
        try:
            with open('Data/spells.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.spell_data = list(reader)
        except Exception:
            self.spell_data = []

        self.spell_section_widget = QWidget()
        spell_section_layout = QVBoxLayout(self.spell_section_widget)
        
        spell_label = QLabel('Spell Selection:')
        spell_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
        spell_section_layout.addWidget(spell_label)
        
        self.spell_info_label = QLabel('No spells available for this class/level.')
        self.spell_info_label.setWordWrap(True)
        spell_section_layout.addWidget(self.spell_info_label)
        self.spell_levels_widget = QWidget()
        self.spell_levels_layout = QVBoxLayout(self.spell_levels_widget)
        spell_section_layout.addWidget(self.spell_levels_widget)
        spell_collapsible_section = self.make_collapsible_section('Spell Selection', self.spell_section_widget)
        char_layout.addWidget(spell_collapsible_section)
        self.level_spin.valueChanged.connect(self.update_spell_selection)
        self.class_combo.currentTextChanged.connect(self.update_spell_selection)
        QTimer.singleShot(500, self.update_spell_selection)
        
        export_pdf_btn = QPushButton('Export to PDF')
        export_pdf_btn.clicked.connect(self.export_character_to_pdf)
        char_layout.addWidget(export_pdf_btn)

        outer_scroll = QScrollArea()
        outer_scroll.setWidgetResizable(True)
        outer_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        container = QWidget()
        container.setLayout(char_layout)
        outer_scroll.setWidget(container)
        self.tabs.addTab(outer_scroll, 'Character Creator')

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
            self.stat_increase_labels[i].setText(f"Increase: {asi.get(stat, 0)}")
            self.stat_total_labels[i].setText(f"Total: {values[i] + asi.get(stat, 0)}")

    def on_asi_source_changed(self):
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
            self.stat_increase_labels[i].setText(f"Increase: {asi.get(stat, 0)}")
            self.stat_total_labels[i].setText(f"Total: {values[i] + asi.get(stat, 0)}")

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
        # Preserve the user's ASI source selection
        self.update_stat_totals()

    def handle_stat_swap(self, changed_idx, *args):
        changed_combo = self.stat_combos[changed_idx]
        selected_idx = changed_combo.currentIndex()
        for i, combo in enumerate(self.stat_combos):
            if i != changed_idx and combo.currentIndex() == selected_idx:
                combo.blockSignals(True)
                changed_combo.blockSignals(True)
                combo.setCurrentIndex(self.stat_combos[changed_idx].property('lastIndex') if combo.property('lastIndex') is not None else changed_idx)
                changed_combo.setCurrentIndex(selected_idx)
                combo.blockSignals(False)
                changed_combo.blockSignals(False)
                break
        for i, combo in enumerate(self.stat_combos):
            combo.setProperty('lastIndex', combo.currentIndex())

    def update_stat_dropdowns(self):
        pass

    def update_race_info(self, race_name):
        for row in self.race_data:
            if row['name'].strip() == race_name:
                info = []
                for key, val in row.items():
                    if key is not None and val and key != 'name':
                        if key.strip().lower() == 'features':
                            features = str(val).replace('\\n', '\n')
                            features = features.replace('\r\n', '\n').replace('\r', '\n')
                            features = features.strip()
                            feature_lines = [f for f in features.split('\n') if f.strip()]
                            features_html = '<br>'.join(f"• {f.strip()}" for f in feature_lines)
                            info.append(f"<b>{str(key).title().replace('_', ' ')}:</b><br>{features_html}")
                        else:
                            info.append(f"<b>{str(key).title().replace('_', ' ')}:</b> {val}")
                self.race_info_label.setText('<br>'.join(info))
                return
        self.race_info_label.setText('')

    def update_bg_info(self, bg_name):
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
        for row in self.class_data:
            if row['name'].strip() == class_name:
                info = []
                if 'hit_die' in row:
                    info.append(f"<b>Hit Die:</b> {row['hit_die']}")
                if 'primary_abilities' in row:
                    abilities = ', '.join(row['primary_abilities'])
                    info.append(f"<b>Primary Abilities:</b> {abilities}")
                if 'subclass_pick_level' in row:
                    info.append(f"<b>Subclass Pick Level:</b> {row['subclass_pick_level']}")
                if 'caster_type' in row and row['caster_type'] != 'none':
                    info.append(f"<b>Caster Type:</b> {row['caster_type'].capitalize()}")
                features = row.get('features', {})
                if features:
                    feature_lines = []
                    for lvl in sorted(features, key=lambda x: int(x)):
                        names = ', '.join(f["name"] for f in features[lvl] if "name" in f)
                        if names:
                            feature_lines.append(f"<b>Level {lvl}:</b> {names}")
                    if feature_lines:
                        info.append("<b>Features by Level:</b><br>" + '<br>'.join(feature_lines))
                subclasses = row.get('subclasses', [])
                if subclasses:
                    subclass_names = ', '.join(sc['name'] for sc in subclasses if 'name' in sc)
                    info.append(f"<b>Subclasses:</b> {subclass_names}")
                self.class_info_label.setText('<br>'.join(info))
                return
        self.class_info_label.setText('')

    def prompt_and_apply_asi(self):
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
        if race:
            race_name = self.race_combo.currentText()
            print(f"[DEBUG] Selected race: {race_name}")
            for row in self.race_data:
                if row['name'].strip() == race_name:
                    asi_str = row.get('Ability Score Increase', '')
                    print(f"[DEBUG] Race ASI string: {asi_str}")
                    asi_result, _ = self.parse_asi_string_with_prompt(asi_str, 'Race')
                    print(f"[DEBUG] Race ASI parsed: {asi_result}")
                    for k, v in asi_result.items():
                        asi[k] += v
                    break
        if background:
            bg_name = self.bg_combo.currentText()
            print(f"[DEBUG] Selected background: {bg_name}")
            for row in self.background_data:
                if row['name'].strip() == bg_name:
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
        import re
        stat_names = {'STR': 'STR', 'DEX': 'DEX', 'CON': 'CON', 'WIS': 'WIS', 'INT': 'INT', 'CHA': 'CHA',
                      'STRENGTH': 'STR', 'DEXTERITY': 'DEX', 'CONSTITUTION': 'CON', 'WISDOM': 'WIS', 'INTELLIGENCE': 'INT', 'CHARISMA': 'CHA',
                      'CHA': 'CHA', 'CON': 'CON', 'WIS': 'WIS', 'INT': 'INT'}
        asi = {k: 0 for k in ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']}
        asi_str = asi_str.strip()
        if not asi_str:
            return asi, None
        direct_pattern = r'([+-]?\d+)\s*(STR|DEX|CON|WIS|INT|CHA|STRENGTH|DEXTERITY|CONSTITUTION|WISDOM|INTELLIGENCE|CHARISMA)|' \
                        r'(STR|DEX|CON|WIS|INT|CHA|STRENGTH|DEXTERITY|CONSTITUTION|WISDOM|INTELLIGENCE|CHARISMA)\s*([+-]?\d+)'
        direct_matches = re.findall(direct_pattern, asi_str.upper())
        if direct_matches:
            for m in direct_matches:
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
        prompt = {'type': None, 'source': source_label, 'raw': asi_str}
        if re.search(r'choose one of', asi_str, re.IGNORECASE):
            prompt['type'] = 'points_among'
            prompt['points'] = 3
            prompt['allowed'] = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']
            return asi, prompt
        elif re.search(r'choose any', asi_str, re.IGNORECASE):
            prompt['type'] = 'choose_any'
            choose_matches = re.findall(r'choose any[^\d+-]*([+-]?\d+)', asi_str, re.IGNORECASE)
            prompt['amounts'] = [int(x) for x in choose_matches]
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
        else:
            prompt['type'] = 'unknown'
        return asi, prompt

    def prompt_asi_choices(self, asi_prompts):
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton, QGroupBox, QFormLayout
        from PySide6.QtCore import QPropertyAnimation
        stat_names = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']
        asi_result = {k: 0 for k in stat_names}
        for prompt in asi_prompts:
            dlg = QDialog(self)
            dlg.setWindowTitle(f"Assign Ability Score Increases ({prompt['source']})")
            dlg.setMinimumWidth(400)
            main_layout = QVBoxLayout()
            # Section header
            header = QLabel(f"<b>{prompt['source']} ASI:</b> <br><i>{prompt['raw']}</i>")
            header.setWordWrap(True)
            header.setStyleSheet('font-size: 16px; color: #2a2a2a; margin-bottom: 8px;')
            main_layout.addWidget(header)
            main_layout.addSpacing(10)

            # Group box for stat assignment
            asi_group = QGroupBox("Assign Points")
            asi_group.setStyleSheet('QGroupBox { background: #f6faff; border-radius: 12px; border: 1.5px solid #b0c4de; font-size: 14px; margin-top: 8px; padding: 12px; }')
            asi_layout = QFormLayout()
            asi_layout.setSpacing(12)

            # Fade-in animation for stat assignment group
            asi_group.setGraphicsEffect(None)
            animation = QPropertyAnimation(asi_group, b"windowOpacity")
            animation.setDuration(400)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)

            # Choose Any: let user pick stats and assign points
            if prompt['type'] == 'choose_any':
                amounts = prompt.get('amounts', [1])
                combo_boxes = []
                for i, amt in enumerate(amounts):
                    stat_combo = QComboBox()
                    stat_combo.addItems(stat_names)
                    stat_combo.setToolTip(f"Select which stat receives +{amt}")
                    stat_combo.setStyleSheet('font-size: 15px; min-height: 28px; border-radius: 6px; background: #eaf6ff;')
                    label = QLabel(f"<b>+{amt}</b> to:")
                    label.setStyleSheet('font-size: 15px;')
                    asi_layout.addRow(label, stat_combo)
                    combo_boxes.append((stat_combo, amt))
                asi_group.setLayout(asi_layout)
                main_layout.addWidget(asi_group)
                animation.start()
                main_layout.addSpacing(10)
                btn = QPushButton('Confirm')
                btn.setStyleSheet('font-size: 15px; font-weight: bold; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e0eaff, stop:1 #cbe6ff); border-radius: 8px; padding: 8px 18px;')
                btn.clicked.connect(dlg.accept)
                main_layout.addWidget(btn)
                dlg.setLayout(main_layout)
                dlg.exec()
                for stat_combo, amt in combo_boxes:
                    chosen_stat = stat_combo.currentText()
                    asi_result[chosen_stat] += amt

            # Points Among: let user distribute points among stats
            elif prompt['type'] == 'points_among':
                points = prompt.get('points', 3)
                allowed = prompt.get('allowed', stat_names)
                spin_boxes = {}
                info_label = QLabel(f"Distribute <b>{points}</b> points among the following stats:")
                info_label.setWordWrap(True)
                info_label.setStyleSheet('font-size: 15px; color: #2a2a2a; margin-bottom: 4px;')
                main_layout.addWidget(info_label)
                main_layout.addSpacing(5)
                for stat in allowed:
                    spin = QSpinBox()
                    spin.setRange(0, points)
                    spin.setToolTip(f"Assign points to {stat}")
                    spin.setStyleSheet('font-size: 15px; min-height: 28px; border-radius: 6px; background: #eaf6ff;')
                    stat_label = QLabel(stat)
                    stat_label.setStyleSheet('font-size: 15px;')
                    asi_layout.addRow(stat_label, spin)
                    spin_boxes[stat] = spin
                asi_group.setLayout(asi_layout)
                main_layout.addWidget(asi_group)
                animation.start()
                main_layout.addSpacing(10)
                btn = QPushButton('Confirm')
                btn.setStyleSheet('font-size: 15px; font-weight: bold; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e0eaff, stop:1 #cbe6ff); border-radius: 8px; padding: 8px 18px;')
                btn.clicked.connect(dlg.accept)
                main_layout.addWidget(btn)
                dlg.setLayout(main_layout)
                while True:
                    dlg.exec()
                    total = sum(spin_boxes[stat].value() for stat in allowed)
                    if total > points:
                        from PySide6.QtWidgets import QMessageBox
                        QMessageBox.warning(dlg, 'Too Many Points', f'You assigned {total} points, but only {points} are allowed. Please adjust.')
                    else:
                        break
                for stat in allowed:
                    asi_result[stat] += spin_boxes[stat].value()

            # Choose One Of: present options as dropdown
            elif prompt['type'] == 'choose_one_of':
                options = prompt.get('options', [])
                combo = QComboBox()
                combo.addItems(options)
                combo.setToolTip("Select one option")
                combo.setStyleSheet('font-size: 15px; min-height: 28px; border-radius: 6px; background: #eaf6ff;')
                label = QLabel('Choose one option:')
                label.setStyleSheet('font-size: 15px;')
                asi_layout.addRow(label, combo)
                asi_group.setLayout(asi_layout)
                main_layout.addWidget(asi_group)
                animation.start()
                main_layout.addSpacing(10)
                btn = QPushButton('Confirm')
                btn.setStyleSheet('font-size: 15px; font-weight: bold; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e0eaff, stop:1 #cbe6ff); border-radius: 8px; padding: 8px 18px;')
                btn.clicked.connect(dlg.accept)
                main_layout.addWidget(btn)
                dlg.setLayout(main_layout)
                dlg.exec()
                chosen = combo.currentText()
                asi_sub, subprompt = self.parse_asi_string_with_prompt(chosen, prompt['source'])
                for k, v in asi_sub.items():
                    asi_result[k] += v
                # If subprompt is another prompt, recursively handle
                if subprompt and subprompt.get('type') not in [None, 'unknown']:
                    sub_result = self.prompt_asi_choices([subprompt])
                    for k, v in sub_result.items():
                        asi_result[k] += v

            # Unknown or direct assignment: show info only
            else:
                info_label = QLabel(f"Unable to parse ASI assignment. Please check the source or assign manually.")
                info_label.setWordWrap(True)
                info_label.setStyleSheet('font-size: 15px; color: #a00; background: #ffe0e0; border-radius: 8px; padding: 8px;')
                main_layout.addWidget(info_label)
                main_layout.addSpacing(10)
                btn = QPushButton('OK')
                btn.setStyleSheet('font-size: 15px; font-weight: bold; background: #ffe0e0; border-radius: 8px; padding: 8px 18px;')
                btn.clicked.connect(dlg.accept)
                main_layout.addWidget(btn)
                dlg.setLayout(main_layout)
                dlg.exec()
        return asi_result
    
    def export_character_to_pdf(self):
        import re
        selected_skills = self.get_selected_race_skills()
        if self.required_race_skills and len(selected_skills) < self.required_race_skills:
            QMessageBox.critical(self, 'Error', f'Please select {self.required_race_skills} skill proficiency(ies) for your race before exporting.')
            return
        
        try:
            from pdfrw import PdfReader, PdfWriter
        except ImportError:
            QMessageBox.critical(self, 'Error', 'pdfrw is not installed. Please run: pip install pdfrw')
            return
        char_name = self.char_name_edit.text().strip()
        alignment = self.alignment_combo.currentText()
        player_name = self.player_name_edit.text().strip()
        class_name = self.class_combo.currentText()
        level = self.level_spin.value()
        background = self.bg_combo.currentText()
        race = self.race_combo.currentText()
        display_char_name = char_name or 'Unnamed'

        proficiency_bonus = 2 
        if level >= 5:
            proficiency_bonus = 3 
        if level >= 9:
            proficiency_bonus = 4 
        if level >= 13:
            proficiency_bonus = 5 
        if level >= 17:
            proficiency_bonus = 6 
        racial_speed = ''
        racial_speed_features = ''
        for row in self.race_data:
            if row.get('name', '').strip() == race:
                speed_text = row.get('Speed', '').strip()
                if speed_text:

                    if ',' in speed_text:
                        parts = speed_text.split(',', 1)
                        racial_speed = parts[0].strip()

                        if len(parts) > 1 and parts[1].strip():
                            racial_speed_features = parts[1].strip()
                    else:
                        racial_speed = speed_text
                break

        class_hit_die = ''
        for entry in self.class_data:
            if entry.get('name', '').strip() == class_name:
                hit_die = entry.get('hit_die', '')
                if hit_die:
                    class_hit_die = hit_die
                break

        stat_names = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHA']
        base_stats = {stat: self.stat_spinboxes[i].value() for i, stat in enumerate(stat_names)}
        
        race_checked = self.asi_race_radio.isChecked() or self.asi_both_radio.isChecked()
        background_checked = self.asi_bg_radio.isChecked() or self.asi_both_radio.isChecked()
        asi = {k: 0 for k in stat_names}
        
        if race_checked:
            race_name = self.race_combo.currentText()
            for row in self.race_data:
                if row['name'].strip() == race_name:
                    asi_str = row.get('Ability Score Increase', '')
                    asi_result, _ = self.parse_asi_string_with_prompt(asi_str, 'Race')
                    for k, v in asi_result.items():
                        asi[k] += v
                    break
        
        if background_checked:
            bg_name = self.bg_combo.currentText()
            for row in self.background_data:
                if row['name'].strip() == bg_name:
                    asi_str = row.get('ability', '')
                    asi_result, _ = self.parse_asi_string_with_prompt(asi_str, 'Background')
                    for k, v in asi_result.items():
                        asi[k] += v
                    break
        
        stats = {stat: base_stats[stat] + asi.get(stat, 0) for stat in stat_names}
   
        def ability_mod(score):

            return (score - 10) // 2
        mods = {stat: ability_mod(val) for stat, val in stats.items()}

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
                                race_features.append(f)
                            else:
                                race_features.append(f)
                        break
        bg_features = []
        bg_attacks = []
        feats_data = []
        try:
            with open('Data/feats.csv', 'r', encoding='utf-8') as f_feats:
                reader_feats = csv.DictReader(f_feats)
                feats_data = list(reader_feats)
        except Exception as e:
            print(f"Error loading feats.csv: {e}")

        for row in self.background_data:
            if row['name'].strip() == background:
                print(f"[DEBUG] Selected background for PDF export: {background}")
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
                        break        # END CORRECTED LOGIC        # Extract class feature names (only names, not descriptions) for character's level
        class_feature_names = []
        for entry in self.class_data:
            if entry.get('name', '').strip() == class_name:
                features_dict = entry.get('features', {})
                for level_str in range(1, level + 1):  # Get features from level 1 up to character level
                    level_features = features_dict.get(str(level_str), [])
                    if level_features:
                        for feature in level_features:
                            feature_name = feature.get('name', '')
                            if feature_name:
                                class_feature_names.append(f"Level {level_str} - {feature_name}")
                break

        features_and_traits = ''
        
        # Add class feature names first (at the very top)
        if class_feature_names:
            features_and_traits += f"Class Features ({class_name}):\n" + '\n'.join(class_feature_names)
        
        if race_features:
            if features_and_traits:
                features_and_traits += '\n\n'
            features_and_traits += f"Race Features ({race}):\n" + '\n\n'.join(race_features)
        if bg_features:
            if features_and_traits:
                features_and_traits += '\n\n'
            features_and_traits += f"Background Features ({background}):\n" + '\n\n'.join(bg_features)
        
        # Add racial speed features if they exist
        if racial_speed_features:
            if features_and_traits:
                features_and_traits += '\n\n'
            features_and_traits += f"Racial Movement:\n{racial_speed_features}"

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
        
        # Add spells to AttacksSpellcasting field
        selected_spells = self.get_selected_spells()
        if selected_spells:
            if attacks_spellcasting:
                attacks_spellcasting += '\n\n'
            attacks_spellcasting += f"Spells ({class_name}):\n"
            
            for spell_level in sorted(selected_spells.keys(), key=lambda x: int(x.replace('0th', '0').replace('st', '').replace('nd', '').replace('rd', '').replace('th', ''))):
                spells = selected_spells[spell_level]
                if spells:
                    attacks_spellcasting += f"\n{spell_level.title()} Level:\n"
                    for spell in spells:
                        # Find spell details from spell data
                        spell_info = self.get_spell_info(spell)
                        if spell_info:
                            casting_time = spell_info.get('Casting Time', '')
                            duration = spell_info.get('Duration', '')
                            range_info = spell_info.get('Range', '')
                            components = spell_info.get('Components', '')
                            attacks_spellcasting += f"• {spell}"
                            if casting_time:
                                attacks_spellcasting += f" ({casting_time}"
                                if duration and duration != 'Instantaneous':
                                    attacks_spellcasting += f", {duration}"
                                if range_info and range_info != 'Self':
                                    attacks_spellcasting += f", {range_info}"
                                attacks_spellcasting += ")"
                            attacks_spellcasting += "\n"
                        else:
                            attacks_spellcasting += f"• {spell}\n"
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
                break        # Merge all proficiencies (race + background, no duplicates)
        all_proficiencies = set(selected_race_skills)
        all_proficiencies.update(background_skills)

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
            skill_data[skill] = f"{skill_modifier:+d}"        # Add class skill proficiencies to skill checkboxes
        selected_class_skills = self.get_selected_class_skills() if hasattr(self, 'get_selected_class_skills') else []
        for skill in selected_class_skills:
            if skill in skill_checkboxes:
                skill_checkboxes[skill] = True
            skill_data[skill] = f"{skill_modifier:+d}"

        # Handle equipment start vs gold start choice
        equipment_choice = self.prompt_equipment_choice()
        equipment_list = []
        starting_gold = 0
        
        def consolidate_equipment(items):
            """Consolidate duplicate items and format them as 'Item xN'"""
            from collections import Counter
            if not items:
                return []
            
            item_counts = Counter(items)
            consolidated = []
            for item, count in item_counts.items():
                if count > 1:
                    consolidated.append(f"{item} x{count}")
                else:
                    consolidated.append(item)
            return consolidated
        
        def process_equipment_items(items):
            """Process equipment items, handling 'simple' weapon choices"""
            processed_items = []
            for item in items:
                if item.lower() == 'simple':
                    # Prompt user to choose a simple weapon
                    selected_weapon = self.prompt_simple_weapon_choice()
                    if selected_weapon:
                        processed_items.append(selected_weapon)
                    else:
                        # User cancelled, show warning and use placeholder
                        QMessageBox.warning(self, 'Warning', 
                            'No simple weapon selected. Using "Simple Weapon" as placeholder.')
                        processed_items.append("Simple Weapon")
                else:
                    processed_items.append(item)
            return processed_items
        
        if equipment_choice == 'equipment':
            # Get starting equipment from class data
            for entry in self.class_data:
                if entry.get('name', '').strip() == class_name:
                    starting_equipment = entry.get('starting_equipment', {})
                    
                    # Add armor (consolidate duplicates)
                    armor = starting_equipment.get('armor', [])
                    processed_armor = process_equipment_items(armor)
                    equipment_list.extend(consolidate_equipment(processed_armor))
                    
                    # Add weapons (process simple weapons, then consolidate duplicates)
                    weapons = starting_equipment.get('weapons', [])
                    processed_weapons = process_equipment_items(weapons)
                    equipment_list.extend(consolidate_equipment(processed_weapons))
                      # Add gear (process simple items, then consolidate duplicates)
                    gear = starting_equipment.get('gear', [])
                    processed_gear = process_equipment_items(gear)
                    equipment_list.extend(consolidate_equipment(processed_gear))
                    
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

        # Process armor for AC calculation and features
        armor_ac = 10  # Base AC without armor
        armor_features = []
        
        # Load armor data
        armor_data = {}
        try:
            with open('Data/armor.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    armor_name = row.get('Name', '').strip()
                    if armor_name:
                        armor_data[armor_name.lower()] = {
                            'ac_formula': row.get('Damage', '').strip(),  # AC formula is in Damage column
                            'text': row.get('Text', '').strip()
                        }
        except Exception as e:
            print(f"Warning: Could not load armor.csv: {e}")
        
        # Find armor in equipment list and calculate AC
        for item in equipment_list:
            item_lower = item.lower()
            for armor_name, armor_info in armor_data.items():
                if armor_name in item_lower:
                    ac_formula = armor_info['ac_formula']
                    armor_text = armor_info['text']
                    
                    if ac_formula:
                        # Parse AC formula (e.g., "AC 14 + Dex (max 2)", "AC 18", "AC 11 + Dex")
                        dex_mod = mods['DEX']
                        
                        if 'AC' in ac_formula:
                            # Extract base AC number
                            import re
                            ac_match = re.search(r'AC\s*(\d+)', ac_formula)
                            if ac_match:
                                base_ac = int(ac_match.group(1))
                                
                                if '+ Dex' in ac_formula:
                                    # Check for max dex bonus
                                    max_match = re.search(r'max\s*(\d+)', ac_formula)
                                    if max_match:
                                        max_dex = int(max_match.group(1))
                                        effective_dex_mod = min(dex_mod, max_dex)
                                    else:
                                        effective_dex_mod = dex_mod
                                    if effective_dex_mod > 0:
                                        armor_ac = base_ac + effective_dex_mod
                                    else:
                                        armor_ac = base_ac
                                else:
                                    armor_ac = base_ac
                    
                    # Add armor text to features if it exists
                    if armor_text:
                        armor_features.append(f"{item}: {armor_text}")
                    
                    break  # Found matching armor, stop searching
          # Add armor information to Features and Traits
        if armor_features:
            if features_and_traits:
                features_and_traits += "\n\nArmor Information:\n"
            else:
                features_and_traits = "Armor Information:\n"
            features_and_traits += "\n".join(armor_features)

        # Prompt for HP calculation method
        hp_max = 0
        hp_current = 0
        
        # Get hit die for calculations        hit_die_num = 8  # Default d8
        if class_hit_die:
            import re
            hit_die_match = re.search(r'd(\d+)', class_hit_die)
            if hit_die_match:
                hit_die_num = int(hit_die_match.group(1))
        
        from PySide6.QtWidgets import QMessageBox, QInputDialog
        msg = QMessageBox(self)
        msg.setWindowTitle('HP Calculation')
        msg.setText('How would you like to calculate hit points?')
        manual_btn = msg.addButton('Manual Entry', QMessageBox.ActionRole)
        average_btn = msg.addButton('Average HP', QMessageBox.ActionRole)
        roll_btn = msg.addButton('Roll for HP', QMessageBox.ActionRole)
        msg.exec()
        
        if msg.clickedButton() == manual_btn:
            # Manual HP entry
            hp_max, ok = QInputDialog.getInt(self, 'Manual HP Entry', 'Enter maximum hit points:', 
                                           8 + mods['CON'])
            if ok and hp_max >= 1:  # Validate minimum value
                hp_current = hp_max
            else:
                hp_max = 8 + mods['CON']  # Default fallback
                hp_current = hp_max
                
        elif msg.clickedButton() == average_btn:
            # Calculate average HP: max at 1st level + average of hit die for remaining levels
            first_level_hp = hit_die_num + mods['CON']
            if level > 1:
                average_per_level = (hit_die_num // 2) + 1 + mods['CON']
                additional_hp = (level - 1) * average_per_level
                hp_max = first_level_hp + additional_hp
            else:
                hp_max = first_level_hp
            hp_current = hp_max
            
        else:  # roll_btn or default
            # Roll for HP: max at 1st level + roll for each additional level
            import random
            first_level_hp = hit_die_num + mods['CON']
            hp_max = first_level_hp
            
            if level > 1:
                rolled_hp = []
                for i in range(level - 1):
                    roll = random.randint(1, hit_die_num)
                    rolled_hp.append(roll)
                    hp_max += roll + mods['CON']
                
                # Show the user what was rolled
                rolls_text = ', '.join(map(str, rolled_hp))
                QMessageBox.information(self, 'HP Rolls', 
                    f'Rolled {rolls_text} for levels 2-{level}\n'
                    f'Total HP: {hp_max} (includes CON modifier)')
            
            hp_current = hp_max        # Add spell slots and cantrips information
        spell_slots_info = ''
        caster_type = self.get_caster_type(class_name)
        if caster_type:
            spell_slots = self.get_spell_slots(caster_type, level)
            if spell_slots:
                # Handle different caster types
                if caster_type == 'warlock':  # Warlock
                    slots = spell_slots.get('slots', 0)
                    slot_level = spell_slots.get('slot_level', '1st')
                    if slots > 0:
                        spell_slots_info = f'Spell Slots: {slots} {slot_level} level'
                else:
                    # Format spell slots for regular casters
                    slot_parts = []
                    for slot_level, count in spell_slots.items():
                        if slot_level not in ['slots', 'slot_level']:
                            slot_parts.append(f"{slot_level}: {count}")
                    if slot_parts:
                        spell_slots_info = 'Spell Slots: ' + ', '.join(slot_parts)
                
                # Add cantrips known
                cantrips_known = self.get_cantrips_known(class_name, level)
                if cantrips_known > 0:
                    if spell_slots_info:
                        spell_slots_info += f'\nCantrips Known: {cantrips_known}'
                    else:
                        spell_slots_info = f'Cantrips Known: {cantrips_known}'

        pdf_data = {
            'CharacterName': display_char_name,
            'ClassLevel': f'{class_name} {level}',
            'Background': background,
            'PlayerName': player_name,
            'Race ': race,
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
            'Equipment': '\n'.join(equipment_list),            'Features and Traits': features_and_traits,
            'AttacksSpellcasting': attacks_spellcasting,
            'ProficienciesLang': race_languages,
            'SpellSlots': spell_slots_info,# Passive Perception (WIS mod + 10)
            'Passive': str(10 + mods['WIS']),            # AC, Initiative, Speed, HP, etc.
            'AC': str(armor_ac),
            'Initiative': f"{mods['DEX']:+d}",
            'Speed': racial_speed,
            'HPMax': str(hp_max),
            'HPCurrent': str(hp_current),
            'HPTemp': '',# Proficiency bonus and hit die
            'ProfBonus': f"+{proficiency_bonus}",
            'HD': class_hit_die,
            'HDTotal': f"{level}{class_hit_die}" if class_hit_die else f"{level}d8",
            # Currency (placeholders)
            'CP': '', 'SP': '', 'EP': '', 'GP': str(starting_gold), 'PP': '',
        }

        current_prof_lang_text = str(race_languages).replace('\\\\n', '\\n')

        if 'extracted_lines_for_prof_lang' in locals() and isinstance(extracted_lines_for_prof_lang, list) and extracted_lines_for_prof_lang:
            # Join the extracted lines with a single newline character
            additional_text = '\n'.join(extracted_lines_for_prof_lang)
            
            # Append additional_text to current_prof_lang_text
            if current_prof_lang_text and additional_text: # Both have content
                current_prof_lang_text += '\n' + additional_text
            elif additional_text:
                current_prof_lang_text = additional_text
        class_proficiencies = []
        for entry in self.class_data:
            if entry.get('name', '').strip() == class_name:
                proficiencies = entry.get('proficiencies', {})
                armor_profs = proficiencies.get('armor', [])
                for armor in armor_profs:
                    if armor.strip():
                        if armor.lower() == 'shields':
                            class_proficiencies.append(armor.capitalize())
                        else:
                            class_proficiencies.append(f"{armor.capitalize()} armor")
                
                weapon_profs = proficiencies.get('weapons', [])
                for weapon in weapon_profs:
                    if weapon.strip():
                        if weapon.lower() == 'firearms':
                            class_proficiencies.append(weapon.capitalize())
                        else:
                            class_proficiencies.append(f"{weapon.capitalize()} weapons")
                tool_profs = proficiencies.get('tools', [])
                for tool in tool_profs:
                    if tool.strip():
                        if tool.lower() == 'artisanchoice':
                            selected_artisan_tool = self.prompt_artisan_tool_choice()
                            if selected_artisan_tool:
                                class_proficiencies.append(selected_artisan_tool)
                            else:
                                QMessageBox.warning(self, 'Warning', 
                                    'No artisan tool selected. Using "Artisan\'s Tools" as placeholder.')
                                class_proficiencies.append("Artisan's Tools")
                        elif tool.lower() == 'artisaninstrumentchoice':
                            selected_tool_or_instrument = self.prompt_artisan_or_instrument_choice()
                            if selected_tool_or_instrument:
                                class_proficiencies.append(selected_tool_or_instrument)
                            else:
                                QMessageBox.warning(self, 'Warning', 
                                    'No tool/instrument selected. Using "Artisan\'s Tools or Musical Instrument" as placeholder.')
                                class_proficiencies.append("Artisan's Tools or Musical Instrument")
                        else:
                            class_proficiencies.append(tool.capitalize())
                break

        if class_proficiencies:
            class_prof_text = '\n'.join(class_proficiencies)
            if current_prof_lang_text:
                current_prof_lang_text += '\n' + class_prof_text
            else:
                current_prof_lang_text = class_prof_text
        pdf_data['ProficienciesLang'] = current_prof_lang_text
        selected_class_name = self.class_combo.currentText()
        class_saving_throws = []
        if hasattr(self, 'class_data'):
            for c_data in self.class_data:
                if c_data.get('name') == selected_class_name:
                    class_saving_throws = [s.lower() for s in c_data.get('saving_throws', [])]
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

        skill_checkbox_order = [
            'Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception', 'History',
            'Insight', 'Intimidation', 'Investigation', 'Medicine', 'Nature', 'Perception',
            'Performance', 'Persuasion', 'Religion', 'Sleight of Hand', 'Stealth', 'Survival'
        ]
        for i, skill in enumerate(skill_checkbox_order, start=23):
            pdf_data[f'Check Box {i}'] = 'Yes' if skill_checkboxes.get(skill, False) else 'Off'
        weapon_data = {}
        try:
            with open('Data/weapons_no_desc.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    weapon_name = row['Name'].strip()
                    weapon_data[weapon_name.lower()] = {
                        'name': weapon_name,
                        'type': row.get('Type', ''),
                        'damage': row.get('Damage', ''),
                        'properties': row.get('Properties', '')
                    }
        except Exception as e:
            print(f"Error loading weapons_no_desc.csv: {e}") 
        class_weapon_profs = set()
        for entry in self.class_data:
            if entry.get('name', '').strip() == class_name:
                proficiencies = entry.get('proficiencies', {})
                weapon_profs = proficiencies.get('weapons', [])
                for weapon_type in weapon_profs:
                    class_weapon_profs.add(weapon_type.lower().strip())
                break

        filled_weapons = []
        for item in equipment_list:
            clean_item = item.split(' x')[0].strip()
            weapon_key = clean_item.lower()
            
            if weapon_key in weapon_data:
                weapon = weapon_data[weapon_key]
                properties = weapon.get('properties', '').lower()
                weapon_type = weapon.get('type', '').lower()
                damage = weapon.get('damage', '')
                
                is_proficient = False
                if 'simple weapon' in weapon_type and 'simple' in class_weapon_profs:
                    is_proficient = True
                elif 'martial weapon' in weapon_type and 'martial' in class_weapon_profs:
                    is_proficient = True
                
                if 'ranged weapon' in weapon_type:
                    ability_mod = mods['DEX']
                elif 'finesse' in properties:
                    ability_mod = max(mods['STR'], mods['DEX'])
                else:
                    ability_mod = mods['STR']
                
                attack_bonus = ability_mod + (proficiency_bonus if is_proficient else 0)
                attack_bonus_str = f"{attack_bonus:+d}"
                
                import re
                if damage:
                    damage_match = re.match(r'(\d+d\d+)', damage)
                    if damage_match:
                        damage_dice = damage_match.group(1)
                        damage_type = damage.replace(damage_dice, '').strip()
                        if ability_mod != 0:
                            damage_str = f"{damage_dice}{ability_mod:+d} {damage_type}"
                        else:
                            damage_str = f"{damage_dice} {damage_type}"
                    else:
                        damage_str = damage
                else:
                    damage_str = ""
                
                filled_weapons.append({
                    'name': clean_item,
                    'attack_bonus': attack_bonus_str,
                    'damage': damage_str
                })
                
                # Only fill up to 3 weapons
                if len(filled_weapons) >= 3:
                    break

        # Fill PDF fields for up to 3 weapons
        for i, weapon in enumerate(filled_weapons):
            if i == 0:
                pdf_data['Wpn Name'] = weapon['name']
                pdf_data['Wpn1 AtkBonus'] = weapon['attack_bonus']
                pdf_data['Wpn1 Damage'] = weapon['damage']
            else:
                pdf_data[f'Wpn Name {i+1}'] = weapon['name']
                if i == 1:
                    pdf_data[f'Wpn{i+1} AtkBonus '] = weapon['attack_bonus']
                else:
                    pdf_data[f'Wpn{i+1} AtkBonus  '] = weapon['attack_bonus']
                pdf_data[f'Wpn{i+1} Damage '] = weapon['damage']        # Map selected spells to specific PDF fields
        selected_spells = self.get_selected_spells()
        if selected_spells:
            # Define spell field mappings for each spell level
            spell_field_mappings = {
                'Cantrips': ['Spells 1014'] + [f'Spells 10{i}' for i in range(16, 23)],  # 1014, 1016-1022
                '1': ['Spells 1015'] + [f'Spells 10{i}' for i in range(23, 34)],        # 1015, 1023-1033
                '2': [f'Spells 10{i}' for i in range(34, 47)],                   # 1034-1046
                '3': [f'Spells 10{i}' for i in range(47, 60)],                   # 1047-1059
                '4': [f'Spells 10{i}' for i in range(61, 73)],                   # 1061-1072
                '5': [f'Spells 10{i}' for i in range(73, 82)],                   # 1073-1081
                '6': [f'Spells 10{i}' for i in range(82, 91)],                   # 1082-1090
                '7': [f'Spells 10{i}' for i in range(91, 100)],                  # 1091-1099
                '8': [f'Spells 101{i:02d}' for i in range(0, 7)],                # 10100-10106
                '9': [f'Spells 101{i:02d}' for i in range(7, 14)]                # 10107-101013
            }
              # Map each spell level to its corresponding PDF fields
            for spell_level, spells in selected_spells.items():
                # Normalize spell level (handle "0th", "Cantrips", "1st", "2nd", etc.)
                if spell_level.lower() in ['cantrips', '0th']:
                    level_key = 'Cantrips'
                else:
                    # Extract numeric part from level (e.g., "1st" -> "1")
                    level_match = re.match(r'(\d+)', spell_level)
                    if level_match:
                        level_key = level_match.group(1)
                    else:
                        continue
                  # Get the field list for this spell level
                if level_key in spell_field_mappings:
                    field_list = spell_field_mappings[level_key]
                      # Map each spell to a field (up to the number of available fields)
                    for i, spell_name in enumerate(spells):
                        if i < len(field_list):
                            field_id = field_list[i]
                            
                            # Get additional spell information
                            spell_info = self.get_spell_info(spell_name)
                            if spell_info:
                                casting_time = spell_info.get('Casting Time', '').strip()
                                range_info = spell_info.get('Range', '').strip()
                                components = spell_info.get('Components', '').strip()
                                
                                # Format: "Spell Name, Casting Time, Range, (Components)"
                                formatted_spell = spell_name
                                if casting_time:
                                    formatted_spell += f" ({casting_time}"
                                if range_info:
                                    formatted_spell += f", {range_info}"
                                if components:
                                    formatted_spell += f", ({components})"
                                
                                pdf_data[field_id] = formatted_spell
                                print(f"DEBUG: Mapped spell '{formatted_spell}' to field '{field_id}' for level {level_key}")
                            else:
                                # Fallback to just spell name if spell info not found
                                pdf_data[field_id] = spell_name
                                print(f"DEBUG: Mapped spell '{spell_name}' (no details found) to field '{field_id}' for level {level_key}")
                else:
                    print(f"DEBUG: No field mapping found for spell level '{level_key}'")

          # Personality, ideals, bonds, flaws (placeholders, could add UI fields)
        # Equipment and features (placeholders, could add UI fields)
        # Currency (placeholders)
        template_path = 'Templates/character_sheet_template.pdf'
        
        # Determine output filename
        if char_name:
            output_path = f"Characters/{char_name.replace(' ', '_')}.pdf"
        else:
            output_path = f"Characters/{race}_{class_name}.pdf".replace(' ', '_')
        
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

    def prompt_simple_weapon_choice(self):
        """Prompt user to choose a simple weapon from available options"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
        
        simple_weapons = [
            "Club",
            "Dagger", 
            "Greatclub",
            "Handaxe",
            "Javelin",
            "Light hammer",
            "Mace",
            "Quarterstaff",
            "Spear"
        ]
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Choose Simple Weapon")
        dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        label = QLabel("Your starting equipment includes a simple weapon.\nPlease select a simple weapon:")
        layout.addWidget(label)
        
        combo = QComboBox()
        combo.addItems(simple_weapons)
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

    def on_race_changed(self):
        race_name = self.race_combo.currentText()
        chosen = []
        for row in self.race_data:
            if row['name'].strip() == race_name:
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
                        options = [opt.strip() for opt in prof_choice.split(',')[:-1]]
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

    def update_spell_selection(self):
        """Update spell selection UI based on current class and level"""
        class_name = self.class_combo.currentText()
        level = self.level_spin.value()
        
        print(f"[DEBUG] update_spell_selection: class_name='{class_name}', level={level}")
        
        # Clear existing spell widgets
        for widget_list in self.spell_widgets.values():
            for widget in widget_list:
                widget.deleteLater()
        self.spell_widgets.clear()
        
        # Clear the layout
        while self.spell_levels_layout.count():
            item = self.spell_levels_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
          # Check if class is a spellcaster
        caster_type = self.get_caster_type(class_name)
        print(f"[DEBUG] caster_type: {caster_type}")
        if not caster_type or caster_type == "none":
            self.spell_info_label.setText('This class does not cast spells.')
            return
        
        # Get spell slots for this level
        spell_slots = self.get_spell_slots(caster_type, level)
        print(f"[DEBUG] spell_slots: {spell_slots}")
        if not spell_slots:
            self.spell_info_label.setText('No spell slots available at this level.')
            return

        class_spells = self.get_class_spells(class_name)
        print(f"[DEBUG] class_spells keys: {list(class_spells.keys()) if class_spells else 'None'}")
        if not class_spells:
            self.spell_info_label.setText('No spells available for this class.')
            return

        slot_info = ', '.join([f"{slots} {spell_level}" for spell_level, slots in spell_slots.items()])
        self.spell_info_label.setText(f'Spell Slots: {slot_info}')

        cantrips_known = self.get_cantrips_known(class_name, level)
        if cantrips_known > 0:
            self.create_spell_level_section('0th', class_spells, class_name)
        
        # Warlock special case: handle slot_level/slots keys
        if 'slot_level' in spell_slots and 'slots' in spell_slots:
            spell_level = spell_slots['slot_level']
            self.create_spell_level_section(spell_level, class_spells, class_name)
        else:
            for spell_level in sorted(
                [k for k in spell_slots.keys() if k.replace('st', '').replace('nd', '').replace('rd', '').replace('th', '').isdigit()],
                key=lambda x: int(x.replace('st', '').replace('nd', '').replace('rd', '').replace('th', ''))
            ):
                self.create_spell_level_section(spell_level, class_spells, class_name)

         
    
    def get_caster_type(self, class_name):
        """Get the caster type for a class"""
        print(f"[DEBUG] get_caster_type: class_name='{class_name}'")
        print(f"[DEBUG] Available classes: {[entry.get('name', '') for entry in self.class_data]}")
        for entry in self.class_data:
            if entry.get('name', '').strip() == class_name:
                caster_type = entry.get('caster_type')
                print(f"[DEBUG] Found class, caster_type: {caster_type}")
                return caster_type
        print(f"[DEBUG] Class not found in class_data")
        return None
    
    def get_spell_slots(self, caster_type, level):
        print(f"[DEBUG] get_spell_slots: caster_type='{caster_type}', level={level}")

        caster_type_map = {
            'full': 'full_caster',
            'half': 'half_caster', 
            'third': 'third_caster',
            'pact': 'pact_caster'
        }
        
        table_key = caster_type_map.get(caster_type, caster_type)
        print(f"[DEBUG] table_key: {table_key}")
        
        try:
            with open('Data/classes.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                spell_tables = data.get('spell_slot_tables', {})
                print(f"[DEBUG] Available spell table keys: {list(spell_tables.keys())}")
                if table_key in spell_tables:
                    progression = spell_tables[table_key].get('progression', {})
                    result = progression.get(str(level), {})
                    print(f"[DEBUG] Spell slots result: {result}")
                    return result
        except Exception as e:
            print(f"[DEBUG] Exception in get_spell_slots: {e}")
        return {}
    
    def get_class_spells(self, class_name):
        print(f"[DEBUG] get_class_spells: class_name='{class_name}'")
        if not self.spell_data:
            print(f"[DEBUG] No spell data loaded")
            return {}
        
        print(f"[DEBUG] Total spells in data: {len(self.spell_data)}")

        class_spells = {}
        spell_count = 0
        for spell in self.spell_data:
            spell_classes = spell.get('Classes', '') + ' ' + spell.get('Optional/Variant Classes', '')
            if class_name in spell_classes:
                spell_count += 1
                level = spell.get('Level', '')
                if level == 'Cantrip':
                    level = '0th'
                elif not level.endswith(('st', 'nd', 'rd', 'th')):
                    level += 'th'
                
                if level not in class_spells:
                    class_spells[level] = []
                class_spells[level].append(spell)
        
        print(f"[DEBUG] Found {spell_count} spells for {class_name}")
        print(f"[DEBUG] Spell levels available: {list(class_spells.keys())}")
        return class_spells
    
    def create_spell_level_section(self, spell_level, class_spells, class_name):
        from PySide6.QtWidgets import QCheckBox
        available_spells = class_spells.get(spell_level, [])
        if not available_spells:
            return

        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)

        display_level = "Cantrip" if spell_level == "0th" else f"{spell_level.title()} Level"
        header_label = QLabel(f'{display_level} Spells')
        header_label.setStyleSheet('font-weight: bold; font-size: 11pt;')
        section_layout.addWidget(header_label)

        if spell_level == '0th':
            num_spells = self.get_cantrips_known(class_name, self.level_spin.value())
        else:
            spell_slots = self.get_spell_slots(self.get_caster_type(class_name), self.level_spin.value())
            num_spells = spell_slots.get(spell_level, 0)

        if num_spells <= 0:
            return

        print(f"[DEBUG] Number of spells to select for {spell_level}: {num_spells}")
        info_label = QLabel(f'Select {num_spells} spells:')
        section_layout.addWidget(info_label)

        spell_checkboxes = []
        grid_layout = QGridLayout()
        for i, spell in enumerate(sorted(available_spells, key=lambda x: x.get('Name', ''))):
            spell_name = spell.get('Name', '')
            if spell_name:
                cb = QCheckBox(spell_name)
                cb.setFixedSize(140, 36)
                cb.setStyleSheet('QCheckBox { align-items: left; min-width: 120px; min-height: 28px; max-width: 140px; max-height: 36px; border: 1px solid #888; border-radius: 6px; padding: 6px; background: #eee; } QCheckBox::indicator { width: 0; height: 0; } QCheckBox:checked { background: #aaf; border: 2px solid #44f; }')
                spell_checkboxes.append(cb)
                row = i // 8
                col = i % 8
                grid_layout.addWidget(cb, row, col)
        section_layout.addLayout(grid_layout)

        # Limit selection to num_spells
        def enforce_limit():
            checked = [cb for cb in spell_checkboxes if cb.isChecked()]
            if len(checked) >= num_spells:
                for cb in spell_checkboxes:
                    if not cb.isChecked():
                        cb.setEnabled(False)
            else:
                for cb in spell_checkboxes:
                    cb.setEnabled(True)
        for cb in spell_checkboxes:
            cb.stateChanged.connect(enforce_limit)
        # Initial enforcement
        enforce_limit()

        if spell_level not in self.spell_widgets:
            self.spell_widgets[spell_level] = []
        self.spell_widgets[spell_level].extend(spell_checkboxes)

        self.spell_levels_layout.addWidget(section_widget)
    
    def get_cantrips_known(self, class_name, level):
        cantrip_progression = {
            'Bard': {1: 2, 4: 3, 10: 4},
            'Cleric': {1: 3, 4: 4, 10: 5},
            'Druid': {1: 2, 4: 3, 10: 4},
            'Sorcerer': {1: 4, 4: 5, 10: 6},
            'Warlock': {1: 2, 4: 3, 10: 4},
            'Wizard': {1: 3, 4: 4, 10: 5},
            'Artificer': {1: 2, 6: 3, 14: 4},
        }
        
        if class_name not in cantrip_progression:
            return 0
        
        progression = cantrip_progression[class_name]
        cantrips = 0
        for req_level in sorted(progression.keys(), reverse=True):
            if level >= req_level:
                cantrips = progression[req_level]
                break
        
        return cantrips
    
    def get_spells_known(self, class_name, level, spell_level):
        
        prepared_casters = ['Cleric', 'Druid', 'Wizard', 'Artificer', 'Paladin', 'Ranger']
        
        if class_name in prepared_casters:

            return min(level + 1, 10)  
        else:
            known_progression = {
                1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10,
                10: 11, 11: 12, 12: 12, 13: 13, 14: 13, 15: 14, 16: 14,
                17: 15, 18: 15, 19: 15, 20: 15
            }
            return known_progression.get(level, 2)
    
    def get_selected_spells(self):
        selected = {}
        for spell_level, widgets in self.spell_widgets.items():
            spells = []
            for widget in widgets:
                if isinstance(widget, QCheckBox):
                    if widget.isChecked():
                        spells.append(widget.text())
                elif hasattr(widget, 'currentText'):
                    spell = widget.currentText()
                    if spell and spell != '-- Select Spell --':
                        spells.append(spell)
            if spells:
                selected[spell_level] = spells
        return selected
    
    def get_spell_info(self, spell_name):
        for spell in self.spell_data:
            if spell.get('Name', '').strip() == spell_name:
                return spell
        return None

def gui_main():
    app = QApplication(sys.argv)
    window = CharacterCreator()
    window.setWindowTitle('D&D Character Creator')
    window.setGeometry(100, 100, 1780, 1000)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    gui_main()
