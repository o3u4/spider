from tkinter import Tk, StringVar
from mv_spider import LocalSpider
from spider_ui import Ui


def submit():
    m3u8_url = [m3u8_url_entry.get()]
    print('m3u8文件网址更新为:', m3u8_url[0])
    video_name = video_name_entry.get()
    print('视频名称更新为:', video_name)
    return m3u8_url, video_name


def open_ts_file():
    folder_path = ui.open_file()
    current_text = 'ts文件保存地址'
    ts_path.set(folder_path)
    print(f'{current_text}更新为:', folder_path)


def open_mv_file():
    folder_path = ui.open_file()
    current_text = '视频保存位置'
    path = folder_path + '/' + video_name_entry.get() + '.mp4'
    movie_path.set(path)
    print(f'{current_text}更新为:', path)


def run():
    urls, name = submit()
    t_path = ts_path.get()
    mv_path = movie_path.get()
    LocalSpider.run_spider(name, urls, t_path, root=rot, prt_dl_label=dl_label)
    dl_label.config(text='下载完成')
    name_list = LocalSpider.get_name_list(name)
    LocalSpider.save_movie(t_path, mv_path, name_list, root=rot, label=gt_label)
    gt_label.config(text='合并完成')


rot = Tk()
rot.title("M3U8视频下载器")
ui = Ui(rot)
m3u8_url_label = ui.label("m3u8文件网址:")
m3u8_url_entry = ui.entry()

video_name_label = ui.label("视频名称:")
video_name_entry = ui.entry()

submit_button = ui.button("Submit", command=lambda: submit())

ts_path = StringVar()
ts_path.set('ts文件保存地址:')
ts_path_label = ui.label(var_text=ts_path)

ts_path_button = ui.button("选择ts文件夹", command=lambda: open_ts_file())

movie_path = StringVar()
movie_path.set("视频保存位置:")
movie_path_label = ui.label(var_text=movie_path)

movie_path_button = ui.button("选择视频文件夹", command=lambda: open_mv_file())

dl_label = ui.label()  # 下载进度条标签
gt_label = ui.label()  # 合并进度条标签

download_button = ui.button("开始下载", command=lambda: run())

rot.mainloop()
