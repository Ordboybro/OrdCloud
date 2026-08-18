class FileSort:

    @staticmethod
    def by_name(items, reverse=False):
        return sorted(
            items,
            key=lambda item: item["name"].lower(),
            reverse=reverse,
        )

    @staticmethod
    def by_size(items, reverse=False):
        return sorted(
            items,
            key=lambda item: item.get("bytes", 0),
            reverse=reverse,
        )

    @staticmethod
    def by_date(items, reverse=True):
        return sorted(
            items,
            key=lambda item: item.get("timestamp", 0),
            reverse=reverse,
        )

    @staticmethod
    def folders_first(items):
        return sorted(
            items,
            key=lambda item: (
                not item["dir"],
                item["name"].lower(),
            ),
        )
