from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import os
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import subprocess
import random
from datetime import datetime
import requests
import psutil
from collections import deque

def find_process_by_name(name):
    """이름으로 프로세스를 찾습니다."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == name:
            return proc
    return None


def terminate_process(process):
    """프로세스를 종료하려고 시도하고, 프로세스가 종료될 때까지 대기합니다."""
    while process.is_running():
        print(f"프로세스 {process.name()}를 종료하는 중입니다...")
        process.kill()
        time.sleep(1)  # 1초 대기 후 다시 확인


def kill_process():
    process_name = "chrome.exe"  # Google Chrome의 실제 프로세스 이름
    chrome_process = find_process_by_name(process_name)

    if chrome_process:
        print("크롬 프로그램을 종료해야 본 프로그램을 사용할 수 있습니다. 크롬을 종료하시겠습니까? (y/n)")
        user_input = input().strip().lower()
        if user_input == 'y':
            while chrome_process is not None:
                try:
                    chrome_process = find_process_by_name(process_name)
                    terminate_process(chrome_process)
                    print(chrome_process)
                    try:
                        chrome_process.kill()
                    except:
                        pass
                except:
                    continue
        else:
            print("본 프로그램을 종료합니다.")
            exit()
    else:
        print("크롬이 실행 중이지 않습니다.")

kill_process()

##사용자 지정
user = os.getlogin()
ver = "2024-07-02"
print("ver:" + ver)
print("인스타그램 게시물 댓글 추출 프로그램입니다")
print("추적하고자 하는 인스타그램 게시물의 링크를 넣어주세요")
print("예시: https://www.instagram.com/p/C6-EuAKtw8j/")
target_url = input("링크: ")


# Instagram 로그인 페이지로 접근
def launch_chrome_with_debugging_port(port):
    subprocess.Popen(
        rf'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port={port} --user-data-dir="C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data"'
    )

def create_webdriver_with_port(port):
    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0")
    driver = webdriver.Chrome(options=options)
    return driver

def get_chrome_version(port):
    try:
        response = requests.get(f'http://127.0.0.1:{port}/json/version')
        version_info = response.json()
        chrome_version = version_info['Browser']
        return chrome_version
    except Exception as e:
        print(f"크롬 버전을 가져오는 중 오류 발생: {e}")
        return None


def load_driver():
    max_attempts = 3
    attempt = 0
    port = None

    while attempt < max_attempts:
        port = random.randint(9200, 9300)
        launch_chrome_with_debugging_port(port)
        time.sleep(2)
        print("포트번호 " + str(port) + "으로 시도합니다")

        try:
            driver = create_webdriver_with_port(port)
            driver.set_page_load_timeout(10)
            chrome_version = get_chrome_version(port)
            if chrome_version:
                print(f"현재 실행 중인 크롬 버전: {chrome_version}")
            else:
                print("크롬 버전을 확인할 수 없습니다.")
            print("크롬 드라이버가 성공적으로 실행되었습니다!")
            return driver, port
        except WebDriverException as e:
            print(f"{attempt + 1}번째 시도 실패: {e}")
            attempt += 1
            time.sleep(2)

    user_input = input("3번 시도했으나 응답이 없습니다. 다시 시도해볼까요? (y/n): ")
    if user_input.lower() == 'y':
        return load_driver()
    else:
        print("프로그램을 종료합니다.")
        return None, None


def main():
    print("이 프로그램을 실행할 때는 다른 크롬 창이 띄워져 있으면 안 됩니다!")
    driver, port = load_driver()

    if not driver:
        exit()

    user_input = input("크롬 사용자 선택 창이 있다면 처리하고, 없더라도 y를 입력하세요: ")
    if user_input.lower() == 'y':
        print("크롬 사용자 선택 창이 처리됐다고 응답하셨으므로 인스타그램에 접속합니다.")
    else:
        print("크롬 사용자 선택을 하지 않으면 프로그램이 창을 인식할 수 없습니다. 프로그램을 종료합니다.")
        driver.quit()
        exit()

    # 성공했던 포트번호로 드라이버를 재정의합니다.
    try:
        driver = create_webdriver_with_port(port)
        print("성공했던 포트번호 " + str(port) + "으로 접속합니다")
        driver.set_page_load_timeout(10)
        driver.get("https://www.instagram.com/")
    except WebDriverException as e:
        print(f"페이지를 열 수 없습니다: {e}")
        driver.quit()

    print("\n인스타그램 정책에 따라 로그인이 필요합니다. 로그인해주세요")
    while True:
        a = input("로그인이 완료되었다면 y 입력:")
        if a == "y":
            break

    # 대상 URL로 접근
    driver.get(target_url)

    print("표적 요소를 로딩합니다 Loading")
    # 2번째 자식 div 태그의 id 가져오기
    time.sleep(2)
    main_div = driver.find_element(By.XPATH, '/html/body/div[2]')
    main_div_id = main_div.get_attribute('id')
    print(main_div_id)

    try:
        comment_area_xpath = '//*[@id="' + main_div_id + '"]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]'
    except:
        print("댓글 영역을 찾을 수 없습니다. 인스타그램에서 경로를 변경했을 수 있습니다")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, comment_area_xpath))
    )
    print("표적 요소를 찾았습니다 OK")
    print("댓글을 로딩합니다 Loading")

    def click_all_see_more(driver, comment_area_xpath):
        # 원하는 영역을 찾기 위해 WebDriverWait을 사용하여 요소를 대기
        comment_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, comment_area_xpath))
        )

        # "모두 보기" 텍스트가 포함된 모든 요소를 찾기
        see_more_elements = comment_area.find_elements(By.XPATH, ".//*[contains(text(), '모두 보기')]")
        print("우회를 위해 0.2~1.5초 범위 내에서 대댓보기 버튼을 랜덤하게 클릭합니다")

        for element in see_more_elements:
            # 클릭 전에 랜덤하게 지연 시간을 설정
            delay = random.uniform(0.2, 1.5)
            time.sleep(delay)

            # 요소가 클릭 가능한지 확인한 후 클릭
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ".//*[contains(text(), '모두 보기')]"))
                )
                element.click()
            except:
                pass

    # 스크롤 내리기
    prev_scroll_position = driver.execute_script("return arguments[0].scrollTop;",
                                                 driver.find_element(By.XPATH, comment_area_xpath))
    while True:
        click_all_see_more(driver, comment_area_xpath)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",
                              driver.find_element(By.XPATH, comment_area_xpath))
        time.sleep(1)
        curr_scroll_position = driver.execute_script("return arguments[0].scrollTop;",
                                                     driver.find_element(By.XPATH, comment_area_xpath))

        if curr_scroll_position == prev_scroll_position:
            print("3초간 스크롤의 변화를 추가로 추적합니다")
            time.sleep(3)
            curr_scroll_position = driver.execute_script("return arguments[0].scrollTop;",
                                                         driver.find_element(By.XPATH, comment_area_xpath))
            if curr_scroll_position == prev_scroll_position:
                print("8초간 스크롤의 변화를 추적했으나 스크롤 위치의 변동을 탐지하지 못했습니다")
                a = input("추가로 탐지할 것이 남아있다면 y 아니라면 n 을 입력")
                if a == 'n':
                    print("댓글이 모두 로딩된 것으로 간주합니다 OK")
                    break
                else:
                    continue
        prev_scroll_position = curr_scroll_position

    # HTML 저장
    html_content = driver.find_element(By.XPATH,
                                       '//*[@id="' + main_div_id + '"]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[2]/div/div[2]').get_attribute(
        'innerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    driver.quit()

    ## 추출된 데이터를 저장할 리스트
    insta_id_list = deque()
    time_list = deque()
    comment_list = deque()
    like_list = deque()
    thatthat_list = deque()

    # 최상위 div 태그들을 찾음
    top_divs = soup.find_all("div", recursive=False)

    # 각 최상위 div 태그들을 반복하여 데이터 추출
    for div in top_divs:
        try:
            n = 0
            while True:

                try:
                    n += 1
                    print(str(n))
                    # Insta ID
                    client_insta_id = div.select_one(
                        f'div:nth-child({n}) > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > div:nth-child(1) > span:nth-child(1) > span > div > a > div > div > span'
                    ).text.replace(" ", "")
                    print(client_insta_id)

                    # 시간
                    client_time = div.select_one(
                        f'div:nth-child({n}) > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > div:nth-child(1) > span:nth-child(2) > a > time'
                    )['datetime'].replace(" ", "")

                    # 댓글
                    client_comment = div.select_one(
                        f'div:nth-child({n}) > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > div:nth-child(2) > span'
                    ).text.replace(" ", "")

                    # 좋아요
                    client_like = div.select_one(
                        f'div:nth-child({n}) > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > span > span'
                    ).text.replace(" ", "").replace("좋아요", "").replace("개", "")
                    if (client_like == "") or ("답글달기" in client_like):
                        client_like = "0"

                    insta_id_list.append(client_insta_id)
                    time_list.append(client_time)
                    comment_list.append(client_comment)
                    like_list.append(client_like)

                    # 대댓글 처리
                    client_thatthat_obj = div.select_one(f'div:nth-child({n}) > div:nth-child(2) > ul')
                    if client_thatthat_obj is None:
                        client_thatthat = "0"
                        thatthat_list.append(client_thatthat)
                    else:
                        m = 0
                        while True:
                            try:
                                #'div:nth-child({n}) > div:nth-child(2) > ul > div > '
                                m += 1
                                # 대댓글 ID
                                client_thatthat_id = div.select_one(
                                    f'div:nth-child({n}) > div:nth-child(2) > ul > div:nth-child({m}) > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > div:nth-child(1) > span:nth-child(1) > span > div > a > div > div > span'
                                ).text.replace(" ", "")
                                print("대댓", client_thatthat_id)

                                # 대댓글 시간
                                client_thatthat_time = div.select_one(
                                    f'div:nth-child({n}) > div:nth-child(2) > ul > div:nth-child({m}) > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > div:nth-child(1) > span:nth-child(2) > a > time'
                                )['datetime'].replace(" ", "")

                                # 대댓글 내용
                                client_thatthat_comment = div.select_one(
                                    f'div:nth-child({n}) > div:nth-child(2) > ul > div:nth-child({m}) > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > div:nth-child(2) > span'
                                ).text.replace(" ", "")
                                #//*[@id="mount_0_0_YG"]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div/div[2]/div/div[4]/div[2]/ul/div[1]/div/div[2]/div[1]/div[1]/div/div[2]/span
                                # 대댓글 좋아요
                                client_thatthat_like = div.select_one(
                                    f'div:nth-child({n}) > div:nth-child(2) > ul > div:nth-child({m}) > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > span > span'
                                ).text.replace(" ", "").replace("좋아요", "").replace("개", "")
                                #//*[@id="mount_0_0_YG"]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div/div[2]/div/div[4]/div[2]/ul/div[1]/div/div[2]/div[1]/div[2]/div[1]/span/span

                                if (client_thatthat_like == "") or ("답글달기" in client_thatthat_like):
                                    client_thatthat_like = "0"

                                insta_id_list.append(client_thatthat_id)
                                time_list.append(client_thatthat_time)
                                comment_list.append(client_thatthat_comment)
                                like_list.append(client_thatthat_like)

                            except AttributeError:
                                break  # 유효한 값을 찾지 못하면 대댓글 반복문 종료
                            except Exception as e:
                                print(f"예상치 못한 오류 발생: {e}")
                                break  # 예상치 못한 오류 발생 시 대댓글 반복문 종료

                        client_thatthat = m - 1
                        thatthat_list.append(client_thatthat)
                        for _ in range(m - 1):
                            client_thatthat_thatthat = "대댓글"
                            thatthat_list.append(client_thatthat_thatthat)

                except AttributeError:
                    break  # 유효한 값을 찾지 못하면 메인 댓글 반복문 종료
                except Exception as e:
                    print(f"예상치 못한 오류 발생: {e}")
                    break  # 예상치 못한 오류 발생 시 메인 댓글 반복문 종료

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
    yymmdd_hhmm = datetime.now().strftime("%y%m%d_%H%M")
    base_output_path = f'C:\\Users\\{user}\\Desktop\\instagram_comments_{yymmdd_hhmm}.xlsx'
    # 파일 존재 여부 확인 및 중복 시 숫자 추가
    counter = 1
    output_path = f'C:\\Users\\{user}\\Desktop\\instagram_comments.xlsx'

    while os.path.exists(output_path):
        output_path = f'C:\\Users\\{user}\\Desktop\\instagram_comments_{yymmdd_hhmm} ({counter}).xlsx'
        counter += 1

    output_path = base_output_path
    df.to_excel(output_path, index=False)
    # 데이터프레임 출력
    print(f"데이터프레임이 {output_path}에 저장되었습니다.")
    a = input()

if __name__ == "__main__":
    main()
