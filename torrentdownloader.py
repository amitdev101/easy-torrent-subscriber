'''
EASY TORRENT SUBSCRIBER
In this project we are trying to download the latest top 100 torrents from 1337x.to using proxy.
1. go to proxy page and get some working proxies --done
2. after doing this show user the list of top 100 torrent available this week  --done
3. ask which torrent to add
4. update list for weekly animes
5. search options
6. store settings in a file 
7. build a proxy manager in case proxy isn't working --done

'''

import requests,os,webbrowser,random
from bs4 import BeautifulSoup as BS


ip =  "192.241.159.43"#128.199.145.187"
port = 8080#8888

proxy = ip + ":" + str(port)
#proxy = ""

proxydict = {"https": "https://"+proxy,
             "http" : "http://"+proxy,
             "ftp" : "ftp://"+proxy,
    }

def set_proxydict(proxy):
    global proxydict
    proxydict = {"https": "https://"+proxy,
             "http" : "http://"+proxy,
             "ftp" : "ftp://"+proxy,
    }
    print("proxy is set ",proxy)



def print_list(List):
    count = 0
    for item  in List:
        print(count," ",item)
        count = count+1

def print_torrent_list(MyList):
    List = MyList#[:]
    count = 0
    for item in List:
        print(count, end=" ")
        print(item.split("/")[-2]) #for 1337x.to 
        #print(item.split('/')[-1])
        #print(item)
        count = count + 1

class Links:
    def __init__(self,html_links,full_links):
        #html links are not full links
        self.html_links = html_links
        self.full_links = full_links



def Get_all_links(baselink,proxies = {}):
    '''
    Get_all_links will return all links on a page as a  List of class Links
    return type is a Class Links
    Elements  of Class Links type have two attributes html_links and full_links
    for example :
        My_Links = Get_all_links(baselink)
        all_full_links_list = My_Links.full_links
        all_html_links_list = My_Links.html_links
    '''
    r = requests.get(baselink,proxies = proxies)
    soup = BS(r.text,'html.parser')
    html_links = []
    full_links = []
    #print(dir(soup))
    for link in soup.find_all('a'):
        temp = link.get('href')
        html_links.append(temp)
        full_links.append(baselink+temp) #this is the full link
    All_links = Links(html_links,full_links)
    return All_links

def Get_proxies():
    '''
    Get_proxies() will return a list of available proxies as a list 
    '''
    #baselink = "https://free-proxy-list.net/" # 1 to 300
    #baselink = "https://www.sslproxies.org/"
    baselink = "https://www.us-proxy.org/" #1 to 200
    r = requests.get(baselink)
    soup = BS(r.text,'html.parser')
    t = soup.find_all('tr')
    proxies = []
    for link in t:
        #print(link.get_text())
        #print(link.contents)
        ip = link.contents[0]
        #print(ip)
        ip = ip.get_text()
        port = link.contents[1]
        #print(port)
        port = port.get_text()
        proxy = ip + ":" + port
        proxies.append(proxy)
    #print(dir(link))
    #print(type(link))
    #print_list(proxies)
    return proxies[1:200]
    

def proxy_manager(baselink):
    '''
    find a working proxy for the torrent site so that we can access the blocked site
    set our global dictionary proxydict to a given proxy
    and check whether we can open our website or not

    '''

    proxies = Get_proxies()
    #print_list(proxies)

    flag = 0
    i = random.randint(1,200)
    n = len(proxies)
    while(i<n and flag==0):
        proxy = proxies[i]
        proxydict = {"https": "https://"+proxy,
             "http" : "http://"+proxy,
             "ftp" : "ftp://"+proxy
        }
        try :
            r = requests.get(baselink,proxies = proxydict)
            print(i," proxy found ",proxy)
            set_proxydict(proxy)
            flag = 1
            return 
            
        except Exception as e:
            print("proxy does not work \n Trying new proxy")
        i = i+1

    print("No working proxy found")

                
def add_torrent(torrent_links):
    print("Enter the number of the torrent you want to download/add")
    i = int(input())
    url = torrent_links[i]
    url = url.replace("popular-movies/","")
    print("url is ",url)
    all_links = Get_all_links(url,proxydict)
    all_links = all_links.html_links 
    magnet_url_list =[link for link in all_links if "magnet" in link]
    magnet_url = magnet_url_list[0]
    webbrowser.open_new_tab(magnet_url)


    




def main():
    print(proxydict)
    torrent_sites = ["https://1337x.to/popular-movies","https://1337x.to/top-100", "https://www.torrentdownloads.me/most-active/"]
    mylink = torrent_sites[0] 
    
    
    
    #proxy_manager(mylink) 
    
    print("here is the value of proxydict:",proxydict)
    
    links_found = Get_all_links(mylink,proxies = proxydict)
    print_list(links_found.full_links)
    torrent_links = [link for link in links_found.full_links if "torrent" in link]
    print_torrent_list(torrent_links)
    add_torrent(torrent_links)


if __name__ == "__main__" :
    main()
