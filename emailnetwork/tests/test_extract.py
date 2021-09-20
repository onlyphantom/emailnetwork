import os
import datetime
from unittest import TestCase

from emailnetwork.extract import MBoxReader, extract_meta, extract_body
from emailnetwork.emails import EmailAddress, EmailMeta, EmailBody

"""
Demo mbox is generated from Benjamin Bengfort's Tribe tool
with person names modified for anonymity 
"""
MBOX_PATH = f'{os.path.dirname(__file__)}/test.mbox'

class TestExtract(TestCase):
    def setUp(self):
        self.reader = MBoxReader(MBOX_PATH)
        self.emails = self.reader.extract()

    def tearDown(self):
        self.reader = None

    def test_read_mbox(self):
        self.assertIsInstance(self.reader, MBoxReader)

    def test_length_mbox(self):
        self.assertEqual(len(self.reader), 140)

    def test_extract(self):
        # self.assertTrue(isinstance(next(self.emails), EmailMeta))
        firstemail = next(self.emails)
        self.assertIsInstance(firstemail, EmailMeta)
        self.assertIsInstance(firstemail.subject, str)
        self.assertIsInstance(firstemail.date, datetime.datetime)
        
        for msg in self.emails:
            self.assertGreaterEqual(len(msg.recipients), 1)
            self.assertIsInstance(msg.cc, list)

    def test_email_address(self):
        firstemail = next(self.emails)
        self.assertIsInstance(firstemail.sender, EmailAddress)
        self.assertIsInstance(firstemail.sender.name, str)
        self.assertIsInstance(firstemail.sender.email, str)        

    def test_filter_emails(self):
        newmails = self.reader.filter_emails(datestring="2020-01-01", dateoperator=">=")
        self.assertEqual(len(newmails), 4)

        for email in newmails:
            self.assertGreater(email.date, datetime.datetime(2020,1,1))
            self.assertLess(email.date, datetime.datetime.now())

        oldmails = self.reader.filter_emails(datestring="2019-12-31", dateoperator="<=")
        self.assertEqual(len(oldmails), 136)

        exactmails = self.reader.filter_emails(datestring="2020-04-17", dateoperator="==")
        self.assertEqual(len(exactmails), 1)
        self.assertEqual(exactmails[0].date.date(), datetime.date(2020, 4, 17))

        namedmails = self.reader.filter_emails(emailaddress='samuelchan@gmail.com')

        for email in namedmails:
            checkers = [email.sender.email] + [recipient.email for recipient in email.recipients]
            self.assertTrue('samuelchan@gmail.com' in checkers)

        fullfilteredmails = self.reader.filter_emails(emailaddress='samuelchan@gmail.com', datestring="2020-01-01", dateoperator=">=")

        for email in fullfilteredmails:
            checkers = [email.sender.email] + [recipient.email for recipient in email.recipients]
            self.assertTrue('samuelchan@gmail.com' in checkers)
            self.assertGreater(email.date, datetime.datetime(2020,1,1))

    # also need tests to fail with expected exception when datetime operator not in [==, <=, >=], emailaddress and datetime in wrong format.
    def test_afunction_throws_exception(self):
        self.assertRaises(ValueError, self.reader.filter_emails, 20, "2019-12-31", "<")

    def test_extract_meta_single(self):
        for email in self.reader.mbox:
            self.assertIsInstance(email['Subject'], (bytes, str))
            emailmsg = extract_meta(email)
            self.assertIsInstance(emailmsg, EmailMeta)
            self.assertIsInstance(emailmsg.origin_domain, str)
            self.assertIsInstance(emailmsg.subject, str)

    def test_extract_body_single(self):
        for email in self.reader.mbox:
            emailbody = extract_body(email)
            self.assertIsInstance(emailbody, EmailBody)
            self.assertIsInstance(emailbody.subject, str)
            self.assertIsInstance(emailbody.body, str)
