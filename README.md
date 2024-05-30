# Instagram Automation Scripts

This repository contains two Python scripts for automating interactions with Instagram:

1. `instagram_commentlike.py`
2. `instagram_find_unfollower.py`

## instagram_commentlike.py

This script automatically finds and clicks the like button on Instagram posts. It relies on image recognition to locate the like button and the "view more comments" button on the screen.

### Prerequisites

Make sure you have the following image files in the same directory as `instagram_commentlike.py`:

- `target_image.png`: An image of the Instagram like button.
- `plus_btn.png`: An image of the "view more comments" button.

### Installation

1. Clone this repository:

    ```sh
    git clone https://github.com/movemin03/instagram_auto.git
    cd instagram_auto
    ```

2. Install the required Python packages:

    ```sh
    pip install pillow, pyautogui
    ```

### Usage

1. Ensure you have the necessary image files (`target_image.png` and `plus_btn.png`) in the same directory as `instagram_commentlike.py`.

2. Run the script and provide the link to the Instagram post you want to automate likes for:

    ```sh
    python instagram_commentlike.py
    ```

### Packaging with PyInstaller

You can create an executable file using PyInstaller:

    ```sh
    pyinstaller instagram_commentlike.py --onefile --hidden-import pillow --hidden-import pyautogui
    ```

## instagram_find_unfollower.py

Details for this script will be provided soon.

### Requirements

- Python 3.x
- `pillow`
- `pyautogui`

# Find your Unfollower 언팔로워 찾기

Before Use this program, pleas download your date from official instagram

- how to download data:
open instagram - settings and privacy - Accounts Center - Your information and permissions - download your information - 
requests a download - select account - Select types... - select followers and follong - submit
Refresh your menu. Normally, you can download data within 10 min.
***You don't have to extract your file. Just input zip file which you download from Instagram***

사용 전, 공식 인스타그램 접속하여 정보를 다운로드 받아주세요

- 방법은 다음과 같습니다:
인스타 접속 - 설정 - 계정센터 - 내 정보 및 권한 - 내 정보 다운로드 - 다운로드 요청 - 
언팔로워 확인할 계정 선택 - 정보 유형 선택 - 팔로워 및 팔로잉 선택- 요청 제출
보통 10분 이내에 다운로드 버튼이 형성되니 다운로드 받아주시길 바랍니다. 나갔다가 해당 메뉴로 다시 들어와보면 생깁니다
***압축을 해제할 필요없습니다. 다운로드 받은 zip 파일 그대로 파일의 경로를 지정해주세요***

We save Unfollowers list to desktop/unfollowers.txt
언팔로우 한 사람들의 리스트를 바탕화면에 unfollowers.txt 이름으로 저장합니다

# instagram_commnet_like
인스타그램 댓글에 좋아요를 달아주는 프로그램입니다.
plus_btn.png 이라는 이름으로 추가 버튼 이미지를 프로그램 실행 위치에 넣어주세요
target_image.png 이라는 이름으로 off 상태의 좋아요 버튼 이미지를 프로그램 실행 위치에 넣어주세요
