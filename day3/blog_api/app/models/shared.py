from dataclasses import dataclass
from typing import Optional

@dataclass
class ResultResp:
    ok: bool = False
    err_msg: Optional[str] = None