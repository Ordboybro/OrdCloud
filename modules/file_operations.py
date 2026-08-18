from pathlib import Path
import shutil

from send2trash import send2trash


class FileOperations:

    @staticmethod
    def delete(path: str | Path) -> None:
        send2trash(str(path))

    @staticmethod
    def copy(src: str | Path, dst: str | Path) -> None:
        src = Path(src)
        dst = Path(dst)

        if src.is_dir():
            shutil.copytree(
                src,
                dst,
                dirs_exist_ok=True,
            )
        else:
            shutil.copy2(src, dst)

    @staticmethod
    def move(src: str | Path, dst: str | Path) -> None:
        shutil.move(str(src), str(dst))

    @staticmethod
    def create_folder(
        folder: str | Path,
        name: str,
    ) -> Path:

        path = Path(folder) / name

        path.mkdir(
            parents=True,
            exist_ok=False,
        )

        return path

    @staticmethod
    def rename(
        path: str | Path,
        name: str,
    ) -> Path:

        path = Path(path)

        destination = path.parent / name

        return path.rename(destination)

    @staticmethod
    def exists(path: str | Path) -> bool:
        return Path(path).exists()
