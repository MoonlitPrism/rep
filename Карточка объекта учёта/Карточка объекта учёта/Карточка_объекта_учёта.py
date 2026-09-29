import sys
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QComboBox,
    QSpinBox, QCheckBox, QSlider, QPushButton, QMessageBox,
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, QGridLayout,
    QDateEdit, QTextEdit
)


class InventoryCardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Карточка объекта учёта — Форма № 423-АПК")
        self.resize(720, 600)

        central = QWidget()
        self.setCentralWidget(central)
        self.main_layout = QVBoxLayout(central)

        self._build_org_group()
        self._build_object_group()
        self._build_params_group()
        self._build_extra_group()
        self._build_buttons()
        self._build_status_bar()

        self._connect_signals()
        self._reset_form()

    def _build_org_group(self):
        group = QGroupBox("Организация")
        form = QFormLayout(group)

        self.org_edit = QLineEdit("ООО «Сельпром»")
        self.org_edit.setPlaceholderText("Введите наименование организации")

        self.subdivision_combo = QComboBox()
        self.subdivision_combo.addItems(["Ферма №2"])

        self.mol_edit = QLineEdit("Кладовщик Семенов Иван Иванович")

        form.addRow("Организация:", self.org_edit)
        form.addRow("Структурное подразделение:", self.subdivision_combo)
        form.addRow("Материально ответственное лицо:", self.mol_edit)

        self.main_layout.addWidget(group)

    def _build_object_group(self):
        group = QGroupBox("Объект учёта")
        form = QFormLayout(group)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Например: Лопата штыковая")

        self.inventory_edit = QLineEdit()
        self.inventory_edit.setPlaceholderText("Например: ИНВ-000123")

        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "Инструмент для земляных работ (ручной)",
        ])

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        form.addRow("Наименование объекта *:", self.name_edit)
        form.addRow("Инвентарный номер:", self.inventory_edit)
        form.addRow("Группа имущества:", self.category_combo)
        form.addRow("Дата постановки на учёт:", self.date_edit)

        self.main_layout.addWidget(group)

    def _build_params_group(self):
        group = QGroupBox("Параметры")
        grid = QGridLayout(group)

        grid.addWidget(QLabel("Срок полезного использования (мес.):"), 0, 0)
        self.life_spin = QSpinBox()
        self.life_spin.setRange(1, 120)
        self.life_spin.setValue(36)
        self.life_spin.setSuffix(" мес.")
        grid.addWidget(self.life_spin, 0, 1)

        grid.addWidget(QLabel("Количество, ед.:"), 1, 0)
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, 1000)
        self.qty_spin.setValue(1)
        grid.addWidget(self.qty_spin, 1, 1)

        grid.addWidget(QLabel("Износ, %:"), 2, 0)
        self.wear_slider = QSlider(Qt.Horizontal)
        self.wear_slider.setRange(0, 100)
        self.wear_slider.setValue(0)
        self.wear_label = QLabel("0 %")
        self.wear_label.setMinimumWidth(50)
        slider_box = QHBoxLayout()
        slider_box.addWidget(self.wear_slider)
        slider_box.addWidget(self.wear_label)
        grid.addLayout(slider_box, 2, 1)

        self.repair_check = QCheckBox("Требуется ремонт")
        grid.addWidget(self.repair_check, 3, 0, 1, 2)

        self.working_check = QCheckBox("В эксплуатации")
        self.working_check.setChecked(True)
        grid.addWidget(self.working_check, 4, 0, 1, 2)

        self.main_layout.addWidget(group)

    def _build_extra_group(self):
        group = QGroupBox("Примечание")
        layout = QVBoxLayout(group)
        self.note_edit = QTextEdit()
        self.note_edit.setPlaceholderText("Дополнительная информация об объекте...")
        self.note_edit.setFixedHeight(70)
        layout.addWidget(self.note_edit)
        self.main_layout.addWidget(group)

    def _build_buttons(self):
        box = QHBoxLayout()

        self.save_btn = QPushButton("Сохранить")
        self.clear_btn = QPushButton("Очистить")
        self.exit_btn = QPushButton("Выход")

        box.addWidget(self.save_btn)
        box.addWidget(self.clear_btn)
        box.addStretch()
        box.addWidget(self.exit_btn)

        self.main_layout.addLayout(box)

    def _build_status_bar(self):
        self.status = self.statusBar()
        self.status.showMessage("Готово")

    def _connect_signals(self):
        self.clear_btn.clicked.connect(self.name_edit.clear)
        self.clear_btn.clicked.connect(self._reset_form)

        self.name_edit.textChanged.connect(self._on_name_changed)
        self.category_combo.currentIndexChanged.connect(self._on_category_changed)
        self.life_spin.valueChanged.connect(self._on_life_changed)
        self.wear_slider.valueChanged.connect(self._on_wear_changed)
        self.repair_check.toggled.connect(self._on_repair_toggled)
        self.working_check.toggled.connect(self._on_working_toggled)

        self.save_btn.clicked.connect(self._on_save)
        self.exit_btn.clicked.connect(self.close)

    def _on_name_changed(self, text: str):
        if text.strip():
            self.status.showMessage(f"Введено название: {text}")
        else:
            self.status.showMessage("Название объекта не заполнено")

    def _on_category_changed(self, index: int):
        self.status.showMessage(
            f"Выбрана группа: {self.category_combo.currentText()}"
        )

    def _on_life_changed(self, value: int):
        years = value // 12
        months = value % 12
        self.status.showMessage(
            f"Срок службы: {value} мес. (~{years} г. {months} мес.)"
        )

    def _on_wear_changed(self, value: int):
        self.wear_label.setText(f"{value} %")
        self.status.showMessage(f"Износ: {value} %")

    def _on_repair_toggled(self, checked: bool):
        self.status.showMessage(
            "Объект требует ремонта" if checked else "Ремонт не требуется"
        )

    def _on_working_toggled(self, checked: bool):
        self.status.showMessage(
            "Объект в эксплуатации" if checked else "Объект не эксплуатируется"
        )

    def _on_save(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(
                self,
                "Ошибка заполнения",
                "Необходимо заполнить название объекта",
            )
            self.name_edit.setFocus()
            return

        info = (
            f"Объект: {name}\n"
            f"Организация: {self.org_edit.text()}\n"
            f"Подразделение: {self.subdivision_combo.currentText()}\n"
            f"Группа: {self.category_combo.currentText()}\n"
            f"Инв. номер: {self.inventory_edit.text() or '—'}\n"
            f"Количество: {self.qty_spin.value()} ед.\n"
            f"Срок службы: {self.life_spin.value()} мес.\n"
            f"Износ: {self.wear_slider.value()} %\n"
            f"Требуется ремонт: {'да' if self.repair_check.isChecked() else 'нет'}\n"
            f"В эксплуатации: {'да' if self.working_check.isChecked() else 'нет'}"
        )
        QMessageBox.information(self, "Данные сохранены", info)
        self.status.showMessage(f"Сохранено: {name}")

    def _reset_form(self):
        self.name_edit.clear()
        self.inventory_edit.clear()
        self.note_edit.clear()

        self.subdivision_combo.setCurrentIndex(0)
        self.category_combo.setCurrentIndex(0)

        self.life_spin.setValue(36)
        self.qty_spin.setValue(1)

        self.repair_check.setChecked(False)
        self.working_check.setChecked(True)

        self.wear_slider.setValue(0)
        self.wear_label.setText("0 %")

        self.org_edit.setText("ООО «Сельпром»")
        self.mol_edit.setText("Кладовщик Семенов Иван Иванович")
        self.date_edit.setDate(QDate.currentDate())

        self.status.showMessage("Форма очищена")


def main():
    app = QApplication(sys.argv)
    window = InventoryCardWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()