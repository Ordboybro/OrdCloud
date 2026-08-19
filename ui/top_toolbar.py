from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton

from ui.icon_button import IconButton
from ui.search_box import SearchBox


class TopToolbar(QFrame):
    """Full-width header matching the reference cloud-drive layout."""

    def __init__(self):
        super().__init__()
        self.setObjectName("topToolbar")
        self.setFixedHeight(104)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 38, 0)
        layout.setSpacing(12)

        self.menu = IconButton("☰")
        self.menu.setObjectName("headerMenu")
        self.menu.setToolTip("Menu")
        layout.addWidget(self.menu)

        brand = QFrame()
        brand.setObjectName("brand")
        brand_layout = QHBoxLayout(brand)
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(12)

        cloud = QLabel("☁")
        cloud.setObjectName("brandCloud")
        cloud.setAlignment(Qt.AlignCenter)
        brand_layout.addWidget(cloud)

        title = QLabel("FILES – МОИ ФАЙЛЫ")
        title.setObjectName("brandTitle")
        brand_layout.addWidget(title)
        layout.addWidget(brand)

        layout.addStretch(1)

        self.back = IconButton("‹")
        self.forward = IconButton("›")
        self.reload = IconButton("↻")
        self.back.hide()
        self.forward.hide()
        self.reload.hide()

        self.search = SearchBox()
        self.search.setObjectName("headerSearch")
        self.search.setMinimumWidth(470)
        self.search.setMaximumWidth(700)
        layout.addWidget(self.search, 1)

        layout.addStretch(1)

        self.notification = IconButton("♧")
        self.notification.setObjectName("headerIcon")
        self.view = IconButton("▦")
        self.view.setObjectName("headerIcon")
        self.profile = IconButton("A")
        self.profile.setObjectName("profileButton")

        self.notification.setToolTip("Уведомления")
        self.view.setToolTip("Вид")
        self.profile.setToolTip("Профиль")

        layout.addWidget(self.notification)
        layout.addWidget(self.view)
        layout.addWidget(self.profile)
