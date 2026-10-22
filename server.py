
import os
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

mcp = FastMCP("Shared Notes MCP", stateless_http=True, json_response=True)

@mcp.tool()
def save_note(title: str, content: str) -> str:
    if not title.strip() or not content.strip():
        return "오류: 제목과 내용을 모두 입력해 주세요."
    return f"메모 초안\n제목: {title.strip()}\n내용:\n{content.strip()}\n\n이 시작 버전은 내용을 영구 저장하지 않습니다."

@mcp.tool()
def create_task(title: str, details: str = "") -> str:
    if not title.strip():
        return "오류: 작업 제목을 입력해 주세요."
    return f"공유 작업 초안\n작업: {title.strip()}\n세부 내용: {details.strip() or '(없음)'}\n\n이 시작 버전은 GitHub 이슈를 실제 생성하지 않습니다."

@mcp.tool()
def server_status() -> str:
    return "MCP 서버가 실행 중입니다."

security = TransportSecuritySettings(
    allowed_hosts=[
        "claude-shared-mcp.onrender.com",
        "claude-shared-mcp.onrender.com:*",
    ]
)

mcp.settings.transport_security = security
app = mcp.streamable_http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
