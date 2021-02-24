from collections import Counter
import matplotlib.pyplot as plt

plt.style.use('seaborn')
class DomainSummary():

    def __init__(self, reader):
        self.emailmetas = reader.extract()
        self.summary = self.get_summary()

    def get_summary(self):
        domains = {}
        for email in self.emailmetas:
            domains[email.origin_domain] = domains.get(email.origin_domain, 0) + 1

        return Counter(domains)

    def plot(self):
        fig = plt.figure(figsize = (10, 5)) 

        domains = list(self.summary.keys()) 
        freqs = list(self.summary.values())
        
        # creating the bar plot 
        plt.barh(domains, freqs, color ='cadetblue') 
        [i.set_color("darkorchid") for i in plt.gca().get_xticklabels()]
        [i.set_color("darkorchid") for i in plt.gca().get_yticklabels()]
        plt.title("Sender's Domain Occurences", fontdict={"fontname": "Helvetica", "color": "k", "fontweight": "bold", "fontsize": 12})
        plt.show() 

    def __str__(self):
        coba = []
        for keys in self.summary:
            coba.append(f"{keys:<25s}: {str(self.summary[keys]):<3s}")
        return "\n".join(coba)
        
if __name__ == "__main__":
    from emailnetwork.extract import MBoxReader
    reader = MBoxReader('/Users/vincentiuscalvin/Documents/Supertype/mbox-dataset/Ori_Sample_01.mbox')
    summary = DomainSummary(reader)

    print(summary.summary)
    print(summary)

    summary.plot()