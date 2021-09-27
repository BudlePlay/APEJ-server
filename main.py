from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import threading

import os

# os.chdir("/src/")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

stubs = []
ips = set()
prev_ip = ""


def startTimer():
    global prev_ip
    prev_ip = ""
    print("도배 풀림")




@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})


@app.post("/send")
def form_get(request: Request, stub: str = Form(...)):
    global prev_ip

    result = stub
    print(result, request.client.host)

    ips.add(request.client.host)

    if request.client.host != prev_ip:
        stubs.append(result)
    else:
        print('도배 의심', request.client.host)
        timer = threading.Timer(60, startTimer)
        timer.start()
        print(timer.is_alive())

    prev_ip = request.client.host

    return RedirectResponse("/end", status_code=302)


@app.get("/end", response_class=HTMLResponse)
async def end(request: Request):
    return templates.TemplateResponse('form.html', context={'request': request, 'result': "완료"})


@app.get("/discord")
def form_post():
    if len(stubs) > 0:
        return {"flag": "success", "stub": stubs.pop(0)}
    else:
        return {"flag": "fail"}
