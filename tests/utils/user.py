from app.services import AuthService
from app.models import User


async def create_test_user(
    username,
    email,
    full_name,
    role,
    password="password",
    is_active=True,
) -> User():
    test_user = await User.create(
        username=username,
        email=email,
        full_name=full_name,
        role=role,
        is_active=is_active,
        hash_password=AuthService.hash_password(password),
    )
    return test_user
