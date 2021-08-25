from dataclasses import dataclass
from typing import Optional


@dataclass
class Command:
    address: int
    is_write: bool
    data: Optional[str] = None

    @property
    def as_raw_str(self):
        out_str = f'{self.address} {"1" if self.is_write else "0"}'
        return out_str if not self.is_write else out_str + " " + self.data
