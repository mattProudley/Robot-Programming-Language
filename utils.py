from dataclasses import dataclass
from typing import Optional, Any
@dataclass
class Result:
    data: Any
    msg: Optional[str]

    def __post_init__(self):
        if self.msg:
            print(self.msg)
            print(self.data)
