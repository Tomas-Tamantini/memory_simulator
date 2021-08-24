from dataclasses import dataclass
from typing import Optional


@dataclass
class Command:
    address: int
    is_write: bool
    data: Optional[str] = None
