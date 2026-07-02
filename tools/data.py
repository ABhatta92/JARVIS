from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
from langchain.tools import tool

from config import PROJECT_ROOT, READ_ALLOWED, WRITE_ALLOWED
from tools.filesystem import _is_allowed


def _resolve(path: str):
    """
    Resolve a local path relative to PROJECT_ROOT.
    Leave URLs unchanged.
    """

    parsed = urlparse(path)

    if parsed.scheme in ("http", "https"):
        return path

    return (PROJECT_ROOT / path).resolve()


@tool
def load_data(path: str) -> dict:
    """
    Load tabular data into a pandas DataFrame.

    Supported formats:
    - csv
    - parquet
    - excel
    - json
    """

    source = _resolve(path)

    if isinstance(source, Path):

        if not _is_allowed(source, READ_ALLOWED):
            raise PermissionError(f"Read access denied: {path}")

        suffix = source.suffix.lower()

    else:
        suffix = Path(urlparse(source).path).suffix.lower()

    match suffix:

        case ".csv":
            df = pd.read_csv(source)

        case ".parquet":
            df = pd.read_parquet(source)

        case ".xlsx" | ".xls":
            df = pd.read_excel(source)

        case ".json":
            df = pd.read_json(source)

        case _:
            raise ValueError(f"Unsupported file type: {suffix}")

    return {
        "success": True,
        "dataframe": df,
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
    }


# @tool
# def save_data(
#     dataframe: pd.DataFrame,
#     path: str,
# ) -> dict:
#     """
#     Save a dataframe.
#     """

#     file = (PROJECT_ROOT / path).resolve()

#     if not _is_allowed(file, WRITE_ALLOWED):
#         raise PermissionError(f"Write access denied: {path}")

#     file.parent.mkdir(parents=True, exist_ok=True)

#     suffix = file.suffix.lower()

#     match suffix:

#         case ".csv":
#             dataframe.to_csv(file, index=False)

#         case ".parquet":
#             dataframe.to_parquet(file, index=False)

#         case ".xlsx":
#             dataframe.to_excel(file, index=False)

#         case ".json":
#             dataframe.to_json(
#                 file,
#                 orient="records",
#                 indent=2,
#             )

#         case _:
#             raise ValueError(f"Unsupported file type: {suffix}")

#     return {
#         "success": True,
#         "path": str(file.relative_to(PROJECT_ROOT)),
#         "rows": len(dataframe),
#     }