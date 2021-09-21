from app.services import AuthService
from app.models import User


async def create_test_user(
    username,
    email,
    full_name,
    role,
    is_superuser=False,
    password="password",
    is_active=False,
) -> User():
    test_user = await User.create(
        username=username,
        email=email,
        full_name=full_name,
        role=role,
        is_superuser=is_superuser,
        hash_password=AuthService.hash_password(password),
        is_active=is_active,
    )
    return test_user
