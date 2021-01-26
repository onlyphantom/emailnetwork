from collections import Counter
import math
import matplotlib.pyplot as plt
import networkx as nx
import textwrap

from emailnetwork.extract import MBoxReader, extract_meta
from emailnetwork.network import PeopleCombination


def plot_single_email(reader:MBoxReader, id:int=False, showtitle:bool=False):
    """[summary]

    Usage:
        reader = MboxReader('path-to-mbox.mbox')
        plot_single_email(reader, 300) plots the 300th email from the mbox
    Args:
        reader (MBoxReader): [description]
        id (int, optional): [description]. Defaults to False.
    """

    len_reader = len(reader)
    if not id:
        email = reader.mbox[len_reader-1]
    else:
        email = reader.mbox[id]
    emailmsg = extract_meta(email)

    subject = textwrap.fill(emailmsg.subject, 40)
    sender = emailmsg.sender.name if len(emailmsg.sender.name) != 0 else emailmsg.sender.email.split('@')[0]

    plt.figure(figsize=(9, 6))
    G = nx.DiGraph(name='Single Email Flow')

    for recipient in emailmsg.recipients:
        rec = recipient.name
        G.add_edge(sender, rec if len(rec) != 0 else recipient.email, 
            message=subject, color='darkorchid', weight=3)
    
    for cc in emailmsg.cc:
        ccc = cc.name
        G.add_edge(sender, ccc if len(ccc) != 0 else cc.email, 
            message='cc', color='lightsteelblue', weight=2)

    colors = nx.get_edge_attributes(G,'color').values()
    weights = nx.get_edge_attributes(G,'weight').values()
    edge_labels = nx.get_edge_attributes(G, 'message')
    
    pos = nx.planar_layout(G)
 
    # nx.draw_spectral(G,node_size=0, alpha=0.8, edge_color=colors, width=list(weights), font_size=8, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, label_pos=0.5)
    nx.draw_planar(G,node_size=0, alpha=1, edge_color=colors, width=list(weights), font_size=8, font_weight='bold', with_labels=True, verticalalignment='bottom')

    if showtitle:
        font = {"fontname": "Helvetica", "color": "k", "fontweight": "bold", "fontsize": 8}
        plt.title(subject + '\n Delivery date: ' + emailmsg.date.strftime("%m/%d/%Y"), fontdict=font)
    
    plt.tight_layout(pad=0.5)
    plt.axis('off')
    plt.show()

def plot_single_socialnetwork(reader:MBoxReader, id:int=False, showtitle:bool=False):
    """[summary]

    Usage:
        reader = MboxReader('path-to-mbox.mbox')
        plot_single_socialnetwork(reader, 300) plots the 300th email from the mbox
    Args:
        reader (MBoxReader): [description]
        id (int, optional): [description]. Defaults to False.
    """
    len_reader = len(reader)
    if not id:
        email = reader.mbox[len_reader-1]
    else:
        email = reader.mbox[id]
    emailmsg = extract_meta(email)

    subject = textwrap.fill(emailmsg.subject, 40)
    ng = PeopleCombination(emailmsg)    
    G = nx.Graph(
            name='Single Email Social Network')
    counter = Counter()
    for combo in ng.combo:
        counter[combo] += 1

    total_combos = sum(counter.values())
    by_freq = {k: v/total_combos for k, v in counter.most_common()}

    for rel in counter.keys():
        G.add_edge(*rel, weight=by_freq[rel], count=counter[rel])
    k = 1/math.sqrt(G.order()) * 2
    pos = nx.spring_layout(G, k=k)
    deg = [v for _, v in G.degree()]
    # nx.draw_networkx_nodes(G, pos, node_size=deg, linewidths=1.0, alpha=0.90, label=G._node.keys())
    nx.draw_networkx_nodes(G, pos, node_size=deg, linewidths=1.0, alpha=0.90)
    nx.draw_networkx_edges(G, pos, edge_color="steelblue", width=1.0, style='dashed', alpha=0.75)
    nx.draw_networkx_labels(G, pos, {n: n for n in G.nodes}, font_size=8, verticalalignment="bottom")
    # nx.draw_networkx_labels(G, pos, {n: n for n in G.nodes if n.split('@')[-1] == 'supertype.ai'}, font_size=8)
    
    if showtitle:
        font = {"fontname": "Helvetica", "color": "k", "fontweight": "bold", "fontsize": 8}
        plt.title(subject + '\n Delivery date: ' + emailmsg.date.strftime("%m/%d/%Y"), fontdict=font)
    
    plt.tight_layout(pad=0.5)
    plt.axis('off')
    plt.show()

def plot_full_emailnetwork(reader:MBoxReader, layout:str='shell'):
    """[summary]

    Usage:
        reader = MboxReader('path-to-mbox.mbox')
        plot_full_emailnetwork(reader) plots the social network from an mbox reader
    Args:
        reader (MBoxReader): [description]
    """
    emails = reader.extract()
    plt.figure(figsize=(12,12))
    G = nx.MultiDiGraph(name='Email Social Network')
    for email in emails:
        sender = email.sender.name
        source_addr = sender if sender != '' else email.sender.email.split('@')[0]

        all_recipients = [em.name if em.name !='' or None else em.email.split('@')[0] for em in email.recipients + email.cc]
        
        for recipient in all_recipients:
            G.add_edge(source_addr, recipient, message=email.subject)

    if layout == 'shell':
        pos = nx.shell_layout(G)
    elif layout == 'spring':
        pos = nx.spring_layout(G)
    else:
        pos = nx.spiral_layout(G)
    nx.draw(G, pos, node_size=0, alpha=0.4, edge_color="cadetblue", font_size=7, with_labels=True)
    ax = plt.gca()
    ax.margins(0.08)
    plt.show()



if __name__ == '__main__':
    # reader = MBoxReader('/Users/samuel/Footprints/emailnetwork/emailnetwork/tests/test.mbox')
    reader = MBoxReader('/Users/samuel/Footprints/samuel-supertype.mbox')
    # plot_single_email(reader,300)
    # plot_single_email(reader, 1, True)
    # plot_full_emailnetwork(reader, 646)
    # plot_full_emailnetwork(reader, "shell")