from fastapi import APIRouter, HTTPException, Depends, Request, Form
from jose import JWTError
import jwt
from requests import Session
from models.order import Order
from db import session
from core.settings import settings
from core.security import get_current_user
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
router = APIRouter()


templates = Jinja2Templates(directory="frontend")


@router.get("/sales")
def view_sale_page(request: Request):
    return templates.TemplateResponse(
        "sales.html", {"request":request})

@router.get("/delivery")
def view_sale_page(request: Request):
    return templates.TemplateResponse(
        "delivery.html", {"request":request})

@router.get("/contacts")
def view_sale_page(request: Request):
    return templates.TemplateResponse(
        "contacts.html", {"request":request})