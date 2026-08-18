from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel


class DashboardCard(QFrame):

    def __init__(self, title, value, icon):
        super().__init__()

        self.setObjectName("dashboardCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)

        top = QHBoxLayout()

        icon_label = QLabel(icon)
        icon_label.setObjectName("dashboardIcon")

        top.addWidget(icon_label)
        top.addStretch()

        layout.addLayout(top)

        layout.addStretch()

        value_label = QLabel(value)
        value_label.setObjectName("dashboardValue")

        title_label = QLabel(title)
        title_label.setObjectName("dashboardText")

        layout.addWidget(value_label)
        layout.addWidget(title_label)
