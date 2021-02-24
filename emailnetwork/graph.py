from collections import Counter
import math
import os
import uuid
import matplotlib.pyplot as plt
import networkx as nx
import textwrap

from emailnetwork.extract import MBoxReader, extract_meta
from emailnetwork.network import PeopleCombination


def plot_single_directed(reader:MBoxReader, id:int=False, showtitle:bool=False) -> None:
    """
    Plot a directed graph from a single email, as determined by `id`. 
    If `showtitle` is `True`, render the plot with a email subject and date as title.

    Usage:
        reader = MboxReader('path-to-mbox.mbox')
        plot_single_directed(reader, 300) plots the 300th email from the mbox
    Args:
        reader (MBoxReader): A `MBoxReader` object
        id (int, optional): `id` of the email in the `MBoxReader`. Defaults to False.
        showtitle (bool, optional): If `True`, render the plot with a email subject and date as title. Defaults to False.
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

def plot_single_undirected(reader:MBoxReader, id:int=False, showtitle:bool=False) -> None:
    """
    Plot an undirected social network graph from a single email, as determined by `id`. 
    If `showtitle` is `True`, render the plot with a email subject and date as title.

    Usage:
        reader = MboxReader('path-to-mbox.mbox')
        plot_single_undirected(reader, 300) plots the 300th email from the mbox
    Args:
        reader (MBoxReader): A `MBoxReader` object
        id (int, optional): `id` of the email in the `MBoxReader`. Defaults to False.
        showtitle (bool, optional): If `True`, render the plot with a email subject and date as title. Defaults to False.
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

def plot_directed(reader:MBoxReader, layout:str='shell', graphml:bool=False) -> None:
    """
    Plot a directed social network graph from the entire `mbox`, supplied by `MBoxReader`. 
    `layout` determines the underlying `NetworkX` layout.   

    Usage:
        reader = MboxReader('path-to-mbox.mbox')
        plot_directed(reader)
    Args:
        reader (MBoxReader): A `MBoxReader` object
        layout (str, optional): Can be one of 'shell', 'spring' or 'spiral'. Defaults to 'shell'.
        graphml (bool, optional): Determines if a .graphml file is exported to the working directory. Defaults to False.
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

    if graphml:
        fileName = f'network-{str(uuid.uuid4().hex)[:8]}.graphml'
        nx.write_graphml(G, fileName)

    if layout == 'shell':
        pos = nx.shell_layout(G)
    elif layout == 'spring':
        pos = nx.spring_layout(G)
    else:
        pos = nx.spiral_layout(G)
    nx.draw(G, pos, node_size=0, alpha=0.4, edge_color='cadetblue', font_size=7, with_labels=True)
    ax = plt.gca()
    ax.margins(0.08)
    plt.show()

def plot_undirected(reader:MBoxReader, layout:str='shell', graphml:bool=False):
    """Plot an undirected social network graph from the entire `mbox`, supplied by `MBoxReader`. 
    `layout` determines the underlying `NetworkX` layout.   

    Usage:
        reader = MboxReader('path-to-mbox.mbox')
        plot_undirected(reader)

    Args:
        reader (MBoxReader): A `MBoxReader` object
        layout (str, optional): Can be one of 'shell', 'spring' or 'spiral'. Defaults to 'shell'.
        graphml (bool, optional): Determines if a .graphml file is exported to the working directory. Defaults to False.
    """

    emails = reader.extract()
    G = nx.Graph(name='Email Social Network')
    plt.figure(figsize=(12,12))
    counter = Counter()
    for email in emails:
        ng = PeopleCombination(email)
    
        for combo in ng.combo:
            counter[combo] += 1

    total_combos = sum(counter.values())
    by_freq = {k: v/total_combos for k, v in counter.most_common()}
    for rel in counter.keys():
        G.add_edge(*rel, weight=by_freq[rel], count=counter[rel])

    if graphml:
        fileName = f'network-{str(uuid.uuid4().hex)[:8]}.graphml'
        nx.write_graphml(G, fileName)
        print(f"Graphml exported as {fileName}")
    
    if layout == 'shell':
        pos = nx.shell_layout(G)
    elif layout == 'spring':
        k = 1/math.sqrt(G.order()) * 2
        pos = nx.spring_layout(G, k=k)
    else:
        pos = nx.spiral_layout(G)

    deg = [v*50 for _, v in G.degree()]
    nx.draw_networkx_nodes(G, pos, node_size=deg, linewidths=1.0, alpha=0.60)
    nx.draw_networkx_edges(G, pos, width=1.0, style='dashed', edge_color='cadetblue', alpha=0.6)
    nx.draw_networkx_labels(G, pos, {n: n.split('@')[0] for n in G.nodes}, font_size=8, font_color='darkorchid')

    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    MBOX_PATH = f'{os.path.dirname(__file__)}/tests/test.mbox'

    # reader = MBoxReader('/Users/samuel/Footprints/emailnetwork/emailnetwork/tests/test.mbox')
    reader = MBoxReader('/Users/vincentiuscalvin/Documents/Supertype/mbox-dataset/Ori_Sample_01.mbox')
    # reader = MBoxReader('/Users/samuel/Footprints/samuel-supertype.mbox')
    # plot_single_directed(reader,300)
    # plot_single_directed(reader, 1, True)
    # plot_directed(reader)
    # plot_directed(reader, "shell")
    plot_undirected(reader, 'spring')