from collections import Counter
from datetime import datetime


class DomainSummary():

    def __init__(self, reader):
        self.emailmetas = reader.extract()
        self.summary = self.get_summary()

    def get_summary(self):
        domains = {}
        for email in self.emailmetas:
            domains[email.origin_domain] = domains.get(
                email.origin_domain, 0) + 1

        return Counter(domains)

    def plot(self):
        import matplotlib.pyplot as plt
        plt.style.use('seaborn')

        fig = plt.figure(figsize=(10, 5))

        domains = list(self.summary.keys())
        freqs = list(self.summary.values())

        plt.barh(domains, freqs, color='cadetblue')
        [i.set_color("darkorchid") for i in plt.gca().get_xticklabels()]
        [i.set_color("darkorchid") for i in plt.gca().get_yticklabels()]
        plt.title("Sender's Domain Occurences", fontdict={
                  "fontname": "Helvetica", "color": "k", "fontweight": "bold", "fontsize": 12})
        plt.show()

    def __str__(self):
        coba = []
        for keys in self.summary:
            coba.append(f"{keys:<25s}: {str(self.summary[keys]):<3s}")
        return "\n".join(coba)


class IncomingOutgoingSummary():

    def __init__(self, reader):
        self.reader = reader
        self.emailmetas = reader.extract()
        self.user_email = self.get_user_email()
        self.summary = self.get_summary()

    def get_user_email(self):
        from emailnetwork.extract import extract_meta

        email_addresses = {}
        for i in range(10):
            email = self.reader.mbox[i]
            emailmsg = extract_meta(email)
            for recipient in emailmsg.recipients:
                email_addresses[recipient.email] = email_addresses.get(
                    recipient.email, 0) + 1
            email_addresses[emailmsg.sender.email] = email_addresses.get(
                emailmsg.sender.email, 0) + 1
        return sorted(email_addresses.items(), key=lambda k: k[1], reverse=True)[0][0]

    def get_summary(self):
        date = {}
        for email in self.emailmetas:
            if email.date.strftime('%B %Y') not in date:
                date[email.date.strftime('%B %Y')] = {
                    'Incoming': 0, 'Outgoing': 0}
            if email.sender.email == self.user_email:
                date[email.date.strftime('%B %Y')]['Outgoing'] += 1
            else:
                date[email.date.strftime('%B %Y')]['Incoming'] += 1

        date = sorted(
            date.items(), key=lambda items: datetime.strptime(items[0], '%B %Y'))
        return dict(date)

    def plot(self):
        import matplotlib.pyplot as plt
        plt.style.use('seaborn')

        dates = list(self.summary.keys())
        incoming = list(item[1]['Incoming'] for item in self.summary.items())
        outgoing = list(item[1]['Outgoing'] for item in self.summary.items())

        fig, ax = plt.subplots()

        ax.bar(dates, incoming, 0.4, label='Incoming', color='cadetblue')
        ax.bar(dates, outgoing, 0.4, bottom=incoming, label='Outgoing')

        [i.set_color("darkorchid") for i in plt.gca().get_xticklabels()]
        [i.set_color("darkorchid") for i in plt.gca().get_yticklabels()]

        plt.xticks(rotation=45)

        ax.set_ylabel('Counts')
        ax.set_title('Number of Incoming and Outgoing Emails per Month', fontdict={"fontname": "Helvetica", "color": "k", "fontweight": "bold", "fontsize": 12})
        ax.legend()

        plt.show()


if __name__ == "__main__":
    from emailnetwork.extract import MBoxReader
    reader = MBoxReader('/Users/vincentiuscalvin/Documents/Supertype/mbox-dataset/Ori_Sample_01.mbox')
    summary = DomainSummary(reader)
    summary_2 = IncomingOutgoingSummary(reader)
