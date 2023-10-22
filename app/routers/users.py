from app.schemas import users
from app.utils import users as users_utils
from app.utils.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.get("/users")
async def health_check():
    return {"Hello": "World"}


@router.post("/auth", response_model=users.TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_utils.get_user_by_email(email=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not users_utils.validate_password(
        password=form_data.password, hashed_password=user["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return await users_utils.create_user_token(user_id=user["id"])


@router.post("/sign-up", response_model=users.User)
async def create_user(user: users.UserCreate):
    db_user = await users_utils.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await users_utils.create_user(user=user)


@router.get("/users/me", response_model=users.UserBase)
async def read_users_me(current_user: users.User = Depends(get_current_user)):
    return current_user


@router.get("/users/{user_id}", response_model=users.UserBase)
async def get_user(user_id: int, current_user: users.User = Depends(get_current_user)):
    return await users_utils.get_user(user_id, current_user)


@router.delete("/users/{user_id}", response_model=users.UserBase)
async def delete_user(user_id: int, current_user: users.User = Depends(get_current_user)):
    return await users_utils.delete_user(user_id, current_user)


@router.put("/users/{user_id}", response_model=users.UserBase)
async def update_user(
    user_id: int, user_data: users.UserBase, current_user: users.User = Depends(get_current_user)
):
    # user_data = await users_utils.get_user(user_id)
    # # print(account)

    await users_utils.update_user(user_id=user_id, user=user_data, current_user=current_user)
    return await users_utils.get_user(user_id, current_user)
