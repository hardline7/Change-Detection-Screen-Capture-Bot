# 변화감지 캡처봇 v5 기준 (Change Detection Screen Capture Bot_v5)

변화감지 캡처봇 v0.0031
소개
변화감지 캡처봇은 사용자가 지정한 화면 영역에서 변화가 감지되면 스크린샷을 저장하고, 필요에 따라 Telegram을 통해 알림과 스크린샷을 전송하는 프로그램입니다. 이 도구를 통해 중요한 화면의 변화를 실시간으로 모니터링하고 기록할 수 있습니다.

주요 기능
화면 영역 선택: 마우스를 이용하여 모니터링할 화면 영역을 직접 선택할 수 있습니다.
저장 경로 지정: 스크린샷이 저장될 폴더를 선택할 수 있습니다.
픽셀 변화량 임계값 설정: 변화로 인식할 픽셀 변화량의 임계값을 조절할 수 있습니다.
Telegram 알림: 옵션으로 Telegram 봇을 통해 변화 감지 시 알림과 스크린샷을 전송할 수 있습니다.
자동 스크린샷 저장: 변화가 감지되면 자동으로 스크린샷을 지정된 폴더에 저장합니다.
상태 알림: 프로그램이 정상적으로 동작 중인지 일정 시간마다 Telegram을 통해 알림을 받을 수 있습니다.
요구 사항
운영 체제: Windows 7 이상
Python 버전: Python 3.6 이상
필수 라이브러리:
PyQt5
Pillow (PIL)
pyautogui
requests
설치 방법
Python 설치: Python 3.6 이상 버전을 설치합니다. Python 공식 웹사이트에서 다운로드 가능합니다.

필수 라이브러리 설치: 다음 명령어를 통해 필요한 라이브러리를 설치합니다.

bash
코드 복사
pip install PyQt5 Pillow pyautogui requests
참고: pyautogui를 사용하기 위해 추가로 pygetwindow, pyscreeze, PyTweening 등의 종속 라이브러리가 자동으로 설치됩니다.

소스 코드 다운로드: 이 저장소를 클론하거나 ZIP 파일로 다운로드하여 압축을 풉니다.

bash
코드 복사
git clone https://github.com/yourusername/your-repo-name.git
사용법
프로그램 실행:

bash
코드 복사
python your_script.py
또는 Windows 환경에서는 더블 클릭하여 실행할 수 있습니다.

사용법 안내 확인: 프로그램 실행 후 나타나는 안내 메시지를 읽고 확인 버튼을 클릭합니다.

저장 경로 선택:

"저장 경로 선택" 버튼을 클릭하여 스크린샷이 저장될 폴더를 선택합니다.
감지 영역 선택:

"감지 영역 선택" 버튼을 클릭합니다.
화면이 어두워지고 마우스 커서로 감지할 영역을 드래그하여 선택합니다.
픽셀 변화량 임계값 설정:

슬라이더를 이용하여 변화로 인식할 픽셀 변화량의 임계값을 조절합니다.
기본값은 100이며, 값이 낮을수록 작은 변화에도 반응합니다.
Telegram 설정 (선택 사항):

"Telegram 사용" 체크박스를 선택합니다.
봇 토큰과 챗 ID를 입력합니다.
봇 토큰: BotFather를 통해 생성한 봇의 토큰을 입력합니다.
챗 ID: @username_to_id_bot 등을 이용하여 자신의 챗 ID를 확인합니다.
"저장" 버튼을 클릭하여 Telegram 설정을 저장합니다.
모니터링 시작:

모든 설정이 완료되면 "모니터링 시작" 버튼이 활성화됩니다.
버튼을 클릭하면 모니터링이 시작되며, 상태 라벨에 "모니터링 중..."이라고 표시됩니다.
모니터링 중지:

모니터링을 중지하려면 "모니터링 중지" 버튼을 클릭합니다.
PyInstaller를 이용한 실행 파일 생성
프로그램을 실행 파일로 만들어 Python이 설치되지 않은 환경에서도 실행할 수 있습니다.

PyInstaller 설치:

bash
코드 복사
pip install pyinstaller
실행 파일 생성:

다음 명령어를 사용하여 실행 파일을 생성합니다.

bash
코드 복사
pyinstaller --onefile --windowed \
    --hidden-import=PyQt5.QtWidgets \
    --hidden-import=PyQt5.QtCore \
    --hidden-import=PyQt5.QtGui \
    --hidden-import=PIL.Image \
    --hidden-import=PIL.ImageChops \
    --hidden-import=pyautogui \
    --hidden-import=requests \
    --hidden-import=json \
    --hidden-import=socket \
    --hidden-import=datetime \
    your_script.py
참고: your_script.py를 실제 파이썬 스크립트 파일명으로 변경하세요.

실행 파일 위치:

명령어 실행 후 생성된 dist 폴더 내에 실행 파일이 생성됩니다.
주의 사항
권한 문제: 프로그램이 스크린샷을 캡처하고 파일을 저장하기 위해서는 충분한 시스템 권한이 필요합니다. 관리자 권한으로 실행하거나 보안 소프트웨어의 예외 처리 설정이 필요할 수 있습니다.
안티바이러스 소프트웨어: 일부 안티바이러스 프로그램에서 오탐지할 수 있으므로 신뢰할 수 있는 프로그램으로 설정해주시기 바랍니다.
해상도 및 디스플레이 설정: 멀티 모니터 환경이나 디스플레이 배율이 변경된 경우 예상치 못한 동작이 발생할 수 있습니다.
라이선스
MIT 라이선스에 따라 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

기여
버그 신고, 기능 개선 제안 또는 기여는 언제나 환영합니다! 이슈를 등록하거나 풀 리퀘스트를 보내주세요.

문의
프로그램 관련 문의는 hardline7@gmail.com으로 연락주시기 바랍니다.
