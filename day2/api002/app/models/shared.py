from dataclasses import dataclass
from typing import Optional

@dataclass
class ResultReq:
    ok: bool = False
    err_msg: Optional[str] = None