from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

from config import ICONS_DIR
from ui.icon_button import IconButton
from ui.search_box import SearchBox


class TopToolbar(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("topToolbar")
        self.setFixedHeight(104)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 38, 0)
        layout.setSpacing(14)

        self.menu = IconButton("ui_menu.svg")
        self.menu.setObjectName("headerMenu")
        self.menu.setToolTip("Меню")
        layout.addWidget(self.menu)

        brand = QFrame()
        brand.setObjectName("brand")
        brand_layout = QHBoxLayout(brand)
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(11)

        cloud = QLabel()
        cloud.setObjectName("brandCloud")
        cloud.setFixedSize(43, 43)
        cloud.setPixmap(QIcon(str(ICONS_DIR / "ui_cloud.svg")).pixmap(QSize(43, 43)))
        cloud.setAlignment(Qt.AlignCenter)
        brand_layout.addWidget(cloud)

        title = QLabel("FILES – МОИ ФАЙЛЫ")
        title.setObjectName("brandTitle")
        brand_layout.addWidget(title)
        layout.addWidget(brand)

        layout.addSpacing(92)

        self.back = IconButton("‹")
        self.forward = IconButton("›")
        self.reload = IconButton("↻")
        self.back.hide()
        self.forward.hide()
        self.reload.hide()

        self.search = SearchBox()
        self.search.setObjectName("headerSearch")
        self.search.setMinimumWidth(650)
        self.search.setMaximumWidth(820)
        layout.addWidget(self.search, 1)

        layout.addStretch(1)

        self.notification = IconButton("ui_bell.svg")
        self.notification.setObjectName("headerIcon")
        self.view = IconButton("ui_grid.svg")
        self.view.setObjectName("headerIcon")
        self.profile = IconButton("A")
        self.profile.setObjectName("profileButton")

        self.notification.setToolTip("Уведомления")
        self.view.setToolTip("Вид")
        self.profile.setToolTip("Профиль")

        layout.addWidget(self.notification)
        layout.addWidget(self.view)
        layout.addWidget(self.profile)
