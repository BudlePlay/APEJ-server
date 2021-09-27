from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os

# os.chdir("/src/")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

stubs = []


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})


@app.post("/send")
def form_get(request: Request, stub: str = Form(...)):
    result = stub
    print(result)
    stubs.append(result)

    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@app.get("/discord")
def form_post():
    if len(stubs) > 0:
        return {"flag": "success", "stub": stubs.pop(0)}
    else:
        return {"flag": "fail"}
