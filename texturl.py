import requests
from requests import RequestException


def get_page_detail():
    heads = {
        'Host': 'www.toutiao.com',
        'User - Agent': 'Mozilla / 5.0(X11;Ubuntu;Linuxx86_64;rv: 58.0) Gecko / 20100101Firefox / 58.0',
        'Accept': 'text / html, application / xhtml + xml, application / xml; q = 0.9, * / *;q = 0.8',
        'Accept - Language': 'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
        'Accept - Encoding': 'gzip, deflate, br',
        'Cookie': 'tt_webid = 6525005387787650573;ga=GA1.2.724539875.1519220966;_gid=GA1.2.813069334.1519220966;uuid="w:a83a1e8139b34dd0ac75c9bca11bba11";UM_distinctid=161b8a3e8bf449-08ffd30ac04968-7c2d6751-1fa400-161b8a3e8c0497;tt_webid =6525005387787650573;tt_webid=6525005387787650573;WEATHER_CITY=%E5%8C%97%E4%BA%AC;CNZZDATA1259612802=1088548397-1519220448-https%253A%252F%252Fwww.baidu.com%252F%7C1519228587;__tasessionId=qhvl4wghb1519232654812',
        'Connection': 'keep - alive',
         'Upgrade - Insecure - Requests': 1
    }
    url = 'http://www.toutiao.com/a6505598931806716429/'
    try:
        response = requests.get('https'+url[4:])
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def main():
    print(get_page_detail())


if __name__ == '__main__':
    main()
