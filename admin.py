from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from werkzeug.security import check_password_hash
import secrets
from database import Session
from repositories.admin_repositories import AdminRepository
import os
from dotenv import load_dotenv
import logging


load_dotenv()
security = HTTPBasic()
app = FastAPI(title='Панель админа')
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger("admin_authentication")
logger.setLevel(logging.WARNING)

def check_the_password(request: Request, credentials: HTTPBasicCredentials=Depends(security)):
    correct_username = os.getenv('ADMIN_USERNAME')
    correct_password_hash = os.getenv('ADMIN_PASSWORD_HASH')

    is_correct_username = secrets.compare_digest(credentials.username, correct_username)
    is_correct_password = check_password_hash(correct_password_hash, credentials.password)

    if not (is_correct_username and is_correct_password):
        client_ip = request.client.host if request.client else 'Unknown'
        logger.warning(f"FAILED LOGIN; IP: {client_ip} USERNAME = '{credentials.username}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Неверный логин или пароль",
            headers={'WWW-Authenticate': 'Basic'},
        )
    return credentials.username
def get_admin_repo():
    session = Session()
    try:
        yield AdminRepository(session)
    finally:
        session.close()

@app.get('/admin', response_class=HTMLResponse)
def admin_panel(request: Request, repo = Depends(get_admin_repo), username: str = Depends(check_the_password)):
    users = repo.get_all_users()
    return templates.TemplateResponse(request=request, name='index.html', context={'users': users})

@app.get("/admin/confirm_delete/{tg_id}", response_class=HTMLResponse)
def confirm_delete_user(request: Request, tg_id: int, repo = Depends(get_admin_repo)):
    user = repo.get_user(tg_id)
    if not user:
        return RedirectResponse(url='/admin', status_code=303)

    return templates.TemplateResponse(request=request, name='confirm_delete.html', context={'user': user})

@app.post('/admin/delete/{tg_id}')
def delete_user(tg_id: int, repo = Depends(get_admin_repo)):
    repo.delete_user(tg_id)
    return RedirectResponse(url='/admin', status_code=303)

@app.get('/admin/confirm_reset/{tg_id}', response_class=HTMLResponse)
def confirm_reset_score(request: Request, tg_id: int, repo = Depends(get_admin_repo)):
    user = repo.get_user(tg_id)
    if not user:
        return RedirectResponse(url='/admin', status_code=303)
    return templates.TemplateResponse(request=request, name='confirm_reset.html', context={'user': user})

@app.post('/admin/reset/{tg_id}')
def reset_user(tg_id: int, repo = Depends(get_admin_repo)):
    repo.reset_user(tg_id)
    return RedirectResponse(url='/admin', status_code=303)

@app.get('/admin/change_score/{tg_id}')
def confirm_reset_score(request: Request, tg_id: int, repo = Depends(get_admin_repo)):
    score = Form()
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)