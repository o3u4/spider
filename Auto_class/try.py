from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 226002287 Twhzs233
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
    pswd.send_keys('xxxxxxx')


def select_course(driver):
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


def get_class(driver):

    # xx_xpath = '//*[@id="app"]/div/div[6]/div[2]/div[1]/i'
    # # time.sleep(2)
    # xx = driver.find_elements(By.XPATH, xx_xpath)  # 叉
    # if xx:
    #     xx[0].click()

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
        # chapters_name_xpath = './li[1]/span[3]'
        # //*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div/ul[1]/li[1]/span[3]
        # //*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div/ul[1]/div[1]/li/div/span
        # chapters_name = chapter.find_element(By.XPATH, chapters_name_xpath).text
        # //*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div/ul[7]/div[7]/li/div/div/span

        class_xpath = './div/li/div/span'  # 每个章节的课程
        # finished_xpath = './div[2]/li/div/div/b[2]'  # div[2] 为第二节课
        class_elements = chapter.find_elements(By.XPATH, class_xpath)  # 每个课的element
        class_num = len(class_elements)
        finished_list = []
        for i in range(class_num):  # 第i节课
            is_finished = chapter.find_elements(By.XPATH, f'./div[{i + 1}]/li/div/div/b[2]')
            if is_finished:
                finished_list.append(1)
            else:
                finished_list.append(0)
        flag = True  # 假设该章节全部完成
        n = 0
        for i in range(class_num):
            if finished_list[i] == 0:
                flag = False  # 未完成
                n = i
                print(class_elements[n].text)
                break
        t = chapter.find_elements(By.XPATH, f'div[{n + 1}]/li/div/div/span')[0].text
        if not flag:  # 有未完成的
            return class_elements[n], t, c, n  # 返回该课
            break
        else:
            c += 1


def speed_run(driver):
    videos_xpath = '//*[@id="vjs_container"]/div[8]'
    video = driver.find_elements(By.XPATH, videos_xpath)[0]
    actions = ActionChains(driver)
    actions.move_to_element(video).perform()
    time.sleep(0.5)
    # //div[@class='speedBox']/span
    spd_box_xpath = '//*[@id="vjs_container"]/div[10]/div[9]/span'
    box = driver.find_elements(By.XPATH, spd_box_xpath)[0]
    actions = ActionChains(driver)
    actions.move_to_element(box).perform()

    spd_xpath = '//*[@id="vjs_container"]/div[10]/div[9]/div/div[1]'
    while True:
        spd_elements = driver.find_elements(By.XPATH, spd_xpath)
        if spd_elements:
            spd = spd_elements[0]
            try:
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, spd_xpath)))
                spd.click()
                break
            except:
                print("Element is not clickable. Trying again...")
        else:
            print("Element not found. Trying again...")
    # while 1:
    #     spd = driver.find_elements(By.XPATH, spd_xpath)[0]
    #     if spd:
    #         spd.click()
    #         break

    run_xpath = '//*[@id="playButton"]'
    run = driver.find_elements(By.XPATH, run_xpath)[0]
    run.click()


def iter_class(driver):
    selected_class, class_tm, selected_chap, order = (
        find_first_cls(get_class(driver)))
    selected_class.click()
    print(class_tm)  # 00:06:11
    time.sleep(2)
    speed_run(driver)
    # while 1:
    #     try:
    #         speed_run(driver)       # 开始播放
    #         break
    #     except:
    #         time.sleep(2)
    return selected_chap, order


def is_finished(present_driver, chap, od):
    """
    不断判断是否完成视频
    :param present_driver:  driver
    :param chap:    选中章节
    :param od:   选中视频
    :return:
    """

    xpath = (f'//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div/'
             f'ul[{chap + 1}]/div[{od + 1}]/li/div/div/b[2]')
    '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div/ul[8]/div[3]/li/div/div/div/div/div/svg'
    elements = present_driver.find_elements(By.XPATH, xpath)
    if elements:
        return True
    else:
        return False


def answer(driver):
    """
    若出现问题, 则回答问题
    :param driver:
    :return:
    """
    tanchuang = '//*[@id="playTopic-dialog"]/div'
    tc = driver.find_elements(By.XPATH, tanchuang)
    if tc:
        option_xpath = '//*[@id="playTopic-dialog"]/div/div[2]/div/div[1]/div/div/div[2]/ul/li'
        options = driver.find_elements(By.XPATH, option_xpath)
        for option in options:
            option.click()
            yes_or_no_xpath = ('//*[@id="playTopic-dialog"]/div/div[2]/div/div[1]/'
                               'div/div/div[2]/p/span[1]/span')
            yes_or_no = driver.find_elements(By.XPATH, yes_or_no_xpath)[0].text
            if yes_or_no == "正确":
                close_xpath = '//*[@id="playTopic-dialog"]/div/div[3]/span/div'
                close = driver.find_elements(By.XPATH, close_xpath)
                close[0].click()
                break
            else:
                continue
        time.sleep(2)
        speed_run(driver)
        # while 1:
        #     try:
        #         speed_run(driver)  # 开始播放
        #         break
        #     except:
        #         time.sleep(2)
    else:
        pass


def exam_code():
    """
    手动做验证码
    :return:
    """
    return False


if __name__ == '__main__':
    # 设置谷歌浏览器驱动路径
    driver_path = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"

    # 创建一个谷歌浏览器实例
    chrome_driver = webdriver.Chrome(executable_path=driver_path)
    chrome_driver.maximize_window()  # 最大化显示
    select_course(chrome_driver)
    selected_chap, order = iter_class(chrome_driver)

    while 1:
        if exam_code():
            input("出现验证码")
        else:
            answer(chrome_driver)
            if is_finished(chrome_driver, selected_chap, order):
                selected_chap, order = iter_class(chrome_driver)
        time.sleep(5)
