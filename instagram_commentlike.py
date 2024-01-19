import pyautogui
from PIL import Image
from pyautogui import ImageNotFoundException
import time

def find_all_images(image):
    # 이미지 불러오기
    target_image = Image.open(image)

    while True:
        # 스크린샷 찍기
        screenshot = pyautogui.screenshot()

        # 이미지 찾기
        try:
            image_locations = pyautogui.locateAll(target_image, screenshot)
        except ImageNotFoundException as e:
            # 이미지를 찾지 못한 경우 처리할 내용 작성
            print("이미지를 찾을 수 없습니다. 이미지 스크린샷을 다시 찍습니다.")
            continue

        # 이미지의 위치를 리스트에 저장
        locations = []
        for location in image_locations:
            locations.append(location)

        return locations

# 이미지 클릭 함수
def click_images(locations):
    for location in locations:
        # 이미지를 찾았을 경우 클릭하기
        image_center = pyautogui.center(location)
        pyautogui.click(image_center)


print("인스타그램 댓글 좋아요 누르기 프로그램입니다")
print("좋아요를 누를 페이지를 띄워주세요. 좋아요 버튼을 가려서는 안 됩니다")
print("준비가 되었다면 아무 값이나 누르고 엔터!!")
a = input()

# 프로그램 실행
first_loop = True
while True:
    # 첫 번째 루프에서는 pagedown 키를 누르지 않도록 함
    if not first_loop:
        # 스크롤 다운 키 누르기
        try:
            plus_btn_locations = find_all_images("plus_btn.png")
            if plus_btn_locations:
                click_images(plus_btn_locations)
            time.sleep(1)
        except:
            print("플러스 버튼 없음, 페이지 스크롤 다운 합니다")
            pyautogui.press("pagedown")
            time.sleep(1)

    # 이미지 찾기
    try:
        image_locations = find_all_images("target_image.png")
    except:
        print("이미지를 더 이상 찾을 수 없습니다.")
        print("아무값이나 입력하고 엔터 시 종료됩니다")
        a = input()
        break

    # 이미지 클릭 함수 호출
    click_images(image_locations)

    # 첫 번째 루프 종료 후 변수 업데이트
    first_loop = False
