# Claude MCP GitHub Starter

Claude가 호출할 원격 MCP 서버의 시작 템플릿입니다.

## 도구
- `server_status`: 서버 응답 확인
- `save_note`: 메모 초안 형식 만들기 (영구 저장 안 함)
- `create_task`: 작업 초안 만들기 (GitHub 이슈를 실제 생성하지 않음)

## 배포
1. GitHub에서 새 저장소를 만들고 이 파일들을 업로드합니다.
2. Render에서 New + → Web Service를 선택하고 GitHub 저장소를 연결합니다.
3. Build command: `pip install -r requirements.txt`
4. Start command: `python server.py`
5. 배포 후 HTTPS 주소를 확인합니다.
6. Claude의 Settings → Connectors → Add custom connector에서 MCP 주소를 입력합니다. 일반적으로 `https://YOUR-SERVICE.onrender.com/mcp` 형태입니다.

## 제한
- GitHub는 코드를 보관하고, Render가 서버를 실행합니다.
- 무료 호스팅은 유휴 시 잠들 수 있습니다.
- 이 템플릿은 영구 메모리나 실제 GitHub 이슈 생성 기능이 없습니다.
- 비밀번호나 GitHub 토큰을 코드에 넣지 마세요.
- ChatGPT Free는 사용자 지정 MCP 서버 직접 연결을 지원하지 않으므로, 이 프로젝트만으로 ChatGPT와 Claude가 자동으로 직접 대화하지는 않습니다.
