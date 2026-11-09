from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn

from Database import Session
from repositories.admin_repositories import AdminRepository

app = FastAPI(title='Панель админа')
templates = Jinja2Templates(directory="templates")

def get_admin_repo():
    session = Session()
    try:
        yield AdminRepository(session)
    finally:
        session.close()

@app.get('/admin', response_class=HTMLResponse)
def admin_panel(request: Request):
    session = Session()
    repo = AdminRepository(session)
    users = repo.get_all_users()
    session.close()

    return templates.TemplateResponse(request=request, name='index.html', context={'users': users})

@app.post('/admin/delete/{tg_id}')
def delete_user(tg_id: int, request: Request):
    session = Session()
    repo = AdminRepository(session)
    repo.delete_user(tg_id)
    session.close()

    return RedirectResponse(url='/admin', status_code=303)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)