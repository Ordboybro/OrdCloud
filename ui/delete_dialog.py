from ui.dialog import Dialog


class DeleteDialog(Dialog):

    def __init__(self, name):

        super().__init__(
            "Delete",
            f"Delete '{name}'?",
        )
