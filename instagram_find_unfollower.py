import os
import zipfile
import shutil
import json
from bs4 import BeautifulSoup

def extract_and_move_json_files(zip_path, destination_folder):
    # Zip 파일이 존재하는지 확인함
    if not os.path.isfile(zip_path):
        print(f"{zip_path} does not exist.")
        return None, None

    # 지정된 경로에 폴더가 있는지 확인하고 없으면 생성
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    followers_file = None
    following_file = None

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # zip 파일 내의 'followers_and_following' 폴더를 찾기
        for file_info in zip_ref.infolist():
            # 파일명이 "followers_1.json", "following.json", "followers_1.html", "following.html"인 경우에만 처리
            if file_info.filename == 'followers_and_following/followers_1.json':
                # 원본 zip 파일 내의 전체 경로를 잡고
                source = zip_ref.extract(file_info)
                # 바탕화면으로 복사할 파일명을 설정
                destination = os.path.join(destination_folder, os.path.basename(file_info.filename))
                # 파일 복사
                shutil.move(source, destination)
                followers_file = destination
                print(f"Copied: {file_info.filename} to {destination}")

            if file_info.filename == 'followers_and_following/following.json':
                # 원본 zip 파일 내의 전체 경로를 잡고
                source = zip_ref.extract(file_info)
                # 바탕화면으로 복사할 파일명을 설정
                destination = os.path.join(destination_folder, os.path.basename(file_info.filename))
                # 파일 복사
                shutil.move(source, destination)
                following_file = destination
                print(f"Copied: {file_info.filename} to {destination}")
            if file_info.filename == 'followers_and_following/followers_1.html':
                # 원본 zip 파일 내의 전체 경로를 잡고
                source = zip_ref.extract(file_info)
                # 바탕화면으로 복사할 파일명을 설정
                destination = os.path.join(destination_folder, os.path.basename(file_info.filename))
                # 파일 복사
                shutil.move(source, destination)
                followers_file = destination
                print(f"Copied: {file_info.filename} to {destination}")

            if file_info.filename == 'followers_and_following/following.html':
                # 원본 zip 파일 내의 전체 경로를 잡고
                source = zip_ref.extract(file_info)
                # 바탕화면으로 복사할 파일명을 설정
                destination = os.path.join(destination_folder, os.path.basename(file_info.filename))
                # 파일 복사
                shutil.move(source, destination)
                following_file = destination
                print(f"Copied: {file_info.filename} to {destination}")

    return followers_file, following_file

def compare_json():
    # 파일에서 데이터 로드
    with open(followers_file, "r", encoding="utf-8") as f:
        followers_data = json.load(f)

    with open(following_file, "r", encoding="utf-8") as f:
        following_data = json.load(f)

    # 필요한 데이터 추출
    followers_list = [follower["string_list_data"][0]["value"] for follower in followers_data]
    following_list = [following["string_list_data"][0]["value"] for following in following_data["relationships_following"]]

    # 팔로잉 목록에는 있지만 팔로워 목록에는 없는 값을 추려내기
    global unfollowers
    unfollowers = [user for user in following_list if user not in followers_list]
    # 팔로잉 목록에는 있지만 팔로워 목록에는 없는 값을 추려내기
    global not_followed
    not_followed = [user for user in followers_list if user not in following_list]

def compare_html():
    # 파일에서 데이터 로드
    with open(followers_file, 'r', encoding="utf-8") as f:
        followers_data = f.read()

    with open(following_file, 'r', encoding="utf-8") as f:
        following_data = f.read()

    # 필요한 데이터 추출
    soup = BeautifulSoup(followers_data, 'html.parser')
    followers_list = [element.text for element in soup.select('div._a6-p > * > * > *')]
    soup = BeautifulSoup(following_data, 'html.parser')
    following_list = [element.text for element in soup.select('div._a6-p > * > * > *')]

    # 팔로잉 목록에는 있지만 팔로워 목록에는 없는 값을 추려내기
    global unfollowers
    unfollowers = [user for user in following_list if user not in followers_list]
    # 팔로우 목록에는 있지만 팔로잉 목록에는 없는 값을 추려내기
    global not_followed
    not_followed = [user for user in followers_list if user not in following_list]

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
print("Find your Unfollower")
print("언팔로워 찾기\n")

print("Before Use this program, pleas download your date from official instagram")
print("how to download data:")
print("open instagram - settings and privacy - Accounts Center - Your information and permissions - download your information")
print("- requests a download - select account - Select types... - select followers and following - change data range into All time -  submit ")
print("Refresh your menu. Normally, you can download data within 10 min. ")
print("***You don't have to extract your file. Just input zip file which you download from Instagram\n")

print("사용 전, 공식 인스타그램 접속하여 정보를 다운로드 받아주세요. 방법은 다음과 같습니다.")
print("인스타 접속 - 설정 - 계정센터 - 내 정보 및 권한 - 내 정보 다운로드 - 다운로드 요청")
print("- 언팔로워 확인할 계정 선택 - 정보 유형 선택 - 팔로워 및 팔로잉 선택 - 기간을 전체기간 설정 - 요청 제출")
print("보통 10분 이내에 다운로드 버튼이 형성되니 다운로드 받아주시길 바랍니다. 나갔다가 해당 메뉴로 다시 들어와보면 생깁니다")
print("***압축을 해제할 필요없습니다. 다운로드 받은 zip 파일 그대로 파일의 경로를 지정해주세요***\n")

print("Enter the path to the zip file below")
zip_file_path = input("경로를 넣어주세요: ").replace('"', "")

# 함수를 호출-작업을 실행하고-결과 변수에 저장
followers_file, following_file = extract_and_move_json_files(zip_file_path, desktop)

if followers_file is None or following_file is None:
    print("\nFailed to extract and move JSON/HTML files into Desktop path.")
else:
    print("\nfollowers_file:", followers_file)
    print("following_file:", following_file)
    print("\n분석중입니다. 조금만 기다려주세요")
    if '.html' in followers_file:
        compare_html()
    else:
        if '.json' in followers_file:
            compare_json()
        else:
            print("can't find html or json files. exit program")
            print("비교할 html 이나 json 파일을 발견하지 못했습니다. 프로그램을 종료합니다")
            a = input("아무키나 입력하면 종료")
            exit()

# 결과를 파일로 저장
unfollowers_file = os.path.join(desktop, "unfollowers.txt")
not_followed_file = os.path.join(desktop, "not_followed.txt")

with open(unfollowers_file, "w", encoding="utf-8") as f:
    for user in unfollowers:
        f.write(user + "\n")
with open(not_followed_file, "w", encoding="utf-8") as f:
    for user in not_followed:
        f.write(user + "\n")

print(f"\nWe save list to desktop in txt file")
print(f"바탕화면에 unfollowers.txt 와  not_followed.txt 이름으로 저장했습니다")
a = input("아무키나 입력하면 종료")
