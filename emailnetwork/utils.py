from datetime import datetime

from dateutil import parser
from dateutil.tz import tzlocal, tzutc
from email.utils import parsedate_tz, mktime_tz

def parse_date(datestring:str):
    """[summary]
    Usage:
        Primarily used for extract_meta(email): parse_date(email['Date'])
        parse_date('Sat, 19 Sep 2020 12:01:38 +0800')
    Args:
        datestring (str): [description]
    """
    try:
        dt = parsedate_tz(datestring)
        if dt is not None:
            return datetime.utcfromtimestamp(mktime_tz(dt))

        return parser.parse(datestring)
    except Exception:
        return None



