from PySide6.QtWidgets import QFrame, QHBoxLayout

from ui.icon_button import IconButton
from ui.search_box import SearchBox


class TopToolbar(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("topToolbar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.back = IconButton("‹")
        self.forward = IconButton("›")
        self.reload = IconButton("⟳")
        self.search = SearchBox()
        self.notification = IconButton("♧")
        self.view = IconButton("▦")
        self.profile = IconButton("A")

        self.back.setToolTip("Back")
        self.forward.setToolTip("Forward")
        self.reload.setToolTip("Refresh")
        self.notification.setToolTip("Notifications")
        self.view.setToolTip("Change view")
        self.profile.setToolTip("Profile")

        for button in (self.back, self.forward, self.reload):
            layout.addWidget(button)
        layout.addSpacing(8)
        layout.addWidget(self.search, 1)
        layout.addSpacing(8)
        layout.addWidget(self.notification)
        layout.addWidget(self.view)
        layout.addWidget(self.profile)
