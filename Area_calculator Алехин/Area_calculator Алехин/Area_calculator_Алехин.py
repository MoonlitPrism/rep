import sys
import math

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QMessageBox,
    QDialog,
    QTextEdit
)
from PySide6.QtCore import Qt

class HelpDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Справка")
        self.setFixedSize(450, 400)

        layout = QVBoxLayout()

        title = QLabel("Формулы для вычислений")
        title.setAlignment(Qt.AlignCenter)

        text = QTextEdit()
        text.setReadOnly(True)

        text.setPlainText(
            "КРУГ\n"
            "Площадь: S = π · r²\n"
            "Длина окружности: P = 2 · π · r\n\n"

            "КВАДРАТ\n"
            "Площадь: S = a²\n"
            "Периметр: P = 4 · a\n\n"

            "ТРЕУГОЛЬНИК\n"
            "Периметр: P = a + b + c\n"
            "Площадь по формуле Герона:\n"
            "p = (a + b + c) / 2\n"
            "S = √(p · (p-a) · (p-b) · (p-c))\n\n"

            "КУБ\n"
            "Площадь поверхности: S = 6 · a²\n"
            "Периметр: P = 12 · a\n"
            "Объём: V = a³\n\n"

            "ШАР\n"
            "Площадь поверхности: S = 4 · π · r²\n"
            "Объём: V = 4/3 · π · r³"
        )

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addWidget(text)
        layout.addWidget(close_button)

        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Расчёт геометрических фигур")
        self.setMinimumSize(550, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

        title = QLabel("Расчёт параметров геометрических фигур")
        title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title)

        figure_layout = QHBoxLayout()
        figure_label = QLabel("Выберите фигуру:")

        self.figure_combo = QComboBox()
        self.figure_combo.addItems([
            "Круг",
            "Квадрат",
            "Треугольник",
            "Куб",
            "Шар"
        ])
        self.figure_combo.currentTextChanged.connect(self.update_fields)

        figure_layout.addWidget(figure_label)
        figure_layout.addWidget(self.figure_combo)
        self.main_layout.addLayout(figure_layout)

        self.form_container = None
        self.form_layout = None
        self.inputs = []
        self.form_index = self.main_layout.count()   # = 2

        self._create_form_container()

        self.calculate_button = QPushButton("Рассчитать")
        self.calculate_button.clicked.connect(self.calculate)
        self.main_layout.addWidget(self.calculate_button)

        result_title = QLabel("Результат:")
        self.main_layout.addWidget(result_title)

        self.result_label = QLabel("Здесь появится результат расчёта.")
        self.result_label.setAlignment(Qt.AlignTop)
        self.result_label.setWordWrap(True)
        self.main_layout.addWidget(self.result_label)

        self.help_button = QPushButton("Справка")
        self.help_button.clicked.connect(self.show_help)
        self.main_layout.addWidget(self.help_button)

        self.update_fields("Круг")

    def _create_form_container(self):
        self.form_container = QWidget()
        self.form_layout = QFormLayout(self.form_container)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.insertWidget(self.form_index, self.form_container)

    def clear_fields(self):
        if self.form_container is not None:
            self.main_layout.removeWidget(self.form_container)
            self.form_container.deleteLater()
            self.form_container = None
            self.form_layout = None

        self.inputs.clear()
        self._create_form_container()

    def update_fields(self, figure):
        self.clear_fields()

        if figure == "Круг":
            labels = ["Радиус:"]
        elif figure == "Квадрат":
            labels = ["Сторона:"]
        elif figure == "Треугольник":
            labels = ["Сторона a:", "Сторона b:", "Сторона c:"]
        elif figure == "Куб":
            labels = ["Ребро:"]
        elif figure == "Шар":
            labels = ["Радиус:"]
        else:
            labels = []

        for label in labels:
            field = QLineEdit()
            field.setMinimumWidth(150)
            self.inputs.append(field)
            self.form_layout.addRow(label, field)

        self.result_label.setText("Здесь появится результат расчёта.")

    def get_number(self, index):
        try:
            value = float(self.inputs[index].text())
            if value <= 0:
                raise ValueError
            return value
        except (ValueError, IndexError):
            raise ValueError("Введите положительное число.")

    def calculate(self):
        figure = self.figure_combo.currentText()

        try:
            if figure == "Круг":
                r = self.get_number(0)
                area = math.pi * r ** 2
                perimeter = 2 * math.pi * r
                result = (
                    f"<b>Круг</b><br><br>"
                    f"Радиус: {r:.2f}<br>"
                    f"Площадь: {area:.2f}<br>"
                    f"Длина окружности: {perimeter:.2f}"
                )

            elif figure == "Квадрат":
                a = self.get_number(0)
                area = a ** 2
                perimeter = 4 * a
                result = (
                    f"<b>Квадрат</b><br><br>"
                    f"Сторона: {a:.2f}<br>"
                    f"Площадь: {area:.2f}<br>"
                    f"Периметр: {perimeter:.2f}"
                )

            elif figure == "Треугольник":
                a = self.get_number(0)
                b = self.get_number(1)
                c = self.get_number(2)

                if a + b <= c or a + c <= b or b + c <= a:
                    raise ValueError(
                        "Треугольник с такими сторонами не существует."
                    )

                perimeter = a + b + c
                p = perimeter / 2
                area = math.sqrt(p * (p - a) * (p - b) * (p - c))

                result = (
                    f"<b>Треугольник</b><br><br>"
                    f"Сторона a: {a:.2f}<br>"
                    f"Сторона b: {b:.2f}<br>"
                    f"Сторона c: {c:.2f}<br>"
                    f"Площадь: {area:.2f}<br>"
                    f"Периметр: {perimeter:.2f}"
                )

            elif figure == "Куб":
                a = self.get_number(0)
                area = 6 * a ** 2
                perimeter = 12 * a
                volume = a ** 3
                result = (
                    f"<b>Куб</b><br><br>"
                    f"Ребро: {a:.2f}<br>"
                    f"Площадь поверхности: {area:.2f}<br>"
                    f"Периметр основания: {perimeter:.2f}<br>"
                    f"Объём: {volume:.2f}"
                )

            elif figure == "Шар":
                r = self.get_number(0)
                area = 4 * math.pi * r ** 2
                volume = 4 / 3 * math.pi * r ** 3
                result = (
                    f"<b>Шар</b><br><br>"
                    f"Радиус: {r:.2f}<br>"
                    f"Площадь поверхности: {area:.2f}<br>"
                    f"Объём: {volume:.2f}"
                )

            else:
                result = "Неизвестная фигура."

            self.result_label.setText(result)

        except ValueError as error:
            QMessageBox.warning(self, "Ошибка", str(error))

    def show_help(self):
        dialog = HelpDialog(self)
        dialog.exec()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
