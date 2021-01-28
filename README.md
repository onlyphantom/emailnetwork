# Email Network

## Description
Network graphing utilities for email/mailbox data.

<img align="left" width="50%" src="https://github.com/onlyphantom/emailnetwork/blob/main/assets/graph1.png?raw=true" style="margin-right:10%">
<img align="left" width="50%" src="https://github.com/onlyphantom/emailnetwork/blob/main/assets/graph4.png?raw=true" style="margin-right:10%">
<img align="left" width="50%" src="https://github.com/onlyphantom/emailnetwork/blob/main/assets/graph3.png?raw=true" style="margin-right:10%">
<img align="left" width="50%" src="https://github.com/onlyphantom/emailnetwork/blob/main/assets/graph2.png?raw=true" style="margin-right:10%">


For the social scientists, creating social networks from your mailbox data and among other things:
* Discover subgroups within your organization (whether the different task forces established were as cohesive as it seems on the outside)  
* Study social actors (most emails from Marketing involve Peter and Andy) and their relative influence  
* Identify the key social groups (Sales team hangs out a lot, but the IT / product division less so)
* Key account managers of the company (Despite being with the company only recently, Margaretha is connected to more key clients than her peers)


If you're a graph theorist and looking for something more statistical:
* Support directed and undirected graphs (**implemented in version 0.0.2**, see below)
* Also output statistical measurements such as centrality distribution (**planned for version 0.0.3**)
* Betweenness, closeness, hubness, distance histograms plotting (**planned for version 0.0.3**) 
* Exports to `.graphml` format for use in other graphing software (**implemented in version 0.0.2**)

## Dependencies
* Python 3.7+
* Only dependencies are NetworkX and Matplotlib

## Example Usage
To install `emailnetwork`:
```
pip install emailnetwork
```

A sample `.mbox` file is provided to you, but you can obtain export your own mailbox from your email service provider. If you use Google (Gmail), you can [use the Google Takeout service](https://takeout.google.com/settings/takeout) to export your mail data.


```python
reader = MBoxReader('path-to-mbox.mbox')
print(f'{len(reader)} emails in the sample mbox.')

# extract a specific email
email = reader.mbox[5]
emailmsg = extract_meta(email)

# filter emails by certain date
thisyearmails = reader.filter_by_date('>=', '2021-01-05')

# print email domains of recipients
print(emailmsg.recipients)
print(emailmsg.recipients[0].domain)

# extract all emails
emails = reader.extract()
```

For graph visualization:
```py
# Read from .mbox
MBOX_PATH = f'{os.path.dirname(__file__)}/tests/test.mbox'
reader = MBoxReader(MBOX_PATH)

# Try the following: 
# plot a single directed graph the email at index 3
plot_single_directed(reader,3)

# plot a single undirected graph the email at index 3, show title in plot
plot_single_undirected(reader, 1, showtitle=True)

# plot a directed graph, optionally specifying a layout style
plot_directed(reader)
plot_directed(reader, 'shell')
# optionally export a .graphml to your working directory for use
# in other network / graphing software
plot_undirected(reader, 'spring', graphml=True)
```


##### Why Python 3.7+?
Python 3.7+ is required because the package is written to take advantage of many features of Python 3.7 and above. 

Examples of features that were used extensively in the creation of this package:
* [Dataclasses, new in Python 3.7](https://www.youtube.com/watch?v=sH_jLQvnpBo)
* [Insertion-ordered Dictionaries, new in Python 3.7](https://www.youtube.com/watch?v=h-DBWPjpqWY)
* [Typing (Type hints), new in Python 3.5](https://docs.python.org/3/library/typing.html)
* [Formatted string literal, new in Python 3.6](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)
## Testing
Git clone, and run `nosetests`. You can also run nosetests with coverage:
```
nosetests --with-coverage --cover-package=emailnetwork

.........
Name                       Stmts   Miss  Cover
----------------------------------------------
emailnetwork/__init__.py       2      0   100%
emailnetwork/emails.py        55     11    80%
emailnetwork/extract.py       54     11    80%
emailnetwork/graph.py        120     82    32%
emailnetwork/network.py       13      7    46%
emailnetwork/utils.py         32     17    47%
emailnetwork/version.py        1      0   100%
----------------------------------------------
TOTAL                        277    128    54%
----------------------------------------------------------------------
Ran 9 tests in 3.226s

OK
```

All tests are located in the `/tests/` directory.


## Authors and Copyright

Samuel Chan, Supertype [https://supertype.ai](https://supertype.ai)

If you find the code useful in your project, please link to this repository in your citation.

##### The MIT License (MIT)

Copyright (c) 2021 Supertype Pte Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.