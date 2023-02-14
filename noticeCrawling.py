from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# 웹드라이버 실행
driver = webdriver.Chrome('./chromedriver.exe')

# 리스트 정의
link_list = []
regdate_list = []
title_list = []

# 3페이지 반복문 처리
for page_num in range(1, 4):
    # 대상 URL
    target_url = input('입력url을넣어주세요')

    # 페이지 접근
    driver.get(target_url)

    # 'a' 태그 찾기
    links = driver.find_elements(By.XPATH, "//table[@class='pyo']//a")
    detail_dates = driver.find_elements(By.XPATH, "//td[@class='small'][1]")

    # 크롤링 시작
    for i in range(len(links)):
        # link 저장
        link = driver.find_elements(By.XPATH, "//table[@class='pyo']//a")[i]
        link_url = link.get_attribute('href')
        link_list.append(link_url)
        
        # regdate 저장
        regdate = driver.find_elements(By.XPATH, "//td[@class='small'][1]")[i]
        regdate_list.append(regdate.text)

        # 상세페이지로 이동
        link.click()
        time.sleep(3)
        
        # 상세제목 저장
        detail_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td[@class='board_tit']")))
        title_list.append(detail_title.text)
        
        # 뒤로 돌아가기
        driver.back()
        time.sleep(3)
    time.sleep(2)

# 웹드라이버 종료
driver.quit()


dic = {"공고명": title_list, "원본 url": link_list, "등록일": regdate_list}
df = pd.DataFrame(dic)
df.to_csv("filename5.csv", index=False, encoding="utf-8-sig")