from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, time as dtime
from typing import Any, Dict, Optional


def _clamp_int(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, x))


def _parse_hhmm(s: str) -> Optional[dtime]:
    try:
        parts = s.strip().split(":")
        if len(parts) != 2:
            return None
        hh = int(parts[0])
        mm = int(parts[1])
        if not (0 <= hh <= 23 and 0 <= mm <= 59):
            return None
        return dtime(hour=hh, minute=mm)
    except Exception:
        return None


@dataclass
class ControlState:
    auto_off: int                  
    brightness: int                
    start_time: Optional[dtime]    
    end_time: Optional[dtime]   

    def update_from_message(self, msg: Dict[str, Any]) -> bool:
        changed = False

        if "auto-off" in msg:
            try:
                v = int(msg["auto-off"])
                v = _clamp_int(v, 1, 3600)
                if v != self.auto_off:
                    self.auto_off = v
                    changed = True
            except Exception:
                pass

        if "brightness" in msg:
            try:
                v = int(msg["brightness"])
                v = _clamp_int(v, 0, 100)
                if v != self.brightness:
                    self.brightness = v
                    changed = True
            except Exception:
                pass

        if "start-time" in msg and "end-time" in msg:
            st = _parse_hhmm(str(msg["start-time"]))
            et = _parse_hhmm(str(msg["end-time"]))
            if st and et:
                if st != self.start_time or et != self.end_time:
                    self.start_time = st
                    self.end_time = et
                    changed = True

        return changed

    def within_allowed_window(self, now: datetime | None = None) -> bool:
        if self.start_time is None or self.end_time is None:
            return True

        now = now or datetime.now()
        t = now.time()

        st = self.start_time
        et = self.end_time

        if st <= et:
            return st <= t <= et
        else:
            return (t >= st) or (t <= et)

