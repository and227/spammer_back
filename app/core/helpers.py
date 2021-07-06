from passlib.context import CryptContext

pass_context = CryptContext(schemes=['sha256_crypt'], deprecated="auto")