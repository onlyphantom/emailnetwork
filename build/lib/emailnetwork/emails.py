from dataclasses import dataclass
from datetime import datetime
from emailnetwork.utils import parse_date

@dataclass
class EmailMeta:
    """
    Also Refer to: 
    https://www.iana.org/assignments/message-headers/message-headers.xhtml
    
    """
    
    sender: str
    subject: str
    date: str
    recipients: list
    cc: list
    origin_domain: str=None

    def __post_init__(self):
        self.origin_domain = self.sender.domain
        self.date = parse_date(self.date)

    def __eq__(self, targetdate):
        if isinstance(targetdate, datetime):
            return self.date.date() == targetdate.date()

    def __ge__(self, targetdate):
        if isinstance(targetdate, datetime):
            return self.date.date() >= targetdate.date()

    def __le__(self, targetdate):
        if isinstance(targetdate, datetime):
            return self.date.date() <= targetdate.date()

@dataclass
class EmailAddress:
    name: str=None
    email: str=None

    def __init__(self, string):
        self.name, self.email  = string
        self.email = self.email.lower()

    def __getitem__(self):
        return self.name, self.email

    @property
    def domain(self):
        return self.email.split('@')[-1] or None

@dataclass
class EmailBody:
    subject: str = None
    body: str = None