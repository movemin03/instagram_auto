from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

##사용자 지정
user = os.getlogin()
download_path = 'C:\\Users\\' + user + '\\Desktop\\result.txt'
target_url = "https://www.instagram.com/p/C6-EuAKtw8j/"
output_path = 'C:\\Users\\' + user + '\\Desktop\\instagram_comments.xlsx'


# Instagram 로그인 페이지로 접근
instagram_main = "https://www.instagram.com/"
driver = webdriver.Chrome()
driver.get(instagram_main)

# 로그인 완료 여부 확인
while True:
    time.sleep(2)
    current_url = driver.current_url
    if "https://www.instagram.com/accounts/onetap" in current_url:
        print("로그인이 완료되었습니다.")
        break
    else:
        print("수동 로그인 대기중")

# 대상 URL로 접근
driver.get(target_url)

print("표적 요소를 로딩합니다 Loading")
# 2번째 자식 div 태그의 id 가져오기
time.sleep(2)
main_div = driver.find_element(By.XPATH, '/html/body/div[2]')
main_div_id = main_div.get_attribute('id')

comment_area_xpath = '//*[@id="' + main_div_id + '"]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]'
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, comment_area_xpath))
)
print("표적 요소를 찾았습니다 OK")
print("댓글을 로딩합니다 Loading")

# 스크롤 내리기
prev_scroll_position = driver.execute_script("return arguments[0].scrollTop;",
                                             driver.find_element(By.XPATH, comment_area_xpath))
while True:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",
                          driver.find_element(By.XPATH, comment_area_xpath))
    time.sleep(1)
    curr_scroll_position = driver.execute_script("return arguments[0].scrollTop;",
                                                 driver.find_element(By.XPATH, comment_area_xpath))

    if curr_scroll_position == prev_scroll_position:
        time.sleep(8)
        curr_scroll_position = driver.execute_script("return arguments[0].scrollTop;",
                                                     driver.find_element(By.XPATH, comment_area_xpath))
        if curr_scroll_position == prev_scroll_position:
            print("8초간 스크롤의 변화를 추적했으나 스크롤 위치의 변동을 탐지하지 못했습니다")
            print("댓글이 모두 로딩된 것으로 간주합니다 OK")
            break
    prev_scroll_position = curr_scroll_position

# HTML 저장
'//*[@id="mount_0_0_5X"]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]'
html_content = driver.find_element(By.XPATH,
                                   '//*[@id="' + main_div_id + '"]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]').get_attribute(
    'innerHTML')

soup = BeautifulSoup(html_content, 'html.parser')
driver.quit()

# 추출된 데이터를 저장할 리스트
insta_id_list = []
time_list = []
comment_list = []
like_list = []
thatthat_list = []

# 최상위 div 태그들을 찾음
top_divs = soup.find_all("div", recursive=False)

# 각 최상위 div 태그들을 반복하여 데이터 추출
for div in top_divs:
    try:
        client_insta_id = div.select_one(
            'div > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div:nth-of-type(1) > span:nth-of-type(1) > span > div > a > div > div > span').text.replace(" ", "")
        client_time = div.select_one(
            'div > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div:nth-of-type(1) > span:nth-of-type(2) > a > time')[
            'datetime'].replace(" ", "")
        client_comment = div.select_one(
            'div > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div:nth-of-type(2) > span').text.replace("         ", "")
        client_like = div.select_one(
            'div > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > span > span').text.replace(" ", "").replace("좋아요", "").replace("개", "")
        if client_like == "" or "답글" in client_like:
            client_like = "0"
        client_thatthat_obj = div.select_one(
            'div:nth-of-type(2) > div > div > span')
        if client_thatthat_obj is None:
            client_thatthat = 0
        else:
            client_thatthat = client_thatthat_obj.text.replace(" ", "").replace("답글", "").replace("개모두보기", "")

        insta_id_list.append(client_insta_id)
        time_list.append(client_time)
        comment_list.append(client_comment)
        like_list.append(int(client_like))
        thatthat_list.append(int(client_thatthat))

    except Exception as e:
        print(e)
        print("없음")
        continue

# 데이터프레임으로 변환
data = {
    "Insta_ID": insta_id_list,
    "Time": time_list,
    "Comment": comment_list,
    "likes": like_list,
    "대댓글수": thatthat_list
}

df = pd.DataFrame(data)
while True:
    try:
        df.to_excel(output_path, index=False)
        print(f"데이터프레임이 {output_path}에 저장되었습니다.")
        break
    except Exception as e:
        print(f"오류 발생: {e}")
        a = input("파일이 열려있다면 닫아주십시오. 프로그램이 파일을 덮어씌우려 합니다. 처리 후 엔터")
        time.sleep(3)

a = input()
