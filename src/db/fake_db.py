from auth.utils import get_password_hash

db = {
    "michal": {
        "username": "michal",
        "full_name": "Michal",
        "email": "michal@gmail.com",
        "hashed_password": "$2b$12$8ioB2bXqC.9jEhbwDqKdAexmntd5dfV/Pkd57tlRYEYB2AzjsGZp2",
        "disabled": False,
    },
    "testuser": {
        "username": "testuser",
        "hashed_password": get_password_hash("testpassword"),
        "disabled": False,
    },
    "inactive_user": {
        "username": "inactive_user",
        "hashed_password": get_password_hash("testpassword"),
        "disabled": True,
    },
}
