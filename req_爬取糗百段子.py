#encoding:UTF-8
import requests
from bs4 import BeautifulSoup

def getResponse(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
       return "error"


def dealRsp(response):
    soup  = BeautifulSoup(response, "html")
    with open(r'./qiubai.txt', 'w') as fp: 
        for i in soup.find_all("div", class_="content"):
            print(i.span.get_text())
            fp.write(i.span.get_text())
        print("successful")
    fp.close()

def main():
    url = "http://www.qiushibaike.com/hot/page/1"
    response = getResponse(url)
    dealRsp(response)

if __name__ == "__main__":
    main()
