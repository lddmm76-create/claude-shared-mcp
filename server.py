
import os
import sqlite3
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

DB_PATH = os.environ.get("DB_PATH", "/tmp/shared_mcp.db")

mcp = FastMCP("Shared Notes MCP", stateless_http=True, json_response=True)

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                details TEXT DEFAULT '',
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

init_db()

@mcp.tool()
def save_note(title: str, content: str) -> str:
    """메모를 데이터베이스에 저장합니다."""
    if not title.strip() or not content.strip():
        return "오류: 제목과 내용을 입력해 주세요."
    with connect_db() as conn:
        cur = conn.execute(
            "INSERT INTO notes (title, content) VALUES (?, ?)",
            (title.strip(), content.strip())
        )
        note_id = cur.lastrowid
    return f"메모 저장 완료. 메모 번호: {note_id}, 제목: {title.strip()}"

@mcp.tool()
def list_notes() -> str:
    """저장된 최근 메모 50개를 조회합니다."""
    with connect_db() as conn:
        rows = conn.execute(
            "SELECT id, title, created_at FROM notes ORDER BY id DESC LIMIT 50"
        ).fetchall()
    if not rows:
        return "저장된 메모가 없습니다."
    return "\n".join(
        f"번호: {r['id']} | 제목: {r['title']} | 작성일: {r['created_at']}"
        for r in rows
    )

@mcp.tool()
def get_note(note_id: int) -> str:
    """메모 번호로 저장된 메모 내용을 불러옵니다."""
    with connect_db() as conn:
        row = conn.execute(
            "SELECT * FROM notes WHERE id = ?", (note_id,)
        ).fetchone()
    if not row:
        return f"메모 번호 {note_id}를 찾을 수 없습니다."
    return f"제목: {row['title']}\n작성일: {row['created_at']}\n\n{row['content']}"

@mcp.tool()
def create_task(title: str, details: str = "") -> str:
    """작업을 저장합니다."""
    if not title.strip():
        return "오류: 작업 제목을 입력해 주세요."
    with connect_db() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, details) VALUES (?, ?)",
            (title.strip(), details.strip())
        )
        task_id = cur.lastrowid
    return f"작업 저장 완료. 작업 번호: {task_id}, 제목: {title.strip()}"

@mcp.tool()
def list_tasks(include_done: bool = True) -> str:
    """저장된 작업 목록을 조회합니다."""
    with connect_db() as conn:
        if include_done:
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY id DESC LIMIT 100"
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE done = 0 ORDER BY id DESC LIMIT 100"
            ).fetchall()
    if not rows:
        return "조회된 작업이 없습니다."
    return "\n".join(
        f"번호: {r['id']} | {'완료' if r['done'] else '진행 중'} | "
        f"{r['title']} | {r['details']}"
        for r in rows
    )

@mcp.tool()
def complete_task(task_id: int) -> str:
    """작업 번호로 완료 처리합니다."""
    with connect_db() as conn:
        cur = conn.execute(
            "UPDATE tasks SET done = 1 WHERE id = ?", (task_id,)
        )
    if cur.rowcount == 0:
        return f"작업 번호 {task_id}를 찾을 수 없습니다."
    return f"작업 {task_id}번을 완료 처리했습니다."

@mcp.tool()
def server_status() -> str:
    """서버와 데이터베이스 상태를 확인합니다."""
    with connect_db() as conn:
        conn.execute("SELECT 1")
    return "MCP 서버와 데이터베이스가 정상 작동 중입니다."

security = TransportSecuritySettings(
    allowed_hosts=["claude-shared-mcp.onrender.com"]
)
mcp.settings.transport_security = security
app = mcp.streamable_http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
