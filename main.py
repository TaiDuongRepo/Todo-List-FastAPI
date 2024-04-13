from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    with open('database.json') as file:
        data = json.load(file)
    return templates.TemplateResponse("todolist.html", {"request": request, "tododict": data})

@app.get("/delete/{id}")
async def delete_todo(request: Request, id:str):
    with open('database.json') as file:
        data = json.load(file)
    del data[id]
    with open('database.json', 'w') as file:
        json.dump(data, file)

    return RedirectResponse("/", 303)

@app.post("/add")
async def add_todo(request: Request):
    with open('database.json') as file:
        data = json.load(file)

    formdata = await request.form()
    newdata = {}
    i = 1
    for id in data:
        newdata[str(i)] = data[id]
        i += 1
    
    newdata[str(i)] = formdata['newtodo']
    print(newdata)
    with open('database.json', 'w') as file:
        json.dump(newdata, file)

    return RedirectResponse("/", 303)