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

This script helps you find and list users who have unfollowed you on Instagram.

### Prerequisites

Before using the script, you need to download your account information from Instagram:

1. Go to Instagram and log in to your account.
2. Navigate to Settings > Accounts Center > Your Information and Permissions > Download Your Information.
3. Submit a request to download your information:
    - Choose the account you want to check for unfollowers.
    - Select the type of information: Followers and Following.
    - Submit the request.
4. You will receive a download link within approximately 10 minutes. Go back to the same menu to find the download button.
5. There is no need to extract the zip file. Just provide the path to the downloaded zip file.

### Installation

1. Clone this repository:

    ```sh
    git clone https://github.com/movemin03/instagram_auto.git
    cd instagram_auto
    ```

2. Install the required Python packages:

    ```sh
    pip install pillow, pyautogui, beautifulsoup4
    ```

### Usage

1. Provide the path to the downloaded zip file when prompted by the script:

    ```sh
    python instagram_find_unfollower.py
    ```

2. The script will save the list of unfollowers to `desktop/unfollowers.txt`.

### Packaging with PyInstaller

You can create an executable file using PyInstaller:

    ```sh
    pyinstaller instagram_find_unfollower.py --onefile --hidden-import os --hidden-import zipfile --hidden-import shutil --hidden-import json --hidden-import bs4
    ```

### Requirements

- Python 3.x
- `pillow`
- `pyautogui`
- `beautifulsoup4`
- Standard Python libraries: `os`, `zipfile`, `shutil`, `json`
