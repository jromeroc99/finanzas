import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlmodel import SQLModel, Field, Session, select
from pydantic import EmailStr
from database import engine
from models import User

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

# Crear Secret Key para JWT: openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 #duración en horas
SECRET = os.getenv("SECRET_KEY")

if not SECRET:
    raise RuntimeError("Falta SECRET_KEY en el entorno. Configúrala en .env o variables del sistema.")


# Esquemas para CRUD de usuarios
class UserRead(SQLModel):
    id: int
    username: str
    email: str
    disabled: bool

class UserCreate(SQLModel):
    username: str = Field(max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)  # bcrypt limit
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)


def search_user_db(username: str) -> User | None:
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        user_db = session.exec(statement).first()
        
        if not user_db:
            return None
        
        return user_db
    
def search_user(username: str) -> UserRead | None:
    user_db = search_user_db(username)
    if not user_db:
        return None
    
    return UserRead.model_validate(user_db)

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)

async def current_user(user: UserRead = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user_db = search_user_db(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    

    if not crypt.verify(form.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {"sub": user_db.username,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate):
    user_db = search_user_db(user.username)
    if user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya existe")

    hashed_password = crypt.hash(user.password)
    
    # Crear instancia de User para la base de datos
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        name=user.name,
        surname=user.surname
    )

    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return UserRead.model_validate(new_user)
    
@router.get("/users/me")
async def me(user: UserRead = Depends(current_user)):
    return user