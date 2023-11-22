from csv import writer
from lxml import etree
import requests

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}

# 发送请求
url = 'https://piaofang.maoyan.com/rankings/year'
response = requests.get(url, headers=headers)

# 解析网页内容
html = etree.HTML(response.text)

# 使用XPath定位元素
name_list = html.xpath('//*[@id="ranks-list"]/ul/li[2]/p[1]/text()')
time_list = html.xpath('//*[@id="ranks-list"]/ul/li[2]/p[2]/text()')
piaofang_list = html.xpath('//*[@id="ranks-list"]/ul/li[3]/text()')
for year in range(2013, 2024):
    with open(f'data/{year}.csv', 'w') as csvfile:
        writer = writer(csvfile)
        writer.writerow(['名称', '年份', '票房'])
        for i in range(len(name_list)):
            mv_year = time_list[i].split('-')[0]
            if mv_year == str(year):
                writer.writerow([name_list[i], time_list[i], piaofang_list[i]])
