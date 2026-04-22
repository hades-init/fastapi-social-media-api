from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

# When the username doesn't exist in the database, we still run verify_password() against a dummy hash 
DUMMY_HASH = password_hash.hash("dummypassword")

# Return hashed password
def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

# Verify password against given hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)
