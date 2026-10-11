"""
rank_api.py  (backend folder)
POST /api/rank  ->  frontend (index.html) ke liye CVs rank karta hai.

Flow:  CV file -> file_reader.read_cv_bytes -> match.match_candidate (extractor + semantic_matcher)
Frontend bhejta hai (multipart/form-data):  jd (text), top_n (number, 0 = all), cvs (files)
Wapas:  {"results": [{filename, score, matched_skills, missing_skills, summary}], "skipped": [...]}
"""
import sys
from pathlib import Path
from typing import List

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

# nlp folder ke modules (flat imports use karte hain) import karne ke liye path add
NLP_DIR = Path(__file__).resolve().parent.parent / "nlp"
sys.path.insert(0, str(NLP_DIR))

from file_reader import read_cv_bytes          # noqa: E402
from match import match_candidate              # noqa: E402

router = APIRouter()

MAX_FILES = 50
MAX_FILE_MB = 5


def _summary(m: dict) -> str:
    text = (f"Skills {m['skills_score']:.0f}%, experience {m['experience_score']:.0f}%, "
            f"education {m['education_score']:.0f}%.")
    good = [e for e in m.get("semantic_evidence", []) if e.get("status") == "potential_match"]
    if good:
        best = max(good, key=lambda e: e["similarity"])
        text += f" Best evidence: \"{best['cv_evidence'][:120]}\""
    return text


@router.post("/api/rank")
async def rank(jd: str = Form(...), top_n: int = Form(10), cvs: List[UploadFile] = File(...)):
    if not jd.strip():
        raise HTTPException(400, "Job description khali hai")
    if not cvs:
        raise HTTPException(400, "Kam az kam ek CV upload karein")
    if len(cvs) > MAX_FILES:
        raise HTTPException(400, f"Ek baar mein maximum {MAX_FILES} CVs")

    results, skipped = [], []
    for f in cvs:
        content = await f.read()
        if len(content) > MAX_FILE_MB * 1024 * 1024:
            skipped.append({"filename": f.filename, "reason": f"{MAX_FILE_MB} MB se bari file"})
            continue
        try:
            cv_text = read_cv_bytes(content, f.filename)
            m = await run_in_threadpool(match_candidate, jd, cv_text)
        except Exception as e:                       # kharab file poore request ko na toray
            skipped.append({"filename": f.filename, "reason": str(e)})
            continue
        results.append({
            "filename": f.filename,
            "score": m["final_score"],
            "matched_skills": sorted(m["matched_skills"]),
            "missing_skills": sorted(m["missing_skills"]),
            "summary": _summary(m),
        })

    results.sort(key=lambda r: r["score"], reverse=True)
    if top_n and top_n > 0:
        results = results[:top_n]
    return {"results": results, "skipped": skipped}
