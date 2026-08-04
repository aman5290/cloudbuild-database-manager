from src.utils.password import hash_password
from src.utils.password import verify_password

password = "Admin123!"

hashed = hash_password(password)

print("Hash:")
print(hashed)

print()

print("Match:")
print(verify_password("Admin123!", hashed))

print()

print("Wrong Password:")
print(verify_password("WrongPassword", hashed))
