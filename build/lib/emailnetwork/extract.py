from datetime import datetime
from email.utils import getaddresses
from mailbox import mbox

from mailbox import mboxMessage

from emailnetwork.utils import clean_subject, clean_body
from emailnetwork.emails import EmailAddress, EmailMeta, EmailBody
from emailnetwork.summary import DomainSummary

from emailnetwork.header import HeaderCounter


def extract_meta(email):

    recs = email.get_all('To', []) + email.get_all('Resent-To', [])
    ccs = email.get_all('Cc', []) + email.get_all('Resent-Cc', [])

    return EmailMeta(
        sender=EmailAddress(getaddresses(email.get_all('From'))[0]),
        recipients=[EmailAddress(rec) for rec in getaddresses(recs)],
        cc=[EmailAddress(cc) for cc in getaddresses(ccs)],
        subject=clean_subject(email['Subject']) or None,
        date=email['Date']
    )


def extract_body(email):

    return EmailBody(
        subject=clean_subject(email['Subject']) or None,
        body=clean_body(email)
    )


class MBoxReader(object):
    """ A class that extends python's `mailbox` module to provide additional 
    functionalities such as length, date filtering and parsing. A key component of 
    many `emailnetwork`'s operations.

    Usage:
        reader = MboxReader('path-to-mbox.mbox')

    Args:
        object ([type]): Instantiate this class by specifying a path to an `.mbox` object
    """

    def __init__(self, path) -> None:
        super().__init__()
        self.path = path
        self.mbox = mbox(path)

    def __iter__(self):
        for msg in self.mbox:
            yield msg

    def __len__(self):
        return self.count()

    def count(self):
        """
        Count the number of emails in the mbox instance.
        Helper function to implement __len__ 
        """
        return self.mbox.keys()[-1]+1
        # return len(self.mbox.keys())

    def extract(self):
        """
        Extract the meta data from the Mbox instance
        """
        for email in self:
            try:
                emailmeta = extract_meta(email)
                if emailmeta is not None:
                    yield emailmeta

            except Exception as e:
                print(e)
                continue

    def filter_emails(self, emailaddress=None, datestring=None, dateoperator="=="):
        if emailaddress != None:
            if type(emailaddress) != str:
                raise ValueError(
                    "Please use a valid string representing an email address")

        if dateoperator not in ['>=', '==', '<=']:
            raise ValueError("Please use one of ['>=', '==', '<=']")

        if datestring != None:
            try:
                targetdate = datetime.strptime(datestring, "%Y-%m-%d")
            except ValueError:
                print(ValueError)
                return "Please use the ISO format for comparison: YYYY-MM-DD"

        val = []
        if emailaddress == None and datestring == None:
            for email in self.mbox:
                emailmeta = extract_meta(email)
                val.append(emailmeta)
        elif emailaddress != None and datestring == None:
            for email in self.mbox:
                emailmeta = extract_meta(email)
                checkers = [emailmeta.sender.email] + [recipient.email for recipient in emailmeta.recipients]
                if emailaddress in checkers:
                    val.append(emailmeta)
        elif emailaddress == None and datestring != None:
            for email in self.mbox:
                emailmeta = extract_meta(email)
                if dateoperator == '>=':
                    if emailmeta >= targetdate:
                        val.append(emailmeta)
                elif dateoperator == '==':
                    if emailmeta == targetdate:
                        val.append(emailmeta)
                elif dateoperator == '<=':
                    if emailmeta <= targetdate:
                        val.append(emailmeta)
        else:
            for email in self.mbox:
                emailmeta = extract_meta(email)
                checkers = [emailmeta.sender.email] + [recipient.email for recipient in emailmeta.recipients]
                if emailaddress in checkers:
                    if dateoperator == '>=':
                        if emailmeta >= targetdate:
                            val.append(emailmeta)
                    elif dateoperator == '==':
                        if emailmeta == targetdate:
                            val.append(emailmeta)
                    elif dateoperator == '<=':
                        if emailmeta <= targetdate:
                            val.append(emailmeta)

        return val


if __name__ == '__main__':
    reader = MBoxReader('/Users/samuel/Footprints/samuel-supertype.mbox')
    # reader = MBoxReader('/Users/vincentiuscalvin/Documents/Supertype/mbox-dataset/Ori_Sample_01.mbox')
    headers = HeaderCounter(reader)
    k = headers.keys()
    spamheaders = list(filter(lambda v: "spam" in v.lower(), k))
    
    summary = DomainSummary(reader)
    
    email = reader.mbox[1]
    emailmsg = extract_meta(email)
    emailbody = extract_body(email)
    mails = reader.filter_emails(datestring='2020-12-31', dateoperator="==")