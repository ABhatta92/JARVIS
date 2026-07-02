from pathlib import Path
from langchain.tools import tool

from config import PROJECT_ROOT, READ_ALLOWED, WRITE_ALLOWED


def _resolve(path: str) -> Path:
    """
    Resolve a path relative to the project root.
    """
    return (PROJECT_ROOT / path).resolve()


def _is_allowed(path: Path, allowed_dirs: list[Path]) -> bool:
    """
    Check whether a path is contained inside one of the allowed directories.
    """
    for directory in allowed_dirs:
        try:
            path.relative_to(directory.resolve())
            return True
        except ValueError:
            continue

    return False


@tool
def read_file(path: str) -> dict:
    """
    Read a UTF-8 text file.
    """

    file = _resolve(path)

    if not _is_allowed(file, READ_ALLOWED):
        raise PermissionError(f"Read access denied: {path}")

    if not file.exists():
        raise FileNotFoundError(path)

    contents = file.read_text(encoding="utf-8")

    return {
        "success": True,
        "path": str(file.relative_to(PROJECT_ROOT)),
        "contents": contents,
        "size": len(contents),
    }


@tool
def write_file(path: str, contents: str) -> dict:
    """
    Write a UTF-8 text file.
    """

    file = _resolve(path)

    if not _is_allowed(file, WRITE_ALLOWED):
        raise PermissionError(f"Write access denied: {path}")

    file.parent.mkdir(parents=True, exist_ok=True)

    file.write_text(contents, encoding="utf-8")

    return {
        "success": True,
        "path": str(file.relative_to(PROJECT_ROOT)),
        "bytes_written": len(contents.encode("utf-8")),
    }


@tool
def list_files(path: str = ".") -> dict:
    """
    List every file beneath a directory.
    """

    folder = _resolve(path)

    if not _is_allowed(folder, READ_ALLOWED):
        raise PermissionError(f"Read access denied: {path}")

    if not folder.exists():
        raise FileNotFoundError(path)

    files = [
        str(f.relative_to(PROJECT_ROOT))
        for f in folder.rglob("*")
        if f.is_file()
    ]

    return {
        "success": True,
        "count": len(files),
        "files": files,
    }


@tool
def delete_file(path: str) -> dict:
    """
    Delete a file.
    """

    file = _resolve(path)

    if not _is_allowed(file, WRITE_ALLOWED):
        raise PermissionError(f"Delete access denied: {path}")

    if not file.exists():
        raise FileNotFoundError(path)

    file.unlink()

    return {
        "success": True,
        "deleted": str(file.relative_to(PROJECT_ROOT)),
    }


@tool
def file_exists(path: str) -> dict:
    """
    Check whether a file exists.
    """

    file = _resolve(path)

    if not _is_allowed(file, READ_ALLOWED):
        raise PermissionError(f"Read access denied: {path}")

    return {
        "success": True,
        "exists": file.exists(),
        "path": str(file.relative_to(PROJECT_ROOT)),
    }


@tool
def make_directory(path: str) -> dict:
    """
    Create a directory.
    """

    folder = _resolve(path)

    if not _is_allowed(folder, WRITE_ALLOWED):
        raise PermissionError(f"Write access denied: {path}")

    folder.mkdir(parents=True, exist_ok=True)

    return {
        "success": True,
        "directory": str(folder.relative_to(PROJECT_ROOT)),
    }