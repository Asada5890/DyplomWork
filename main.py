from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.security import get_password_hash
from db.session import get_db
from models.user import User

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Настройка базы данных
DATABASE_URL = "sqlite+aiosqlite:///./example.db"
engine = create_async_engine(DATABASE_URL, future=True)
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Создаем новые таблицы с актуальной структурой
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы успешно пересозданы")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@app.post("/create-user/")
async def create_user(
    request: Request,
    name: str = Form(...),
    sur_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        hashed_password = get_password_hash(password)
        db_user = User(
            name=name,
            surname=sur_name,
            email=email,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        return templates.TemplateResponse("create_user.html", {
            "request": request,
            "message": "Пользователь успешно создан!"
        })
        
    except Exception as e:
        await db.rollback()
        return templates.TemplateResponse("create_user.html", {
            "request": request,
            "error": f"Ошибка: {str(e)}"
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)