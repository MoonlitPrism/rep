import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: root
    visible: true
    width: 740
    height: 640
    title: "Карточка объекта учёта"
    color: "#f0f0f0"

    Component.onCompleted: resetForm()

    footer: ToolBar {
        RowLayout {
            anchors.fill: parent
            Label {
                id: statusLabel
                text: "Готово"
                elide: Label.ElideRight
                Layout.fillWidth: true
                leftPadding: 10
            }
        }
    }

    ScrollView {
        anchors.fill: parent
        anchors.margins: 10
        clip: true

        ColumnLayout {
            width: parent.width
            spacing: 15

            GroupBox {
                title: "Организация"
                Layout.fillWidth: true

                GridLayout {
                    columns: 2
                    columnSpacing: 15
                    rowSpacing: 10
                    anchors.fill: parent

                    Label { text: "Организация:" }
                    TextField {
                        id: orgEdit
                        text: "ООО «Сельпром»"
                        placeholderText: "Введите наименование организации"
                        Layout.fillWidth: true
                    }

                    Label { text: "Структурное подразделение:" }
                    TextField {
                        id: subdivisionEdit
                        text: "Ферма №2"
                        placeholderText: "Введите какую ферму вы выбрали"
                        Layout.fillWidth: true
                    }

                    Label { text: "Материально ответственное лицо:" }
                    TextField {
                        id: molEdit
                        text: "Кладовщик Семенов Иван Иванович"
                        Layout.fillWidth: true
                    }
                }
            }

            GroupBox {
                title: "Объект учёта"
                Layout.fillWidth: true

                GridLayout {
                    columns: 2
                    columnSpacing: 15
                    rowSpacing: 10
                    anchors.fill: parent

                    Label { text: "Наименование объекта *:" }
                    TextField {
                        id: nameEdit
                        placeholderText: "Например: Лопата штыковая"
                        Layout.fillWidth: true
                        onTextChanged: {
                            if (text.trim() !== "") {
                                statusLabel.text = "Введено название: " + text
                            } else {
                                statusLabel.text = "Название объекта не заполнено"
                            }
                        }
                    }

                    Label { text: "Группа имущества:" }
                    ComboBox {
                        id: categoryCombo
                        model: ["Инструмент для земляных работ (ручной)"]
                        Layout.fillWidth: true
                        onCurrentTextChanged: {
                            statusLabel.text = "Выбрана группа: " + currentText
                        }
                    }

                    Label { text: "Дата постановки на учёт:" }
                    TextField {
                        id: dateEdit
                        text: Qt.formatDate(new Date(), "dd.MM.yyyy")
                        Layout.fillWidth: true
                    }
                }
            }

            GroupBox {
                title: "Параметры"
                Layout.fillWidth: true

                GridLayout {
                    columns: 2
                    columnSpacing: 15
                    rowSpacing: 10
                    anchors.fill: parent

                    Label { text: "Срок полезного использования (мес.):" }
                    SpinBox {
                        id: lifeSpin
                        from: 1
                        to: 120
                        value: 36
                        editable: true
                        textFromValue: function(value) { return value + " мес." }
                        valueFromText: function(text) { return parseInt(text) }
                        Layout.fillWidth: true
                        onValueChanged: {
                            var years = Math.floor(value / 12)
                            var months = value % 12
                            statusLabel.text = "Срок службы: " + value + " мес. (~" + years + " г. " + months + " мес.)"
                        }
                    }

                    Label { text: "Количество, ед.:" }
                    SpinBox {
                        id: qtySpin
                        from: 1
                        to: 1000
                        value: 1
                        Layout.fillWidth: true
                    }

                    Label { text: "Износ, %:" }
                    RowLayout {
                        Layout.fillWidth: true
                        Slider {
                            id: wearSlider
                            from: 0
                            to: 100
                            value: 0
                            Layout.fillWidth: true
                            onValueChanged: {
                                wearLabel.text = value + " %"
                                statusLabel.text = "Износ: " + value + " %"
                            }
                        }
                        Label {
                            id: wearLabel
                            text: "0 %"
                            Layout.preferredWidth: 50
                        }
                    }

                    CheckBox {
                        id: repairCheck
                        text: "Требуется ремонт"
                        Layout.columnSpan: 2
                        onToggled: {
                            statusLabel.text = checked ? "Объект требует ремонта" : "Ремонт не требуется"
                        }
                    }

                    CheckBox {
                        id: workingCheck
                        text: "В эксплуатации"
                        checked: true
                        Layout.columnSpan: 2
                        onToggled: {
                            statusLabel.text = checked ? "Объект в эксплуатации" : "Объект не эксплуатируется"
                        }
                    }
                }
            }

            GroupBox {
                title: "Примечание"
                Layout.fillWidth: true

                ScrollView {
                    height: 70
                    Layout.fillWidth: true
                    TextArea {
                        id: noteEdit
                        placeholderText: "Дополнительная информация об объекте..."
                        wrapMode: TextArea.Wrap
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Button {
                    text: "Сохранить"
                    onClicked: {
                        var name = nameEdit.text.trim()
                        if (name === "") {
                            warningDialog.text = "Необходимо заполнить название объекта"
                            warningDialog.open()
                            nameEdit.forceActiveFocus()
                            return
                        }

                        var info = "Объект: " + name + "\n" +
                                   "Организация: " + orgEdit.text + "\n" +
                                   "Подразделение: " + subdivisionEdit.text + "\n" +
                                   "Группа: " + categoryCombo.currentText + "\n" +
                                   "Количество: " + qtySpin.value + " ед.\n" +
                                   "Срок службы: " + lifeSpin.value + " мес.\n" +
                                   "Износ: " + wearSlider.value + " %\n" +
                                   "Требуется ремонт: " + (repairCheck.checked ? "да" : "нет") + "\n" +
                                   "В эксплуатации: " + (workingCheck.checked ? "да" : "нет")

                        infoDialog.text = info
                        infoDialog.open()
                        statusLabel.text = "Сохранено: " + name
                    }
                }

                Button {
                    text: "Очистить"
                    onClicked: {
                        resetForm()
                    }
                }

                Item { Layout.fillWidth: true }

                Button {
                    text: "Выход"
                    onClicked: {
                        Qt.quit()
                    }
                }
            }
        }
    }

    Dialog {
        id: warningDialog
        title: "Ошибка заполнения"
        standardButtons: Dialog.Ok
        modal: true
        anchors.centerIn: parent
        width: 300
        property alias text: warningText.text
        Label {
            id: warningText
            wrapMode: Label.Wrap
            width: parent.width
        }
    }

    Dialog {
        id: infoDialog
        title: "Данные сохранены"
        standardButtons: Dialog.Ok
        modal: true
        anchors.centerIn: parent
        width: 400
        property alias text: infoText.text
        Label {
            id: infoText
            wrapMode: Label.Wrap
            width: parent.width
        }
    }

    function resetForm() {
        nameEdit.clear()
        noteEdit.clear()

        lifeSpin.value = 36
        qtySpin.value = 1

        repairCheck.checked = false
        workingCheck.checked = true

        wearSlider.value = 0
        wearLabel.text = "0 %"

        orgEdit.text = "ООО «Сельпром»"
        subdivisionEdit.text = "Ферма №2"
        molEdit.text = "Кладовщик Семенов Иван Иванович"
        dateEdit.text = Qt.formatDate(new Date(), "dd.MM.yyyy")

        statusLabel.text = "Форма очищена"
    }
}