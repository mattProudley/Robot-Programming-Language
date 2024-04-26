from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Result:
    data: Any
    msg: Optional[str]

    def __post_init__(self):
        if self.msg:
            # Terminal print message for debugging
            # terminal_print(self.msg)
            # IDE Terminal print for debugging
            print(self.data)
            print(self.msg)
