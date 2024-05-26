from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# selenium__version__ = "3.141.0"
# https://registry.npmmirror.com/binary.html
# https://registry.npmmirror.com/binary.html?path=chromedriver/
# https://registry.npmmirror.com/binary.html?path=chrome-for-testing/

def login_by_StudentID(driver):
    driver.find_elements(By.XPATH, '//*[@id="qStudentID"]')[0].click()
    school = driver.find_elements(By.XPATH, '//*[@id="quickSearch"]')[0]
    stu_id = driver.find_elements(By.XPATH, '//*[@id="clCode"]')[0]
    pswd = driver.find_elements(By.XPATH, '//*[@id="clPassword"]')[0]
    school.send_keys('宁波大学')
    stu_id.send_keys('226002287')
    pswd.send_keys('Twhzs233')


def select_course(driver):
    """
    选择课程
    :param driver:
    :return:
    """
    # 打开网页
    log_in = ("https://passport.zhihuishu.com/"
              "login?service=https://onlineservice-api.zhihuishu.com/gateway/f/v1/login/gologin")

    driver.get(log_in)

    login_by_StudentID(driver)
    input("输入验证码, 跳出完整页面后, 按任意键继续")

    courses_xpath = '//*[@id="sharingClassed"]/div[2]/ul'
    courses_list = driver.find_elements(By.XPATH, courses_xpath)

    course_elements = []  # 所有课程列表
    i = 0
    for courses in courses_list:
        course_xpath = './div/dl/dt/div[1]/div[1]'
        course_element = courses.find_element(By.XPATH, course_xpath)
        course_elements.append(course_element)
        txt = course_element.text
        print(i, txt)
        i += 1

    n = int(input("输入所选课程:"))
    course_elements[n].click()

    # time.sleep(6)
    input("等待课程跳出后, 按任意键继续")
    # 关闭叉
    # //*[@id="app"]/div/div[6]/div[@class="dialog-read"]
    xx_xpath = '//*[@id="app"]/div/div[6]/div[2]/div[@class="el-dialog__header"]/i[@class="iconfont iconguanbi"]'
    xx = driver.find_elements(By.XPATH, xx_xpath)
    if xx:
        xx[0].click()


def get_class(driver):
    """
    获取所有课程信息
    :param driver:
    :return:
    """
    chapters_xpath = '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div/ul'  # 所有章节

    while 1:
        chapters = driver.find_elements(By.XPATH, chapters_xpath)
        if len(chapters) >= 2:
            break
        else:
            time.sleep(1)
    return chapters


def find_first_cls(chaps):
    """
    返回第一个未完成的课程的 element (要求全屏化界面)
    :return:
    class_elements[n], t, c, n: 课程, 时长, 章节, 章节内课程序号
    """

    c = 0
    for chapter in chaps:
        c += 1
        # 先找直接能看的第一级视频
        clickable_classes = chapter.find_elements(By.XPATH, './div/li[@class="clearfix video"]')
        if not clickable_classes:   # 找不到课, 可能是还有分级
            clickable_classes = chapter.find_elements(By.XPATH, './div/ul/li[@class="clearfix video"]')
        n = 0
        for classes in clickable_classes:
            n += 1
            class_element = classes.find_elements(By.XPATH, './div/span')[0]  # 每个课的element
            is_finished_ = class_element.find_elements(By.XPATH, '..//b[@class="fl time_icofinish"]')
            # 是否完成
            if is_finished_:
                continue
            else:
                print(class_element.text)
                ts = classes.find_elements(By.XPATH, f'./div/div/span')
                if not ts:
                    ts = classes.find_elements(By.XPATH, f'./div/span[2]')
                if ts:
                    t = ts[0].text
                else:
                    t = 0
                return class_element, t, c, n  # 返回该课
    return None


def speed_run(driver):
    """
    倍速播放
    :param driver:
    :return:
    """
    while True:  # 点击播放
        videos_xpath = '//*[@id="vjs_container"]/div[8]'
        videos = driver.find_elements(By.XPATH, videos_xpath)
        if videos:
            video = videos[0]
            actions = ActionChains(driver)
            actions.move_to_element(video).perform()  # 移动鼠标到视频上
            run_xpath = '//*[@id="playButton"]'
            run = driver.find_elements(By.XPATH, run_xpath)
            if run:
                try:
                    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, run_xpath)))
                    run[0].click()  # 播放按钮开始播放
                    time.sleep(1)
                    if exam_code(driver):  # 检查是否有验证码
                        input("出现验证码")
                    else:
                        answer(driver)  # 防止直接跳出题目
                    break
                except:
                    print("Play button Element is not clickable. Trying again...")
                    # 防止 WebDriverWait 一直等不到按钮可点击
                    if exam_code(driver):  # 检查是否有验证码
                        input("出现验证码")
                    else:
                        answer(driver)  # 防止直接跳出题目
            else:
                print("Play button Element not found. Trying again...")
        else:   # 没找到视频
            print("Can't find video. Trying again...")
            time.sleep(2)
            break

    while True:  # 点击倍速
        videos_xpath = '//*[@id="vjs_container"]/div[8]'
        video = driver.find_elements(By.XPATH, videos_xpath)[0]
        actions = ActionChains(driver)
        actions.move_to_element(video).perform()  # 移动鼠标到视频上
        time.sleep(0.5)  # 可以删除
        spd_box_xpath = '//*[@id="vjs_container"]/div[10]/div[@class="speedBox"]/span'
        box = driver.find_elements(By.XPATH, spd_box_xpath)[0]
        actions = ActionChains(driver)
        actions.move_to_element(box).perform()  # 移动鼠标到倍速选项上

        spd_xpath = ('//*[@id="vjs_container"]/div[10]/div[@class="speedBox"]/div[@class="speedList"]'
                     '/div[@class="speedTab speedTab15"]')

        spd_elements = driver.find_elements(By.XPATH, spd_xpath)
        if spd_elements:
            spd = spd_elements[0]
            try:
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, spd_xpath)))
                spd.click()
                break
            except:
                print("Speed Element is not clickable. Trying again...")
        else:
            print("Speed Element not found. Trying again...")


def iter_class(driver):
    """
    循环播放视频
    :param driver:
    :return:
    """
    selected_class, class_tm, selected_chap, order = (
        find_first_cls(get_class(driver)))
    selected_class.click()
    print(class_tm)  # 00:06:11
    time.sleep(2)  # 可以删除, 防止直接跳题目
    if exam_code(driver):  # 检查是否有验证码
        input("出现验证码")
    elif answer(driver):  # 防止直接跳出题目
        pass
    else:
        time.sleep(2)
        speed_run(driver)

    return selected_class, selected_chap, order


def is_finished(cls):
    """
    不断判断是否完成视频
    :param cls:  视频元素
    :return:
    """
    xpath = '..//b[@class="fl time_icofinish"]'
    elements = cls.find_elements(By.XPATH, xpath)
    if elements:
        return True
    else:
        return False


def answer(driver):
    """
    若出现问题, 则回答A, 然后关闭问题, 然后点击播放
    :param driver:
    :return:
    """
    tanchuang = '//*[@id="playTopic-dialog"]/div'
    tc = driver.find_elements(By.XPATH, tanchuang)
    if tc:
        print('遇到问题, 即将自动回答')
        option_xpath = '//*[@id="playTopic-dialog"]/div/div[2]/div/div[1]/div/div/div[2]/ul/li'
        options = driver.find_elements(By.XPATH, option_xpath)
        options[0].click()  # 尝试答案
        close_xpath = '//*[@id="playTopic-dialog"]/div/div[3]/span/div'
        close = driver.find_elements(By.XPATH, close_xpath)
        close[0].click()  # 关闭
        print('回答完毕')

        time.sleep(2)  # 可以删除
        speed_run(driver)
        return True
    else:
        return False


def exam_code(driver):
    """
    手动做验证码
    :return:
    """
    title_xpath = '/html/body/div[5]/div[2]/div/div/div[1]/span[2]'
    title = driver.find_elements(By.XPATH, title_xpath)
    if title:
        return True
    else:
        return False


def question_button(driver):
    question_xpath = '//*[@id="app"]/div/div[2]/div[1]/div[3]/ul/li'
    question = driver.find_elements(By.XPATH, question_xpath)
    if question:
        question[0].click()


if __name__ == '__main__':
    # 设置谷歌浏览器驱动路径
    driver_path = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"

    # 创建一个谷歌浏览器实例
    chrome_driver = webdriver.Chrome(executable_path=driver_path)  # 同级目录下可不写
    chrome_driver.maximize_window()  # 最大化显示
    select_course(chrome_driver)
    print("开始课程观看")
    selected_cls, selected_chap, order = iter_class(chrome_driver)
    time.sleep(2)  # 防止直接跳出题目没被检测到
    while 1:  # 每5秒检测是否完成
        if exam_code(chrome_driver):
            input("出现验证码")
        else:
            answer(chrome_driver)
            if is_finished(selected_cls):
                selected_cls, selected_chap, order = iter_class(chrome_driver)
        time.sleep(5)
