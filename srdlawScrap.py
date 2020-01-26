from bs4 import BeautifulSoup
import requests
import re
from flask import Flask, jsonify,request

# Init
app = Flask(__name__)

home_output = {}
detail_output = {}
base_url = 'https://www.srdlawnotes.com/'


class Scrapyhome:

    def home_scrap(self,base_url:str):
        source = requests.get(base_url).text
        soup = BeautifulSoup(source, 'lxml')
        for index,data in enumerate(soup.find_all('article')):
            # print(data.h2.a.text)
            # print(data.h2.a['href'])
            # print(data.find('div',class_='post-body entry-content').p.text)
            home_output[index] = { }
            home_output[index]["id"] = str(index)
            home_output[index]["title"] = data.h2.a.text
            home_output[index]["link"] = data.h2.a['href']
            home_output[index]["short_description"]= data.find('div',class_='post-body entry-content').p.text
        return home_output

    def detail_Scrap(self,link:str):
        source = requests.get(link).text
        soup = BeautifulSoup(source,'lxml')
        detail_output['title'] = soup.find('div', class_='post-body entry-content').div.h3.text
        a=soup.find('div',class_='post-body entry-content').div.text
        detail_output['article_message']=re.split("See Also...",a)[0]
        return detail_output

    def search_scrap(self,search_term:str):
        if ' ' in search_term:
            search_term = search_term.replace(' ','+')
        url = f"{base_url}/search?q={search_term}"
        search_output = self.home_scrap(base_url=url)
        print(search_term)
        return search_output

def get():
    for i in home_output:
        print(home_output[i]['link'])

# print(Scrapyhome().home_scrap(base_url))
# Scrapyhome().detail_Scrap(home_output[0]['link'])
# print(detail_output)
# Scrapyhome().search_scrap('scope of jurisprudence')
# print(home_output)
# for i in home_output:
#     print(home_output[i]['title'])
# api routing
@app.route('/api/v1/get')
def GetHome():
    return jsonify(Scrapyhome().home_scrap(base_url))

@app.route('/api/v1/details',methods = ['GET'])
def DetailOut():

    a = request.args.get('link',default='*',type=str)
    print(a)
    return jsonify(Scrapyhome().detail_Scrap(a))

@app.route('/api/v1/search')
def searchout():
    a = request.args.get('term',default='*',type=str)
    print(a)
    return jsonify(Scrapyhome().search_scrap(a))

if __name__== '__main__':
    app.run(debug=True)