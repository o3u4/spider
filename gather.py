import os


# file_lst = ['c.txt', 'b.txt', 'a.txt']    # 按指定顺序合并


def file_gather(folder_path, target_path, file_list=None):
    # 合并文件
    if file_list is None:
        file_list = os.listdir(folder_path)
    with open(target_path, 'wb') as merged_file:
        for file_name in file_list:
            file_path = folder_path + '/' + file_name
            with open(file_path, 'rb') as f:
                merged_file.write(f.read())


if __name__ == '__main__':
    file_gather('ab', 'abc;', ['c.txt', 'b.txt', 'a.txt'])
