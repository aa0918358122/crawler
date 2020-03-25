import requests
from bs4 import BeautifulSoup
import re
import json
import os
import moment
from datetime import datetime

def FTV(req):
    # a = requests.get('https://api.ftvnews.com.tw/api/FtvGetNews?Cate=POL&Page=1&Sp=18')
    save_list = []
    data = eval(req.text)['ITEM']
    for item in data:
        article_name = item['ID']
        date = moment.date(article_name[:-5], '%Y%m%d').date
        date = datetime.strftime(date, '%Y%m%d')
        article_name = article_name.replace(article_name[:-5], date)
        article_name = article_name[:-5] + '-' + article_name[-5:]
        article = ''
        soup1 = BeautifulSoup(item['Preface'], 'html.parser')
        text1 = soup1.getText()
        article += text1
        soup2 = BeautifulSoup(item['Content'], 'html.parser')
        text2 = soup2.getText()
        article += text2
        article = re.sub(r'(--【.*?】|【.*?】|（民視新聞.*|更多最新消息.*)', '', article)
        save_dict = dict()
        save_dict['filename'] = article_name
        save_dict['article'] = article
        save_dict['raw_data'] = req.text
        save_list.append(save_dict)
    return save_list

def CT(req):
    # a = requests.get('https://www.chinatimes.com/politic/PageListTotal/?page=1&_=1582217556616')
    save_list = []
    data = eval(req.text)['list']
    for item in data:
        URL = re.findall('.+', item['HyperLink'])
        name = re.findall('\d{14}', item['HyperLink'])
        article_name = name[0][:8] + '-' + name[0][8:]
        b = requests.get('https://www.chinatimes.com'+URL[0]+'?chdtv')
        soup = BeautifulSoup(b.text, 'html.parser')
        tag = soup.find(class_='article-body')
        article = ''
        for link in tag.find_all(name='p'):
            text = link.getText()
            article += text
        article = re.sub(r'(\(中時.*|\(工商.*|更多 CTWANT.*|\(中國時報.*)', '', article)
        save_dict = dict()
        save_dict['filename'] = article_name
        save_dict['article'] = article
        save_dict['raw_data'] = b.text
        save_list.append(save_dict)
    return save_list

def PTS(req):
    # a = requests.get('https://news.pts.org.tw/subcategory/9')
    save_list = []
    soup1 = BeautifulSoup(req.text, 'html.parser')
    for link1 in soup1.find_all(class_='news-right-list'):
        for link2 in link1.find_all(name='a'):
            URL = link2.get('href')
            name = re.findall('\d+', URL)
            b = requests.get(URL)
            soup2 = BeautifulSoup(b.text, 'html.parser')
            tag1 = soup2.find(class_='maintype-wapper hidden-lg hidden-md').getText()
            date = moment.date(tag1[:10], '%Y%m%d').date
            date = datetime.strftime(date, '%Y%m%d')
            article_name = date + '-' + name[0]
            tag2 = soup2.find(class_='article_content')
            article = tag2.text
            article = article.strip().replace('\n', '').replace('\xa0', '')
            save_dict = dict()
            save_dict['filename'] = article_name
            save_dict['article'] = article
            save_dict['raw_data'] = b.text
            save_list.append(save_dict)
    return save_list

def CNA(req):
    # a = requests.get('https://www.cna.com.tw/cna2018api/api/simplelist/categorycode/aipl/pageidx/1/')
    save_list = []
    data = eval(req.text)['result']['SimpleItems']
    for item in data:
        URL = re.findall('.+', item['PageUrl'])
        article_name = re.findall('\d+', item['PageUrl'])
        article_name = article_name[0][:8] + '-' + article_name[0][8:]
        b = requests.get(URL[0])
        soup = BeautifulSoup(b.text, 'html.parser')
        tag = soup.find(class_='paragraph')
        article = ''
        for link in tag.find_all(name='p'):
            text = link.getText()
            article += text
        article = re.sub(r'(（編輯：.*|.*電）)', '', article)
        save_dict = dict()
        save_dict['filename'] = article_name
        save_dict['article'] = article
        save_dict['raw_data'] = b.text
        save_list.append(save_dict)
    return save_list

def LTN(req):
    # a = sequests.get('https://news.ltn.com.tw/ajax/breakingnews/politics/1')
    save_list = []
    data = json.loads(req.text)['data']
    for item in data:
        URL = re.findall('.+', item['url'])
        name = re.findall('\d+', item['url'])
        b = requests.get(URL[0])
        soup = BeautifulSoup(b.text, 'html.parser')
        tag1 = soup.find(class_='time').getText()
        date = moment.date(tag1, '%Y%m%d').date
        date = datetime.strftime(date, '%Y%m%d')
        article_name = date + '-' + name[0]
        tag2 = soup.find(class_='text boxTitle boxText')
        for link in tag2.find_all(name='p', class_='appE1121'):
            link.decompose()
        for link in tag2.find_all(class_='photo boxTitle'):
            link.decompose()
        for link in tag2.find_all(name='p', class_='before_ir'):
            link.decompose()
        article = ''
        for link in tag2.find_all(name='p'):
            text = link.getText()
            article += text
        article = re.sub(r'(.*］|.*〕|武漢肺炎懶人包.*|（.*記者.*）)', '', article)
        save_dict = dict()
        save_dict['filename'] = article_name
        save_dict['article'] = article
        save_dict['raw_data'] = b.text
        save_list.append(save_dict)
    return save_list

def PChome(req):
    # a = requests.get('http://news.pchome.com.tw/cat/politics/hot/1')
    save_list = []
    soup1 = BeautifulSoup(req.text, 'html.parser')
    for link1 in soup1.find_all(class_='channel_newssection'):
        for link2 in link1.find_all(name='a', limit=1):
            URL = link2.get('href')
            name = re.findall('\d+', URL)
            article_name = name[0] + '-' + name[1]
            b = requests.get('http://news.pchome.com.tw'+URL)
            soup2 = BeautifulSoup(b.text, 'html.parser')
            tag = soup2.find(id='newsContent')
            article = tag.text
            article = re.sub(r'(（.*電）|【.*?】|（圖.*）|照片來源：.*|《更多匯流新聞網報導》.*|（作者.*|\(作者.*)', '', article)
            article = re.sub(r'.*／.*?報導', '', article, 1)
            save_dict = dict()
            save_dict['filename'] = article_name
            save_dict['article'] = article.strip()
            save_dict['raw_data'] = b.text
            save_list.append(save_dict)
    return save_list

def NOW(req):
    # a = requests.get('https://www.nownews.com/cat/politics/page/1/')
    save_list = []
    soup1 = BeautifulSoup(req.text, 'html.parser')
    for link1 in soup1.find_all(class_='entry-title td-module-title'):
        for link2 in link1.find_all(name='a'):
            URL = link2.get('href')
            name = re.findall('\d+', URL)
            article_name = name[0] + '-' +name[1]
            b = requests.get(URL)
            soup2 = BeautifulSoup(b.text, 'html.parser')
            tag = soup2.find(itemprop='articleBody')
            article = ''
            for link3 in tag.find_all(name='p'):
                text = link3.getText()
                article += text
            article = re.sub(r'※.*', '', article)
            article = re.sub(r'【.*?】.*|（編輯.*|￼', '', article)
            save_dict = dict()
            save_dict['filename'] = article_name
            save_dict['article'] = article
            save_dict['raw_data'] = b.text
            save_list.append(save_dict)
    return save_list

def crawler(url):
    a = requests.get(url)
    news = re.findall('ftvnews|chinatimes|pts|cna|ltn|pchome|nownews', url)
    if news[0] == 'ftvnews':
        return FTV(a)
    elif news[0] == 'chinatimes':
        return CT(a)
    elif news[0] == 'pts':
        return PTS(a)
    elif news[0] == 'cna':
        return CNA(a)
    elif news[0] == 'ltn':
        return LTN(a)
    elif news[0] == 'pchome':
        return PChome(a)
    elif news[0] == 'nownews':
        return NOW(a)

if '__main__' == __name__:
    websites = [#'https://api.ftvnews.com.tw/api/FtvGetNews?Cate=POL&Page=1&Sp=18',
                #'https://www.chinatimes.com/politic/PageListTotal/?page=1&_=1582217556616',
                #'https://news.pts.org.tw/subcategory/9',
                #'https://www.cna.com.tw/cna2018api/api/simplelist/categorycode/aipl/pageidx/1/',
                #'https://news.ltn.com.tw/ajax/breakingnews/politics/1',
                #'https://news.pchome.com.tw/cat/politics/hot/1',
                'https://www.nownews.com/cat/politics/page/1/']
    for i, website in enumerate(websites):
        for element in crawler(website):
            name = element['filename']
            context = element['article']
            html = element['raw_data']
            print(name)
            #if not os.path.exists('articles_politics'):
            #    os.mkdir('articles_politics')
            #if not os.path.exists(f'articles_politics/{i+1}'):
            #    os.mkdir(f'articles_politics/{i+1}')
            #with open(f'./articles_politics/{i+1}/{i+1}-{name}', 'w') as f:
            #    f.write(context)
            #if not os.path.exists('htmls_politics'):
            #    os.mkdir('htmls_politics')
            #if not os.path.exists(f'htmls_politics/{i+1}'):
            #    os.mkdir(f'htmls_politics/{i+1}')
            #with open(f'./htmls_politics/{i+1}/{i+1}-{name}.html', 'w') as f:
            #    f.write(html)
