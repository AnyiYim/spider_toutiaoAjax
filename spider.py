import json
from urllib.parse import urlencode
from hashlib import md5
import os
from requests.exceptions import RequestException
import requests
from bs4 import BeautifulSoup
import re
from config import *
import pymongo


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_page_index(offset, keyword):
    data = {
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'format': 'json',
        'from': 'gallery',
        'keyword': keyword,
        'offset': offset
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None


def get_page_detail(url):
    heads = {
        'Host': 'www.toutiao.com',
        'User - Agent': 'Mozilla / 5.0(X11;Ubuntu;Linuxx86_64;rv: 58.0) Gecko / 20100101Firefox / 58.0',
        'Accept': 'text / html, application / xhtml + xml, application / xml; q = 0.9, * / *;q = 0.8',
        'Accept - Language': 'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
        'Accept - Encoding': 'gzip, deflate, br',
        # 'Cookie': 'tt_webid = 6525005387787650573;ga=GA1.2.724539875.1519220966;_gid=GA1.2.813069334.1519220966;uuid="w:a83a1e8139b34dd0ac75c9bca11bba11";UM_distinctid=161b8a3e8bf449-08ffd30ac04968-7c2d6751-1fa400-161b8a3e8c0497;tt_webid =6525005387787650573;tt_webid=6525005387787650573;WEATHER_CITY=%E5%8C%97%E4%BA%AC;CNZZDATA1259612802=1088548397-1519220448-https%253A%252F%252Fwww.baidu.com%252F%7C1519228587;__tasessionId=qhvl4wghb1519232654812',
        'Connection': 'keep - alive',
        # 'Upgrade - Insecure - Requests': 1
    }
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            url = item.get('article_url')
            if url.startswith('http://tou'):
                yield url[:19]+'a'+url[25:]


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.title.string
    # print(title)
    img_pattern = re.compile('gallery: JSON.parse\("(.*?)"\),.*?lingList:', re.S)
    result = re.search(img_pattern, html)
    if result:
        rejson = (result.group(1)).replace('\\"', '"').replace('\\\\/', '/')
        # print(rejson)
        data = json.loads(rejson)
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            imgs = [item.get('url') for item in sub_images]
            for img in imgs:
                download_image(img)
            return {
                'title': title,
                'url': url,
                'images': imgs
            }


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print(result)
        return True
    return False


def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片出错')
        return None


def save_image(content):
      file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(),'jpg')
      if not os.path.exists(file_path):
          with open(file_path, 'wb') as f:
              f.write(content)
              f.close()


def main(time):
    for i in range(time):
        html = get_page_index(i*10, KEYWORD)
        for url in parse_page_index(html):
            print(url)
        for url in parse_page_index(html):
            html = get_page_detail(url)
            if html:
                result = parse_page_detail(html, url)
                save_to_mongo(result)


if __name__ == '__main__':
    main(10)


