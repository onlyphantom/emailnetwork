from datetime import datetime

from dateutil import parser
from dateutil.tz import tzlocal, tzutc
from email.utils import parsedate_tz, mktime_tz
from email.header import decode_header


def parse_date(datestring: str):
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


def clean_subject(subject):
    """[summary]
    Usage:

    Args:
        subject (byte or str)
    """
    subject, encoding = decode_header(subject)[0]
    if isinstance(subject, bytes):
        try:
            return subject.decode(encoding).strip()
        except:
            return subject.decode('utf-8').strip()
    else:
        return subject.strip().replace('\r\n', '')


def clean_body(email):
    if email.is_multipart():
        for part in email.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                return part.get_payload(decode=True).decode()  # decode
                break
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        return email.get_payload(decode=True).decode()
