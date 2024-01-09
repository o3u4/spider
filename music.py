import requests
import json
from lxml import etree
from csv import writer
import time

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
     'AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/58.0.3029.110 Safari/537.3'


def page_search(key, page=None, current_url=None):
    url = ''
    if page and not current_url:
        url = f'http://www.2t58.com/so/{key}/{page}.html'
    elif current_url and not page:
        url = current_url
    headers = {'User-Agent': ua}
    resp = requests.get(url, headers=headers)
    data = resp.text
    html = etree.HTML(data)

    search_list_name = html.xpath("/html/body/div[1]/div/div[2]/ul/li/div[1]/a/text()")  # 搜索结果名称
    search_list_url = html.xpath("/html/body/div[1]/div/div[2]/ul/li/div[1]/a/@href")  # 搜索结果url
    search_list_order = [item.split('/')[-1].split('.')[0] for item in search_list_url]  # 搜索结果编号
    next_href_list = html.xpath('/html/body/div[1]/div/div[2]/div[2]/a[3]/@href')
    while len(next_href_list) == 0:  # 重新访问, 防止访问过快
        next_href_list = html.xpath('/html/body/div[1]/div/div[2]/div[2]/a[3]/@href')
    next_href = ('http://www.2t58.com' + next_href_list[0])
    # print(search_list_name)
    # print(search_list_url)
    # print(search_list_order)
    return search_list_name, search_list_order, next_href


def search(key):
    search_list_name, search_list_order, next_href = page_search(key, 1)
    print('搜索结果为:')
    print('-----------------------------------------------')
    prt(search_list_name)
    flag = input("是否下一页(是y, 否回车)")

    while flag:
        name_lst, order_lst, next_href = page_search(key, current_url=next_href)
        prt(name_lst, len(search_list_name))
        search_list_name += name_lst
        search_list_order += order_lst
        flag = input("是否下一页(是y, 否回车)")
    return search_list_name, search_list_order


def choose(lst1, lst2):
    lst = []
    order = int(input("选择序号"))
    lst.append(order)
    print(lst1[order], lst2[order])
    flg = input('继续下载(y或回车)')
    while flg:
        order = int(input("选择序号"))
        lst.append(order)
        print(lst1[order], lst2[order])
        flg = input('继续下载(y或回车)')
    with open("./歌曲编号.csv", mode='a', newline='') as f:
        wt = writer(f)
        wt.writerows([[lst1[num], lst2[num]] for num in lst])
    lst = [lst2[num] for num in lst]
    return lst


def prt(lst1, ori_num=0):
    # print(lst1)
    # print(lst2)   # lst2为删除参数, 输出编号
    for i in range(0, len(lst1)):
        print(ori_num + i, lst1[i])


def mp3_download(order):
    url = 'http://www.2t58.com/js/play.php'  # 接口获取mp3网址
    code = order  # 歌曲独特编号
    payload = {'id': code, 'type': 'music'}
    refer = f'http://www.2t58.com/song/{code}.html'  # 防盗链
    headers = {'Referer': refer, 'User-Agent': ua}

    response = requests.post(url, data=payload, headers=headers)  # 发送信息
    time.sleep(1)
    data = response.text

    # 解析 JSON 数据
    parsed_data = json.loads(data)
    # 提取 title 和 url 元素放入字典
    result = [parsed_data["title"], parsed_data["url"]]
    print(result)
    name = parsed_data["title"]
    mp3_url = result[1]
    resp = requests.get(mp3_url)

    # 写歌
    with open(f"./{name}.mp3", mode="wb") as f:
        f.write(resp.content)
    print(f"成功下载", name)


def lrc_download(name, order):
    # 下载LRC歌词
    url = f'http://www.2t58.com/song/{order}.html'
    headers = {'User-Agent': ua}
    resp = requests.get(url, headers=headers)

    html = etree.HTML(resp.text)

    lrc_libretto_url_list = html.xpath("/html/body/div[1]/div/div[2]/div[4]/a[2]/@href")
    lrc_libretto_url = 'http://www.2t58.com/' + lrc_libretto_url_list[0]
    # print(lrc_libretto_url)
    resp = requests.get(lrc_libretto_url, headers=headers)
    with open(f"./{name.lrc}", mode='wb') as f:
        f.write(resp.content)


if __name__ == '__main__':
    key_word = input("输入关键词:")
    name_list, order_list = search(key_word)
    r_code_list = choose(name_list, order_list)
    for r_code in r_code_list:
        mp3_download(r_code)
