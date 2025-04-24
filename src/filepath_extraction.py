from typing import Union
from pathlib import Path

def get_single_subpath_part(base_dir: Union[Path, str], n:int) -> str:
    if n ==0:
        return Path(base_dir).name
    for _ in range(n):
        base_dir = Path(base_dir).parent
    return getattr(base_dir, "name")