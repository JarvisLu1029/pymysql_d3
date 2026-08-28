"""消失的黃金吐司：FastAPI + Jinja2 教學遊戲。"""

from __future__ import annotations

import importlib.util
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.middleware.sessions import SessionMiddleware

BASE_DIR = Path(__file__).resolve().parent
STUDENT_FILE = BASE_DIR / "03_student_starter.py"
CASE_START = "2026-08-20 21:10:00"
CASE_END = "2026-08-20 21:35:00"


@dataclass(frozen=True)
class Chapter:
    number: int
    label: str
    title: str
    skill: str
    prompt: str
    placeholder: str
    function_name: str
    function_args: tuple[Any, ...]
    result_hint: str
    answers: tuple[str, ...]
    validate: Callable[[list[dict[str, Any]]], bool]


def _contains(rows: list[dict[str, Any]], *needles: str) -> bool:
    text = " ".join(str(value) for row in rows for value in row.values()).casefold()
    return all(needle.casefold() in text for needle in needles)


CHAPTERS = (
    Chapter(1, "案件卷宗", "黃金吐司消失", "SELECT / View", "黃金吐司從哪一個房間消失？", "例如：R00", "load_case_brief", (), "預期欄位：case_name、estimated_start、discovered_at、crime_room、mission", ("r03", "Ｒ０３"), lambda rows: _contains(rows, "消失的黃金吐司", "R03")),
    Chapter(2, "門禁紀錄", "四名金庫訪客", "WHERE / BETWEEN", "依進入時間，成功進入 R03 的四位人員編號是？", "例如：101,102,103,104", "find_successful_r03_entries", (CASE_START, "2026-08-20 21:25:00"), "預期 4 筆；欄位：suspect_id、access_time，只可包含 SUCCESS + IN", ("104,105,109,102",), lambda rows: len(rows) == 4 and _contains(rows, "102", "104", "105", "109")),
    Chapter(3, "現場物證", "足跡與橘色纖維", "AND / 條件組合", "同時符合 27.5 足跡與橘色纖維線索的四名嫌疑人是？", "依門禁順序輸入四個姓名", "find_physical_matches", (27.5,), "預期欄位：name、shoe_size、has_orange_accessory", ("帕瓦,波奇塔,彭德·佛傑,淀治",), lambda rows: len(rows) == 4 and _contains(rows, "淀治", "帕瓦", "波奇塔", "彭德·佛傑", "27.5")),
    Chapter(4, "影像與消費", "無臉的橘色身影", "多表 JOIN", "監視器攜帶物與消費品項共同指向什麼物件？", "輸入物件名稱", "find_camera_and_purchase_clues", (CASE_START, CASE_END), "預期欄位：name、seen_time、location、carrying、item_name", ("銀色保溫袋", "保溫袋"), lambda rows: bool(rows) and _contains(rows, "銀色保溫袋", "淀治")),
    Chapter(5, "數位鑑識", "被刪除的斷電計畫", "LIKE / 自我 JOIN", "是誰要求波奇塔在 21:10 左右進行斷電？", "輸入姓名", "find_deleted_messages", ("斷電",), "預期欄位：sender_name、receiver_name、sent_at、message_text、is_deleted", ("淀治",), lambda rows: bool(rows) and _contains(rows, "淀治", "波奇塔", "斷電")),
    Chapter(6, "最終逮捕令", "纖維、保溫袋與咬痕", "DISTINCT / 多表 JOIN", "所有數位證據唯一指向誰？", "輸入完整姓名", "find_prime_suspect", (CASE_START, CASE_END), "預期欄位：suspect_id、name、job_title，且只能有一列", ("淀治", "102"), lambda rows: len(rows) == 1 and _contains(rows, "102", "淀治", "公安惡魔獵人")),
)


class AnswerPayload(BaseModel):
    level: int = Field(ge=1, le=len(CHAPTERS))
    answer: str = Field(min_length=1, max_length=80)


def create_app() -> FastAPI:
    app = FastAPI(title="消失的黃金吐司", docs_url=None, redoc_url=None)
    app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "local-detective-classroom-secret"), same_site="lax")
    app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
    templates = Jinja2Templates(directory=BASE_DIR / "templates")

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        unlocked = _get_unlocked(request)
        total = len(CHAPTERS)
        viewable_until = min(unlocked + 1, total)
        chapter = CHAPTERS[unlocked] if unlocked < total else None
        rows, query_error = _run_student_function(chapter) if chapter else ([], None)
        return templates.TemplateResponse(request=request, name="index.html", context={
            "chapters": CHAPTERS, "chapter": chapter, "unlocked": unlocked,
            "rows": rows, "columns": list(rows[0].keys()) if rows else [],
            "query_error": query_error, "total": total,
            "viewable_until": viewable_until, "is_current": chapter is not None,
            "resume_panel": unlocked + 1 if unlocked < total else 0,
        })

    @app.get("/api/panel/{chapter_number}", response_class=HTMLResponse)
    async def chapter_panel(request: Request, chapter_number: int):
        unlocked = _get_unlocked(request)
        total = len(CHAPTERS)
        viewable_until = min(unlocked + 1, total)

        if chapter_number == 0:
            if unlocked < total:
                return HTMLResponse("這份結案卷宗尚未解鎖。", status_code=403)
            chapter = None
            is_current = False
        elif 1 <= chapter_number <= viewable_until:
            chapter = CHAPTERS[chapter_number - 1]
            is_current = unlocked < total and chapter_number == unlocked + 1
        else:
            return HTMLResponse("這份卷宗尚未解鎖。", status_code=403)

        rows, query_error = _run_student_function(chapter) if chapter else ([], None)
        return templates.TemplateResponse(request=request, name="_case_panel.html", context={
            "chapter": chapter, "unlocked": unlocked, "total": total,
            "rows": rows, "columns": list(rows[0].keys()) if rows else [],
            "query_error": query_error, "is_current": is_current,
            "resume_panel": unlocked + 1 if unlocked < total else 0,
        })

    @app.post("/api/check")
    async def check_answer(request: Request, payload: AnswerPayload):
        unlocked = _get_unlocked(request)
        if unlocked >= len(CHAPTERS) or payload.level != unlocked + 1:
            return JSONResponse({"ok": False, "message": "這份卷宗尚未解鎖。"}, status_code=409)
        chapter = CHAPTERS[unlocked]
        rows, query_error = _run_student_function(chapter)
        if query_error:
            return JSONResponse({"ok": False, "message": "先完成本關 function，讓查詢成功後才能提交推理。"}, status_code=422)
        if not chapter.validate(rows):
            return JSONResponse({"ok": False, "message": "查詢結果尚未符合本關要求，請檢查 SQL 條件與欄位。"}, status_code=422)
        if _normalize(payload.answer) not in {_normalize(answer) for answer in chapter.answers}:
            return {"ok": False, "message": "推理尚有矛盾。重新比對上方查詢結果。"}
        next_unlocked = min(unlocked + 1, len(CHAPTERS))
        request.session["unlocked"] = next_unlocked
        solved = next_unlocked == len(CHAPTERS)
        next_panel = 0 if solved else next_unlocked + 1
        return {
            "ok": True, "solved": solved, "unlocked": next_unlocked,
            "next_panel": next_panel,
            "message": "證據吻合。逮捕令已完成。" if solved else "證據吻合，下一份卷宗已解鎖。",
        }

    @app.post("/reset")
    async def reset_case(request: Request):
        request.session.clear()
        return RedirectResponse(url="/", status_code=303)

    return app


def _get_unlocked(request: Request) -> int:
    value = request.session.get("unlocked", 0)
    return value if isinstance(value, int) and 0 <= value <= len(CHAPTERS) else 0


def _normalize(value: str) -> str:
    return re.sub(r"[\s,，、;；]", "", value).casefold()


def _load_student_module():
    module_name = "chapter5_student_queries"
    spec = importlib.util.spec_from_file_location(module_name, STUDENT_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法載入學生任務檔")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _run_student_function(chapter: Chapter) -> tuple[list[dict[str, Any]], str | None]:
    connection = None
    try:
        student = _load_student_module()
        connection = student.get_connection()
        result = getattr(student, chapter.function_name)(connection, *chapter.function_args)
        if not isinstance(result, (list, tuple)):
            return [], f"{chapter.function_name}() 必須回傳 list[dict]。"
        rows = list(result)
        if rows and not all(isinstance(row, dict) for row in rows):
            return [], f"{chapter.function_name}() 的每一列必須是 dict。"
        return rows, None
    except NotImplementedError as exc:
        return [], str(exc)
    except Exception as exc:
        return [], f"{type(exc).__name__}: {exc}"
    finally:
        if connection is not None:
            connection.close()


app = create_app()
