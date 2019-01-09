'''
In this project we are trying to download the latest top 100 torrents from 1337x.to using proxy.
1. go to proxy page and get some working proxies 
2. after doing this show user the list of top 100 torrent available this week
3. ask which torrent to add
4. update list for weekly animes
5. search options
6. store settings in a file 

'''

import requests,os
from bs4 import BeautifulSoup as BS

ip = "128.199.145.187"
port = 8888

proxy = ip + ":" + str(port)

proxydict = {"https": "https://"+proxy,
             "http" : "http://"+proxy,
                
}

def print_list(List):
    for item  in List:
        print(item)

def print_torrent_list(List):
    count = 1
    for item in List:
        print(count, end=" ")
        print(item.split("/")[-2])
        #print(item)
        count = count + 1

class Links:
    def __init__(self,html_links,full_links):
        #html links are not full links
        self.html_links = html_links
        self.full_links = full_links



def Get_all_links(baselink,proxies = {}):
    r = requests.get(baselink,proxies = proxies)
    soup = BS(r.text,'html.parser')
    html_links = []
    full_links = []
    for link in soup.find_all('a'):
        temp = link.get('href')
        html_links.append(temp)
        full_links.append(baselink+temp) #this is the full link
    All_links = Links(html_links,full_links)
    return All_links

if __name__ == "__main__":
    links_found = Get_all_links("https://1337x.to/top-100",proxydict)
    torrent_links = [link for link in links_found.full_links if "torrent" in link]
    print_torrent_list(torrent_links)