from PySide6.QtWidgets import QWidget, QGridLayout

from ui.dashboard_card import DashboardCard


class DashboardStats(QWidget):

    def __init__(self):
        super().__init__()

        layout = QGridLayout(self)
        layout.setSpacing(14)

        cards = [
            ("Folders", "124", "📁"),
            ("Files", "5 428", "📄"),
            ("Images", "982", "🖼"),
            ("Videos", "38", "🎥"),
            ("Music", "142", "🎵"),
            ("Archives", "25", "📦"),
        ]

        for index, data in enumerate(cards):

            row = index // 3
            column = index % 3

            layout.addWidget(
                DashboardCard(*data),
                row,
                column,
            )
