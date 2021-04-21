#Chloe Flores
#Project 2

import urllib.request, urllib.parse, urllib.error
from collections import deque

def byte2str(b):
    """
    Input: byte sequence b of a string
    Output: string form of the byte sequence
    Required for python 3 functionality
    """
    return "".join(chr(a) for a in b)

def getLinks(url,baseurl="http://secon.utulsa.edu/cs2123/webtraverse/"):
    """
    Input: url to visit, Boolean absolute indicates whether URLs should include absolute path (default) or not
    Output: list of pairs of URLs and associated text
    """
    #import the HTML parser package 
    try:
        from bs4 import BeautifulSoup
    except:
        print('You must first install the BeautifulSoup package for this code to work')
        raise
    #fetch the URL and load it into the HTML parser
    soup = BeautifulSoup(urllib.request.urlopen(url).read(),features="html.parser")
    #pull out the links from the HTML and return
    return [baseurl+byte2str(a["href"].encode('ascii','ignore')) for a in soup.findAll('a')]

def print_dfs(url):
    """
    Print all links reachable from a starting **url** 
    in depth-first order
    """
    temp = {}
    dfsD = createDictionary(url, temp)
    print(dfs(dfsD, url))
    

def print_bfs(url):
    """
    Print all links reachable from a starting **url** 
    in breadth-first order
    """
    temp = {}
    bfsD = createDictionary(url, temp)
    print(bfs(bfsD,url))


def find_shortest_path(url1,url2):
    """
    Find and return the shortest path
    from **url1** to **url2** if one exists.
    If no such path exists, say so.
    """
    dict = pathShortD()
    P = bfs_parents(dict,"http://secon.utulsa.edu/cs2123/webtraverse/index.html")
    path = [url2]
    u = url2
    xx = True
    while P[u] != url1:
        if P[u] is None: #give up if we find the root
            print('path not found')
            xx = False
            break
        path.append(P[u])
        u = P[u]
    
    path.append(P[u]) #don't forget to add the source
    path.reverse()    #reorder the path to start from url1
    if xx: 
        print(path)

def bfs_parents(G, s):
    P, Q = {s: None}, deque([s])# Parents and FIFO queue
    while Q:
        u = Q.popleft()         # Constant-time for deque
        for v in G[u]:
            if v in P: continue # Already has parent
            P[v] = u            # Reached from u: u is parent
            Q.append(v)
    return P

def find_max_depth(start_url):
    """
    Find and return the URL that is the greatest distance from start_url, along with the sequence of links that must be followed to reach the page.
    For this problem, distance is defined as the minimum number of links that must be followed from start_url to reach the page.
    """
    temp= {}
    maxDepthD = createDictionary(start_url, temp)
    maxDepthS = bfs(maxDepthD,start_url)
    farLink = list(maxDepthS)[len(maxDepthS)-1]
    find_shortest_path(start_url,farLink)
    #shortest path to farthest link

    


def pathShortD():
    temp = {}
    return createDictionary("http://secon.utulsa.edu/cs2123/webtraverse/index.html",temp)
    
def createDictHelper(links, dictionary):
    for link in links:
        createDictionary(link,dictionary)

def createDictionary(url, dictionary):
    base = getLinks(url)
    for item in base:
        if item not in dictionary:
            dictionary.update({item:getLinks(item)})
            createDictHelper(getLinks(item), dictionary)
    return dictionary


def dfs(G,s):
    S, Q = [], []       # Visited-set and queue
    Q.append(s)            # We plan on visiting s
    while Q:               # Planned nodes left?
        u = Q.pop()        # Get one
        if u in S: continue# Already visited? Skip it
        S.append(u)           # We've visited it now
        Q.extend(G[u])     # Schedule all neighbors
    return S          # Report u as visited

def bfs(Dict, link):
    S, Q = [], deque()
    Q.append(link)
    while Q:                 
        u = Q.popleft()  
        if u in S: continue
        S.append(u)    
        Q.extend(Dict[u])
    return S  


if __name__=="__main__":
    starturl = "http://secon.utulsa.edu/cs2123/webtraverse/index.html"
    print("*********** (a) Depth-first search   **********")
    print_dfs(starturl)
    print("*********** (b) Breadth-first search **********")
    print_bfs(starturl)
    print("*********** (c) Find shortest path between two URLs ********")
    find_shortest_path("http://secon.utulsa.edu/cs2123/webtraverse/index.html","http://secon.utulsa.edu/cs2123/webtraverse/wainwright.html")
    find_shortest_path("http://secon.utulsa.edu/cs2123/webtraverse/turing.html","http://secon.utulsa.edu/cs2123/webtraverse/dijkstra.html")
    print("*********** (d) Find the longest shortest path from a starting URL *****")
    find_max_depth(starturl)