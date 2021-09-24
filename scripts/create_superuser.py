import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# flake8: noqa F401
from tortoise import Tortoise, run_async
from app.config import settings
from app.services.user import UserService
from app.serializers import UserRegistration


async def main():
    """Create superuser"""
    await Tortoise.init(
        db_url=settings.DATABASE_URI,
        modules={"models": ["models"]},
    )
    print("Create superuser")
    username = input("Username: ")
    email = input("Email: ")
    full_name = input("Full name: ")
    password = input("Password: ")
    role = input("Role:")
    user_service = UserService()
    super_user = await user_service.get_username_email(username=username, email=email)
    if not super_user:
        user_in = UserRegistration(
            username=username,
            email=email,
            full_name=full_name,
            role=role,
            password=password,
            is_superuser=True,
        )
        await user_service.create_superuser(schema=user_in)
        print("Success")
    else:
        print("Error, user existing")


if __name__ == "__main__":
    run_async(main())
