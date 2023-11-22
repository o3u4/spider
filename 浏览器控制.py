from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

# 获取Chrome浏览器的WebDriver对象
driver = Chrome()

# 打开百度首页
driver.get('https://piaofang.maoyan.com/rankings/year')

ranks_list = driver.find_elements(By.XPATH, '//*[@id="ranks-list"]/ul')
name = []
time = []
piao_fang = []
for rank in ranks_list:
    nm = rank.find_element(By.XPATH, './li[2]/p[1]').text
    name.append(nm)
    tm = rank.find_element(By.XPATH, './li[2]/p[2]').text
    time.append(tm)
    pf = rank.find_element(By.XPATH, './li[3]').text
    piao_fang.append(pf)
    break               # 测试
print(name)
print(time)
print(piao_fang)
