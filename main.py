from fastapi import FastAPI, Request, Form, Depends, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import os
import json

from database import get_db, create_tables, User, Lesson, Word, UserProgress, QuizAttempt
from auth import hash_password, verify_password, create_token, get_current_user, require_user, require_admin

app = FastAPI(title="English Learning for Kids")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
    create_tables()
    db = next(get_db())
    # If no users exist at all → fresh cloud deployment, run full seed
    if db.query(User).count() == 0:
        from seed_all import seed_data
        seed_data(db)
    db.close()


# ─── Auth Routes ────────────────────────────────────────────────────────────

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login")
def login(request: Request, response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "שם משתמש או סיסמה שגויים"})
    token = create_token(user.id)
    resp = RedirectResponse(url="/", status_code=302)
    resp.set_cookie("token", token, httponly=True, max_age=604800)
    return resp


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})


@app.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...), email: str = Form(""), db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        return templates.TemplateResponse("register.html", {"request": request, "error": "שם המשתמש כבר קיים"})
    user = User(username=username, email=email or None, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    token = create_token(user.id)
    resp = RedirectResponse(url="/", status_code=302)
    resp.set_cookie("token", token, httponly=True, max_age=604800)
    return resp


@app.get("/logout")
def logout():
    resp = RedirectResponse(url="/login", status_code=302)
    resp.delete_cookie("token")
    return resp


# ─── Home ─────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    lessons = db.query(Lesson).filter(Lesson.is_published == True).order_by(Lesson.week_number).all()
    progress_map = {}
    if user:
        for p in db.query(UserProgress).filter(UserProgress.user_id == user.id).all():
            progress_map[p.lesson_id] = p

    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": user,
        "lessons": lessons,
        "progress_map": progress_map,
    })


# ─── Lesson ───────────────────────────────────────────────────────────────

@app.get("/lessons/{lesson_id}", response_class=HTMLResponse)
def lesson_page(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.is_published == True).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    progress = db.query(UserProgress).filter(UserProgress.user_id == user.id, UserProgress.lesson_id == lesson_id).first()
    if not progress:
        progress = UserProgress(user_id=user.id, lesson_id=lesson_id)
        db.add(progress)
        db.commit()
        db.refresh(progress)

    return templates.TemplateResponse("lesson.html", {
        "request": request,
        "user": user,
        "lesson": lesson,
        "progress": progress,
    })


@app.post("/lessons/{lesson_id}/mark-reading")
def mark_reading_done(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return JSONResponse({"ok": False}, status_code=401)
    progress = db.query(UserProgress).filter(UserProgress.user_id == user.id, UserProgress.lesson_id == lesson_id).first()
    if progress:
        progress.reading_done = True
        db.commit()
    return JSONResponse({"ok": True})


@app.post("/lessons/{lesson_id}/mark-words")
def mark_words_done(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return JSONResponse({"ok": False}, status_code=401)
    progress = db.query(UserProgress).filter(UserProgress.user_id == user.id, UserProgress.lesson_id == lesson_id).first()
    if progress:
        progress.words_studied = True
        db.commit()
    return JSONResponse({"ok": True})


# ─── Quiz ─────────────────────────────────────────────────────────────────

@app.get("/lessons/{lesson_id}/quiz", response_class=HTMLResponse)
def quiz_page(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.is_published == True).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    progress = db.query(UserProgress).filter(UserProgress.user_id == user.id, UserProgress.lesson_id == lesson_id).first()
    words = lesson.words
    words_json = [{"id": w.id, "english": w.english, "hebrew": w.hebrew, "example": w.example_sentence or ""} for w in words]

    return templates.TemplateResponse("quiz.html", {
        "request": request,
        "user": user,
        "lesson": lesson,
        "progress": progress,
        "words_json": json.dumps(words_json),
        "words": words,
    })


@app.post("/api/quiz/submit")
async def submit_quiz(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return JSONResponse({"ok": False}, status_code=401)

    data = await request.json()
    lesson_id = data.get("lesson_id")
    stage = data.get("stage")
    answers = data.get("answers", [])

    correct_count = 0
    for ans in answers:
        word = db.query(Word).filter(Word.id == ans["word_id"]).first()
        if not word:
            continue

        is_correct = False
        if stage == 1:
            # Check Hebrew translation (flexible matching)
            user_ans = ans.get("answer", "").strip()
            correct_ans = word.hebrew.strip()
            is_correct = user_ans.lower() == correct_ans.lower() or user_ans in correct_ans or correct_ans in user_ans
        elif stage == 2:
            # Check if English word appears in the sentence
            user_ans = ans.get("answer", "").strip().lower()
            is_correct = word.english.lower() in user_ans and len(user_ans) > len(word.english) + 2

        if is_correct:
            correct_count += 1

        attempt = QuizAttempt(
            user_id=user.id,
            lesson_id=lesson_id,
            stage=stage,
            word_id=word.id,
            user_answer=ans.get("answer", ""),
            is_correct=is_correct,
        )
        db.add(attempt)

    score = round((correct_count / len(answers)) * 100) if answers else 0

    progress = db.query(UserProgress).filter(UserProgress.user_id == user.id, UserProgress.lesson_id == lesson_id).first()
    if progress:
        if stage == 1:
            progress.quiz_stage1_done = True
            progress.stage1_score = score
        elif stage == 2:
            progress.quiz_stage2_done = True
            progress.stage2_score = score
            if progress.quiz_stage1_done:
                progress.completed_at = datetime.utcnow()

    db.commit()
    return JSONResponse({"ok": True, "score": score, "correct": correct_count, "total": len(answers)})


# ─── Profile ──────────────────────────────────────────────────────────────

@app.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    progresses = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == user.id)
        .join(Lesson)
        .filter(Lesson.is_published == True)
        .all()
    )
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "progresses": progresses,
    })


# ─── Admin ─────────────────────────────────────────────────────────────────

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse(url="/", status_code=302)

    lessons = db.query(Lesson).order_by(Lesson.week_number).all()
    users = db.query(User).filter(User.is_admin == False).order_by(User.username).all()
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "user": user,
        "lessons": lessons,
        "users": users,
    })


@app.post("/admin/users/{user_id}/set-level")
async def set_user_level(user_id: int, request: Request, db: Session = Depends(get_db)):
    admin = get_current_user(request, db)
    if not admin or not admin.is_admin:
        return JSONResponse({"ok": False}, status_code=403)
    data = await request.json()
    target = db.query(User).filter(User.id == user_id).first()
    if target:
        target.level = data.get("level", "intermediate")
        db.commit()
        return JSONResponse({"ok": True})
    return JSONResponse({"ok": False})


@app.post("/admin/users/new")
async def create_user(request: Request, db: Session = Depends(get_db)):
    admin = get_current_user(request, db)
    if not admin or not admin.is_admin:
        return RedirectResponse(url="/", status_code=302)
    form = await request.form()
    username = form.get("username", "").strip()
    password = form.get("password", "").strip()
    level = form.get("level", "intermediate")
    if username and password and not db.query(User).filter(User.username == username).first():
        db.add(User(username=username, hashed_password=hash_password(password), level=level))
        db.commit()
    return RedirectResponse(url="/admin?tab=users", status_code=302)


@app.post("/admin/users/{user_id}/delete")
def delete_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    admin = get_current_user(request, db)
    if not admin or not admin.is_admin:
        return RedirectResponse(url="/", status_code=302)
    target = db.query(User).filter(User.id == user_id, User.is_admin == False).first()
    if target:
        db.delete(target)
        db.commit()
    return RedirectResponse(url="/admin?tab=users", status_code=302)


@app.get("/admin/lessons/new", response_class=HTMLResponse)
def new_lesson_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("lesson_edit.html", {"request": request, "user": user, "lesson": None, "words": []})


@app.post("/admin/lessons/new")
async def create_lesson(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse(url="/", status_code=302)

    form = await request.form()
    lesson = Lesson(
        title=form.get("title"),
        topic=form.get("topic"),
        level=form.get("level", "intermediate"),
        reading_text=form.get("reading_text"),
        week_number=int(form.get("week_number") or 0) or None,
        is_published=form.get("is_published") == "on",
    )
    db.add(lesson)
    db.flush()

    # Parse words from form
    words_data = json.loads(form.get("words_json", "[]"))
    for w in words_data:
        word = Word(
            lesson_id=lesson.id,
            english=w.get("english", ""),
            hebrew=w.get("hebrew", ""),
            example_sentence=w.get("example", ""),
            phonetic=w.get("phonetic", ""),
            word_type=w.get("word_type", ""),
        )
        db.add(word)

    db.commit()
    return RedirectResponse(url="/admin", status_code=302)


@app.get("/admin/lessons/{lesson_id}/edit", response_class=HTMLResponse)
def edit_lesson_page(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse(url="/", status_code=302)
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404)
    words = lesson.words
    return templates.TemplateResponse("lesson_edit.html", {"request": request, "user": user, "lesson": lesson, "words": words})


@app.post("/admin/lessons/{lesson_id}/edit")
async def update_lesson(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse(url="/", status_code=302)

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404)

    form = await request.form()
    lesson.title = form.get("title")
    lesson.topic = form.get("topic")
    lesson.level = form.get("level", "intermediate")
    lesson.reading_text = form.get("reading_text")
    lesson.week_number = int(form.get("week_number") or 0) or None
    lesson.is_published = form.get("is_published") == "on"

    # Replace words
    for w in lesson.words:
        db.delete(w)
    db.flush()

    words_data = json.loads(form.get("words_json", "[]"))
    for w in words_data:
        word = Word(
            lesson_id=lesson.id,
            english=w.get("english", ""),
            hebrew=w.get("hebrew", ""),
            example_sentence=w.get("example", ""),
            phonetic=w.get("phonetic", ""),
            word_type=w.get("word_type", ""),
        )
        db.add(word)

    db.commit()
    return RedirectResponse(url="/admin", status_code=302)


@app.post("/admin/lessons/{lesson_id}/delete")
def delete_lesson(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        return RedirectResponse(url="/", status_code=302)
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson:
        db.delete(lesson)
        db.commit()
    return RedirectResponse(url="/admin", status_code=302)


@app.post("/admin/lessons/{lesson_id}/toggle-publish")
def toggle_publish(lesson_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        return JSONResponse({"ok": False}, status_code=403)
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson:
        lesson.is_published = not lesson.is_published
        db.commit()
        return JSONResponse({"ok": True, "published": lesson.is_published})
    return JSONResponse({"ok": False})


# ─── AI Generation ─────────────────────────────────────────────────────────

@app.post("/api/generate-lesson")
async def generate_lesson(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user or not user.is_admin:
        return JSONResponse({"ok": False}, status_code=403)

    data = await request.json()
    topic = data.get("topic", "")
    level = data.get("level", "intermediate")
    word_count = data.get("word_count", 15)

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return JSONResponse({"ok": False, "error": "ANTHROPIC_API_KEY not set"})

    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    level_desc = {"beginner": "easy (A1-A2)", "intermediate": "medium (B1-B2)", "advanced": "challenging (C1-C2)"}.get(level, "medium")

    prompt = f"""Create an English reading lesson for Israeli teenagers (age 11-15) about the topic: "{topic}".
Level: {level_desc}
Number of vocabulary words: {word_count}

Return ONLY valid JSON with this exact structure:
{{
  "title": "Lesson title",
  "reading_text": "A paragraph of 150-250 words in English about the topic, appropriate for the age group",
  "words": [
    {{
      "english": "word",
      "hebrew": "מילה בעברית",
      "phonetic": "/fəˈnetɪk/",
      "word_type": "noun/verb/adjective/adverb",
      "example": "A natural example sentence using the word"
    }}
  ]
}}

Make the reading text engaging and age-appropriate. Choose vocabulary words that appear in the text."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        content = message.content[0].text
        # Extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return JSONResponse({"ok": True, "data": result})
        return JSONResponse({"ok": False, "error": "Could not parse AI response"})
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})
