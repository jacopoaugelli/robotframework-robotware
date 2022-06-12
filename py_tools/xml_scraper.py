import requests
from bs4 import BeautifulSoup

#funzione che genera l'url dal quale ricavare la sitemap prendendo in input l'host
def url_gen(host):
    url1 = "http://" + host + "/sitemap"
    url2 = "http://" + host + "/sitemap.xml"
    if requests.get(url1).status_code == 200:
        return url1
    else:
        return url2




#funzione che prende l'url ed effettua lo scraping della sitemap.xml (restituisce una lista di tutti i link presenti nella sitemap)
def xml_scraper(url):

    scraped_urls = []
   
    
    r = requests.get(url)
    

    sp = BeautifulSoup(r.text, 'lxml')
    
    links = sp.find_all('loc')
    
    
    for link in links:
        scraped_urls.append((link.text + "/"))
    
    return scraped_urls


#funzione che per ogni url spiderato dalla funzione xml_scraper effettua una richiesta http ad una pagina presente nella wordlist dictionary
def dir_searcher(urls, dictionary):  

    ok_status = [] 
    
    for url in range(len(urls)): 
        for word in range(len(dictionary)):
             response = requests.get(urls[url] + dictionary[word]) 
        if response.status_code == 200:
            
            ok_status.append(urls[url] + dictionary[word]) 
        else:
                        
            print("Error 404: " + urls[url] + dictionary[word] + " does not exist") 
    return ok_status
       



#chiamata alla funzione che genera gli url spiderati dalla sitemap a partire dall'host input dell'utente
host = input()
scraped_urls = xml_scraper(url_gen(host))

#wordlist di prova
dict = ["skdjfhiksudhfoiusd", "robot"]

#test
print(dir_searcher(scraped_urls , dict))
