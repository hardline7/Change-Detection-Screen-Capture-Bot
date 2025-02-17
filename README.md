# 변화감지 캡처봇 (Screen Change Monitor)

## 프로젝트 개요

변화감지 캡처봇은 사용자가 지정한 화면 영역의 변화를 실시간으로 모니터링하고, 변화가 감지되면 자동으로 스크린샷을 캡처하여 저장하는 Python 기반의 데스크톱 애플리케이션입니다. 추가적으로 Telegram 봇 기능을 통해 원격으로 알림을 받을 수 있습니다.

## 주요 기능

1. **사용자 정의 화면 영역 모니터링**
   - 사용자가 직접 모니터링할 화면 영역을 드래그하여 선택 가능

2. **실시간 화면 변화 감지**
   - 설정된 주기로 화면을 스캔하여 변화 감지

3. **자동 스크린샷 캡처 및 저장**
   - 변화 감지 시 자동으로 스크린샷을 캡처하고 지정된 폴더에 저장

4. **조절 가능한 감도 설정**
   - 픽셀 변화량 임계값을 슬라이더로 조절 가능

5. **Telegram 봇 연동**
   - 변화 감지 시 Telegram을 통해 알림 메시지 및 스크린샷 전송
   - 주기적인 작동 상태 보고 기능

6. **사용자 친화적 GUI**
   - PyQt5 기반의 직관적인 그래픽 사용자 인터페이스

7. **설정 저장 및 불러오기**
   - 프로그램 설정을 JSON 파일로 저장하고 자동으로 불러오기

8. **에러 처리 및 로깅**
   - 예외 상황에 대한 처리 및 사용자에게 알림

9. **윈도우만 지원**
   

## 설치 방법

### 방법 1: Python 환경에서 직접 실행

1. Python 3.6 이상 버전 설치 (https://www.python.org/downloads/)

2. 프로젝트 코드 다운로드 또는 클론
   ```
   git clone https://github.com/hardline7/Change-Detection-Screen-Capture-Bot.git   
   cd Change-Detection-Screen-Capture-Bot
   ```

3. 가상 환경 생성 및 활성화 (선택사항이지만 권장)
   ```
   python -m venv venv
   source venv/bin/activate  # Windows의 경우: venv\Scripts\activate
   ```

4. 필요한 라이브러리 설치
   ```
   pip install -r requirements.txt
   ```

5. 프로그램 실행
   ```
   python screen_monitor.py
   ```

### 방법 2: PyInstaller를 이용한 실행 파일 생성

1. PyInstaller 설치
   ```
   pip install pyinstaller
   ```

2. 실행 파일 생성
   ```
   pyinstaller --onefile --windowed --hidden-import=PyQt5.QtWidgets --hidden-import=PyQt5.QtCore --hidden-import=PyQt5.QtGui --hidden-import=PIL.Image --hidden-import=PIL.ImageChops --hidden-import=pyautogui --hidden-import=requests --hidden-import=json --hidden-import=socket --hidden-import=datetime --hidden-import=time --hidden-import=os --hidden-import=sys --hidden-import=traceback screen_monitor.py
   ```

3. `dist` 폴더 내의 실행 파일을 실행

## 상세 사용 방법

1. **프로그램 시작**
   - 설치 후 `screen_monitor.py`를 실행하거나, PyInstaller로 생성된 실행 파일을 더블클릭합니다.

2. **저장 경로 설정**
   - '저장 경로 선택' 버튼을 클릭하여 스크린샷이 저장될 폴더를 지정합니다.

3. **모니터링 영역 선택**
   - '감지 영역 선택' 버튼을 클릭합니다.
   - 전체 화면이 반투명한 검은색으로 덮이면, 모니터링하고자 하는 영역을 마우스로 드래그하여 선택합니다.

4. **감도 조절**
   - '픽셀 변화량 임계값' 슬라이더를 조절하여 감지 감도를 설정합니다.
   - 값이 낮을수록 작은 변화에도 반응하며, 높을수록 큰 변화에만 반응합니다.

5. **Telegram 설정 (선택사항)**
   - 'Telegram 사용' 체크박스를 선택합니다.
   - 봇 토큰과 채팅 ID를 입력합니다. (자세한 설정 방법은 아래 참조)
   - '저장' 버튼을 클릭하여 설정을 저장합니다.

6. **모니터링 시작**
   - '모니터링 시작' 버튼을 클릭하여 감지를 시작합니다.
   - 상태 표시줄에 현재 상태가 표시됩니다.

7. **모니터링 중지**
   - '모니터링 중지' 버튼을 클릭하여 감지를 중지합니다.

## Telegram 봇 상세 설정 방법

텔레그램 봇 설정 상세 가이드
1. 봇 파더(BotFather)를 통한 봇 생성
텔레그램 앱을 엽니다.
검색창에 "@BotFather"를 입력하고 검색합니다.
결과 목록에서 파란 확인 표시가 있는 "BotFather"를 선택합니다.
"시작" 또는 "/start" 버튼을 클릭하여 BotFather와의 대화를 시작합니다.
"/newbot" 명령어를 입력하여 새 봇 생성 프로세스를 시작합니다.
봇의 이름을 입력하라는 메시지가 표시됩니다. 원하는 이름을 입력하세요 (예: "내 스크린 모니터 봇").
봇의 사용자명을 입력하라는 메시지가 표시됩니다. 이는 고유해야 하며 '_bot'으로 끝나야 합니다 (예: "my_screen_monitor_bot").
성공적으로 봇이 생성되면, BotFather가 봇 토큰을 제공합니다. 이 토큰을 안전한 곳에 저장하세요. 이는 나중에 프로그램에서 사용됩니다.

2. 채팅 ID 확인
텔레그램 앱에서 검색창에 "@userinfobot"을 입력하고 검색합니다.
결과 목록에서 "UserInfoBot"을 선택합니다.
"시작" 또는 "/start" 버튼을 클릭하여 UserInfoBot과의 대화를 시작합니다.
봇이 자동으로 당신의 정보를 표시할 것입니다. 여기서 "Id" 항목의 숫자가 바로 당신의 채팅 ID입니다.
이 채팅 ID를 메모해두세요. 이는 나중에 프로그램에서 사용됩니다.

3. 생성한 봇과 대화방 열기
텔레그램 앱의 검색창에 앞서 생성한 봇의 사용자명을 입력합니다 (예: "@my_screen_monitor_bot").
검색 결과에서 해당 봇을 선택합니다.
"시작" 또는 "/start" 버튼을 클릭하여 봇과의 대화를 시작합니다.
이제 봇과의 개인 대화방이 열렸습니다. 이 대화방에서 봇이 보내는 메시지와 스크린샷을 받게 될 것입니다.

4. 프로그램에 봇 정보 입력
변화감지 캡처봇 프로그램을 실행합니다.
'Telegram 사용' 체크박스를 선택합니다.
'봇 토큰' 필드에 BotFather에게서 받은 봇 토큰을 입력합니다.
'챗 ID' 필드에 UserInfoBot에게서 확인한 채팅 ID를 입력합니다.
'저장' 버튼을 클릭하여 설정을 저장합니다.

주의사항
봇 토큰은 비밀번호와 같이 중요한 정보입니다. 절대로 다른 사람과 공유하지 마세요.
채팅 ID도 개인 정보이므로 주의해서 다루세요.
봇 설정에 문제가 있다면, BotFather에게 "/mybots" 명령어를 보내 기존 봇의 설정을 확인하거나 수정할 수 있습니다.

## 주의사항 및 팁

- 이 프로그램은 개인적인 용도로 제작되었습니다. 타인의 동의 없이 사용하거나 프라이버시를 침해하지 않도록 주의하세요.
- 높은 빈도로 화면을 캡처하면 시스템 성능에 영향을 줄 수 있습니다. 필요한 경우에만 사용하세요.
- Telegram 알림을 사용할 경우, 봇 토큰과 채팅 ID를 안전하게 보관하세요.
- 프로그램 설정은 자동으로 저장되며, 다음 실행 시 불러와집니다.
- 에러 발생 시 화면에 표시되는 메시지를 확인하고, 필요한 경우 개발자에게 보고해 주세요.

## 문제 해결

- **프로그램이 실행되지 않는 경우**
  - Python이 올바르게 설치되어 있는지 확인하세요.
  - 필요한 모든 라이브러리가 설치되어 있는지 확인하세요.

- **화면 캡처가 되지 않는 경우**
  - 선택한 영역이 올바른지 확인하세요.
  - 픽셀 변화량 임계값을 낮추어 보세요.

- **Telegram 알림이 오지 않는 경우**
  - 봇 토큰과 채팅 ID가 올바른지 확인하세요.
  - 인터넷 연결을 확인하세요.

## 향후 개발 계획

- 다중 영역 모니터링 기능
- 사용자 정의 알림 설정
- 이미지 분석을 통한 더 정교한 변화 감지
- 웹 인터페이스 추가

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 기여하기

버그 리포트, 기능 제안 또는 풀 리퀘스트는 언제나 환영합니다. 프로젝트에 기여하고 싶으시다면 이슈를 열어주세요.

1. 프로젝트를 포크합니다.
2. 새 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`).
3. 변경사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`).
4. 브랜치에 푸시합니다 (`git push origin feature/AmazingFeature`).
5. 풀 리퀘스트를 생성합니다.

## 연락처

제작자: 충
이메일: hardline7@gmail.com.com

## 감사의 말

이 프로젝트는 다음과 같은 오픈 소스 프로젝트들을 사용하여 제작되었습니다:

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- [Pillow](https://python-pillow.org/)
- [pyautogui](https://pyautogui.readthedocs.io/)
- [requests](https://requests.readthedocs.io/)

이 프로젝트들의 개발자들에게 감사드립니다.

---

변화감지 캡처봇을 사용해 주셔서 감사합니다. 화면 모니터링 및 자동 캡처 기능을 유용하게 사용하시기 바랍니다!
