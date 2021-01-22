import matplotlib.pyplot as plt
import networkx as nx
import textwrap

from emailnetwork.extract import MBoxReader, extract_meta


def plot_single_email(reader:MBoxReader, id:int=False):
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
    sender = emailmsg.sender.name if len(emailmsg.sender.name) != 0 else emailmsg.sender.email

    G = nx.DiGraph(name='Email Social Network')
    for recipient in emailmsg.recipients:
        rec = recipient.name
        G.add_edge(sender, rec if len(rec) != 0 else recipient.email, 
            message=subject, color='plum', weight=3)
    
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

    plt.tight_layout(pad=0.05)
    plt.axis('off')
    plt.show()


