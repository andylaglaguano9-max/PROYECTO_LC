from passlib.context import CryptContext
from app.schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db: list[dict] = []
current_id: int = 0


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(user_id: int) -> dict | None:
    return next((u for u in users_db if u["id"] == user_id), None)


def get_user_by_email(email: str) -> dict | None:
    return next((u for u in users_db if u["email"] == email), None)


def get_user_by_username(username: str) -> dict | None:
    return next((u for u in users_db if u["username"] == username), None)


def get_users(skip: int = 0, limit: int = 100) -> list[dict]:
    return users_db[skip: skip + limit]


def create_user(user: UserCreate) -> dict:
    global current_id
    current_id += 1
    db_user = {
        "id": current_id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "hashed_password": hash_password(user.password),
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
    }
    users_db.append(db_user)
    return db_user


def update_user(user_id: int, user: UserUpdate) -> dict | None:
    db_user = get_user(user_id)
    if not db_user:
        return None
    update_data = user.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    for key, value in update_data.items():
        db_user[key] = value
    return db_user


def delete_user(user_id: int) -> bool:
    global users_db
    user = get_user(user_id)
    if not user:
        return False
    users_db = [u for u in users_db if u["id"] != user_id]
    return True
