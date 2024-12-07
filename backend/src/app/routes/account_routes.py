from utils.base import SessionLocal
from src.models import Account
from src.schemas import AccountSchema
from fastapi.routing import APIRouter
from utils.swagger_configs import RouteTags
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

account_router = APIRouter(tags=[RouteTags.ACCOUNT])
session = SessionLocal()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    password: str | None = None


pwe_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwe_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwe_context.hash(password)


def authenticate_user(username: str, password: str):
    user = session.query(Account).filter(Account.username == username).first()
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user


def get_user(username: str):
    user = session.query(Account).filter(Account.username == username).first()
    session.close()
    if user:
        return user


def create_access_token(data: dict, expires_delta: int | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth_2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Account = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@account_router.get("/token", response_model=Token)
async def login_for_access_token(form_data: dict):
    print(form_data)
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"access_token": access_token, "token_type": "bearer"}


@account_router.get("/me", response_model=AccountSchema)
async def read_users_me(current_user: Account = Depends(get_current_active_user)):
    return current_user


@account_router.get("/me/items")
async def read_users(current_user: Account = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@account_router.get("/")
async def root():
    return {"message": "Hellow World"}


@account_router.post("/signup")
async def signup_view(data: AccountSchema):
    hashed_password = get_password_hash(data.password)
    data.password = hashed_password
    session = SessionLocal()
    try:
        account = Account(**data.dict())
        session.add(account)
        session.commit()
        session.refresh(account)
        session.close()
        fresh_account = account
        return {
            "is_success": True,
            "username": fresh_account.username,
            "first_name": fresh_account.first_name,
            "last_name": fresh_account.last_name,
        }
    except IntegrityError as e:
        session.rollback()
        print("<<<<<<<<<<<<<<<<<<<<<<<<", e)
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()


@account_router.post("/login")
async def login_view(data: TokenData):
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "first_name": user.first_name,
    }


@account_router.get("/logout")
async def logout_view():
    return {"is_success": True}
