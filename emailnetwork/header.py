from collections import Counter
from email.header import decode_header
from emailnetwork.utils import clean_subject


class HeaderCounter(Counter):
    """[summary]

    Args:
        Counter ([type]): [description]
    """

    def __init__(self, reader):
        super().__init__()
        self = self.build_from(reader)

    def __str__(self):
        return f'{self.most_common()}'

    def build_from(self, reader):
        for email in reader:
            for k in email.keys():
                self[k] += 1

        return self

    def histogram(self, n=25):
        from matplotlib import pyplot as plt
        plt.style.use('fivethirtyeight')
        k, v = (list(self.keys())[:n], list(self.values())[:n])
        fig = plt.figure(figsize=(7, 10))
        ax = fig.add_subplot(111)
        y_pos = [i for i in range(n)]
        ax.barh(y_pos, v, color='plum')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(k)
        ax.invert_yaxis()
        ax.set_xlabel('Frequency')
        ax.set_title('Email Header Analysis')
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    from emailnetwork.extract import MBoxReader
    # reader = MBoxReader('/Users/samuel/Footprints/samuel-supertype.mbox')
    reader = MBoxReader('/Users/vincentiuscalvin/Documents/Supertype/mbox-dataset/Ori_Sample_01.mbox')
    headers = HeaderCounter(reader)

    k = headers.keys()

    containspam = list(filter(lambda v: "spam" in v.lower(), k))

    for email in reader:
        for key in email.keys():
            if key in containspam:
                print({key: decode_header(email[key])})
