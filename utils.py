import asyncio
from argon2 import PasswordHasher

hasher = PasswordHasher(time_cost=2, memory_cost=32768)

async def verify_password(stored_hash, password):
    loop = asyncio.get_running_loop()
    try:
        return await loop.run_in_executor(None, hasher.verify, stored_hash, password)
    except Exception as e:
        print(f"an error occured verifying password: {e}")
        return False
     