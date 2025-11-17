from datetime import datetime, timezone
import zoneinfo

_JST = zoneinfo.ZoneInfo("Asia/Tokyo")

def jst_now() -> datetime:
    return datetime.now(_JST)

def utc_now() -> datetime:
    return datetime.now(timezone.utc)
