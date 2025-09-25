from passlib.context import CryptContext

bcryp_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password):
    return bcryp_context.hash(password)

def verify_password(password, hased_password):
    return bcryp_context.verify(password, hased_password)
    