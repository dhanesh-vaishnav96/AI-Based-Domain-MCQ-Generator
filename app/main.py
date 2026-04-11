from fastapi import FastAPI
from app.api.v1.mcq_routes import router as mcq_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.include_router(mcq_router)
# Static setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# templates = Jinja2Templates(directory="templates")


app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)