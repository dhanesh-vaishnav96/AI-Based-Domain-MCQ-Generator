from fastapi import APIRouter, HTTPException, Request, Form, BackgroundTasks
from fastapi.responses import  HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates


from app.services.excel_service import generate_excel
from app.core.domain_config import DOMAINS
from app.models.request_models import MCQRequest

from app.services.input_validator import validate_request
from app.services.topic_engine import distribute_topics
from app.services.batch_service import generate_mcqs_topicwise

from app.services.prompt_builder import build_prompt
from app.services.llm_service import generate_with_retry
from app.services.validator import ( validate_mcq_list, fill_missing_questions )

from pathlib import Path
import os


router = APIRouter(prefix="/api/v1/mcq")

BASE_DIR = Path(__file__).resolve().parents[3]

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "mcqs": None,
            "form_data": {
                "domain": "",
                "difficulty": "",
                "num_questions": ""
            }
        }
    )


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/generate-download")
def generate_and_download(
    domain: str = Form(...),
    difficulty: str = Form(...),
    num_questions: int = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):

    # Step 1: validate request
    request_data  = MCQRequest(
        domain=domain,
        difficulty=difficulty,
        num_questions=num_questions
    )
    validate_request(request_data )

    # Step 2: get domain topics
    topics = DOMAINS.get(domain)
    if not topics:
        raise HTTPException(status_code=400, detail="Invalid domain")


    distributed_topics = distribute_topics(topics, num_questions)

    raw_mcqs = generate_mcqs_topicwise(
        build_prompt,
        distributed_topics,
        difficulty,
        domain
    )

    # Step 5: validate MCQs
    valid_mcqs = validate_mcq_list(raw_mcqs)

    # Step 6: fill missing questions
    final_mcqs = fill_missing_questions(
        valid_mcqs,
        num_questions,
        lambda: generate_with_retry(
            build_prompt("Basics", difficulty, domain, 3)
        )
    )

    # Step 7: generate Excel
    file_path = generate_excel(final_mcqs)

   # Step 8: create filename
    filename = f"{domain.lower().replace(' ', '-')}-{num_questions}mcq-{difficulty.lower()}.xlsx"



    # STREAMING RESPONSE
    def iterfile():
        with open(file_path, "rb") as file:
            yield from file

    response = StreamingResponse(
        iterfile(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'

    # SAFE CLEANUP 
    def cleanup():
        if os.path.exists(file_path):
            os.remove(file_path)

    background_tasks.add_task(cleanup)

    return response