# 변화감지 캡처봇 (Change Detection Screen Capture Bot)

이 프로젝트는 지정된 모니터 화면의 영역에서 변화를 감지하여 스크린샷을 찍고, 이를 텔레그램 봇을 통해 자동으로 전송하는 프로그램입니다.

This project is a screen capture bot that detects changes in a specified area of the monitor screen, takes a screenshot, and automatically sends it via a Telegram bot.

## 기능 (Features)

- 지정된 모니터 영역에서 변화 감지
- 스크린샷 자동 저장 및 텔레그램 전송
- 텔레그램 봇 토큰 및 챗 ID 설정
- 감지 영역 및 체크 딜레이 설정
- 스크린샷 저장 경로 선택 가능
- 시간 간격마다 텔레그램 상태 메시지 전송
- 변화 감지된 스크린샷 텔레그램 메시지 전송

## 설치 방법 (Installation)

1. 이 레포지토리를 클론합니다:

    ```bash
    git clone https://github.com/your_username/screen_capture_bot.git
    ```

2. 필요한 라이브러리를 설치합니다:

    ```bash
    pip install -r requirements.txt
    ```

3. `PyQt5`, `Pillow`, `pyautogui`, `python-telegram-bot` 등의 패키지가 설치되어야 합니다.

4. Python 3.7 이상이 필요합니다.

## 사용법 (Usage)

1. 프로그램을 실행하면, 설정 창이 나타납니다.
2. 텔레그램 봇 토큰과 챗 ID를 입력하고, 저장 경로를 선택합니다.
3. 모니터링할 영역을 마우스로 드래그하여 선택합니다.
4. 체크 딜레이를 조절한 후, "모니터링 시작" 버튼을 눌러 감지를 시작합니다.
5. 화면 변화가 감지되면 자동으로 스크린샷이 저장되고, 텔레그램 메시지로 전송됩니다.

### 텔레그램 봇 설정

1. [텔레그램 봇파더](https://t.me/BotFather)를 통해 새 봇을 생성하고 토큰을 발급받습니다.
2. 챗 ID는 봇과의 대화에서 `/start` 명령어를 실행하여 확인할 수 있습니다.

## 주요 라이브러리 (Key Libraries)

- PyQt5: GUI 인터페이스
- Pillow: 이미지 처리
- pyautogui: 화면 캡처
- python-telegram-bot: 텔레그램 API 통신

## 기여 (Contributing)

기여는 언제나 환영합니다. Pull Request를 보내주시거나 이슈를 등록해주세요.

---

# Change Detection Screen Capture Bot

This project detects changes in a specified area of the monitor screen, captures screenshots, and automatically sends them via a Telegram bot.

## Features

- Detect changes in a specified monitor area
- Automatically save screenshots and send them via Telegram
- Configure Telegram bot token and chat ID
- Set detection area and check delay
- Select a directory for saving screenshots
- Send status messages via Telegram at regular intervals

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your_username/screen_capture_bot.git
    ```

2. Install required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have installed `PyQt5`, `Pillow`, `pyautogui`, `python-telegram-bot`, and other dependencies.

4. Requires Python 3.7 or later.

## Usage

1. Run the program and the settings window will appear.
2. Enter your Telegram bot token and chat ID, then select a save directory.
3. Drag and select the monitoring area on the screen.
4. Adjust the check delay and click "Start Monitoring" to begin.
5. Once a change is detected, a screenshot is automatically saved and sent via Telegram.

### Telegram Bot Setup

1. Create a new bot using the [Telegram BotFather](https://t.me/BotFather) and get the token.
2. The chat ID can be found by starting a conversation with the bot and running the `/start` command.

## Key Libraries

- PyQt5: GUI Interface
- Pillow: Image Processing
- pyautogui: Screen Capture
- python-telegram-bot: Telegram API Communication

## Contributing

Contributions are always welcome. Please submit a Pull Request or open an issue.

