import time


def progress_bar(total, progress, color='default'):
    colors = {
        'default': '█',
        'black': '\033[30m█\033[0m',
        'red': '\033[31m█\033[0m',
        'green': '\033[32m█\033[0m',
        'yellow': '\033[33m█\033[0m',
        'blue': '\033[34m█\033[0m',
        'magenta': '\033[35m█\033[0m',
        'cyan': '\033[36m█\033[0m',
        'white': '\033[37m█\033[0m',
        'reset': '\033[0m'
    }
    bar_length = 50     # 条总长
    filled_length = int(bar_length * progress // total)     # 当前进度占长
    bar = colors[color] * filled_length + '-' * (bar_length - filled_length)      # 构建字符串
    percentage = progress / total * 100     # 百分比
    print(f'\rProgress: [{bar}] {percentage:.1f}%  {progress}/{total}', end='', flush=True)
    # end=''不换行, flush=True, 立即将输出刷新到终端


if __name__ == '__main__':
    # 示例用法
    total_progress = 150
    for i in range(total_progress + 1):
        progress_bar(total_progress, i)
        time.sleep(0.1)
