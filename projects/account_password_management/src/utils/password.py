from passlib.context import CryptContext

# autogenerate salt https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html#passlib.hash.bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
