from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory='/code/templates')


@app.get("/", response_class=HTMLResponse)
async def read_item(request : Request):
    num = 100
    return templates.TemplateResponse("progress.html", {"request": request, "num": num})
