from flask import Flask, render_template, request, send_file
from music_class import Music
import asyncio
import os
import socket


def get_local_ip():     # 获取本地ip
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


app = Flask(__name__)
music = Music()
lst = []    # 获取歌曲编号
user_input = ''     # 获取搜索关键词


@app.route('/')
def index():    # 首页输入关键词
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def submit():   # 输出结果表格, 选择下载对象
    global lst, user_input
    page = request.args.get('page', default=1, type=int)
    if page == 1:   # 访问第一页需要提前输入关键词
        user_input = request.form['user_input']
    list1, list2, next_page = music.page_search(user_input, page=page)  # 名称, 编号
    lst = list2
    order_list = [i for i in range(len(list1))]     # 序号
    return render_template('result.html',
                           key=user_input, page=page,
                           order_list=order_list,
                           list1=list1, list2=list2,
                           next_page=f'http://{get_local_ip()}:5000/search?page={page + 1}')


@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':    # 以请求发送的需要先下载
        numbers = request.form['order']     # 获取输入的下载序号
        if numbers != '':
            numbers_list = [int(num) for num in numbers.split(' ')]
            order_list = [lst[num] for num in numbers_list]
            asyncio.run(music.main(order_list))
    msc_list = os.listdir('mp3')    # 列出文件夹所有文件
    order_list = [i for i in range(len(msc_list))]
    link_list = [f'http://{get_local_ip()}:5000/download/{name}' for name in msc_list]
    return render_template('package.html',
                           order_list=order_list, msc_list=msc_list, link_list=link_list)


@app.route('/download/<path:filename>')
def download_file(filename):    # 传输文件
    # 指定要提供下载的文件路径
    file_path = './mp3/' + filename
    # 使用send_file函数将文件提供为下载链接
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')     # host='0.0.0.0'可以被他人访问
