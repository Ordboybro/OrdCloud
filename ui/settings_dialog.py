from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QVBoxLayout,
)

from modules.settings import Settings


class SettingsDialog(QDialog):
    """Persistent local application settings."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки OrdCloud")
        self.setMinimumWidth(420)
        self.settings = Settings()
        values = self.settings.load()

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 22, 24, 20)
        root.setSpacing(18)

        title = QLabel("Настройки")
        title.setObjectName("settingsTitle")
        root.addWidget(title)

        subtitle = QLabel("Параметры сохраняются локально на этом компьютере.")
        subtitle.setObjectName("settingsSubtitle")
        subtitle.setWordWrap(True)
        root.addWidget(subtitle)

        form = QFormLayout()
        form.setHorizontalSpacing(22)
        form.setVerticalSpacing(14)

        self.view = QComboBox()
        self.view.addItem("Обычный список", "list")
        self.view.addItem("Компактный список", "compact")
        self.view.setCurrentIndex(max(0, self.view.findData(values.get("view", "list"))))
        form.addRow("Представление", self.view)

        self.animations = QCheckBox("Плавные переходы интерфейса")
        self.animations.setChecked(bool(values.get("animations", True)))
        form.addRow("Анимации", self.animations)

        self.confirm_delete = QCheckBox("Спрашивать подтверждение перед удалением")
        self.confirm_delete.setChecked(bool(values.get("confirm_delete", True)))
        form.addRow("Удаление", self.confirm_delete)

        self.show_extensions = QCheckBox("Показывать расширения файлов")
        self.show_extensions.setChecked(bool(values.get("show_extensions", True)))
        form.addRow("Файлы", self.show_extensions)

        root.addLayout(form)
        root.addStretch(1)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)

    def _save(self):
        data = self.settings.load()
        data.update(
            {
                "view": self.view.currentData(),
                "animations": self.animations.isChecked(),
                "confirm_delete": self.confirm_delete.isChecked(),
                "show_extensions": self.show_extensions.isChecked(),
            }
        )
        self.settings.save(data)
        self.accept()
