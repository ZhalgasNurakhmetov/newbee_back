from datetime import timedelta

from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.models.models import EntrepreneurModel, ClientModel

from database.database import get_db

router = InferringRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth", auto_error=False)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> EntrepreneurModel | ClientModel:
    user: EntrepreneurModel | ClientModel = check_token(token, db)
    return user


def check_token(token: str, db: Session) -> EntrepreneurModel | ClientModel:
    from jose import jwt
    from config.config import config
    from services.auth.schemas.auth_schemas import TokenDataSchema
    from datetime import datetime
    from error_handler.error_handler_service import user_not_found_exception, unauthorized_exception

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id: str = payload.get("sub")
        expires: datetime = payload.get("exp")
        if user_id is None:
            raise user_not_found_exception
        if expires is None or datetime.utcnow() > datetime.fromtimestamp(expires):
            raise unauthorized_exception
        token_data = TokenDataSchema(id=user_id, expires=expires)
    except Exception:
        raise unauthorized_exception
    user: EntrepreneurModel | ClientModel = EntrepreneurModel.get_by_id(token_data.id, db) if EntrepreneurModel.get_by_id(token_data.id, db) else ClientModel.get_by_id(token_data.id, db)
    if user is None:
        raise user_not_found_exception
    return user


def generate_access_token(data: dict, expires_delta: timedelta = None):
    from datetime import datetime
    from jose import jwt
    from config.config import config

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}


@cbv(router)
class Auth:
    from services.auth.schemas.auth_schemas import TokenSchema
    from services.auth.schemas.auth_schemas import UserCredentialsSchema

    @router.post('/auth', response_model=TokenSchema)
    def authenticate(self, credentials: UserCredentialsSchema, db: Session = Depends(get_db)):
        from datetime import timedelta
        from config.config import config

        user = self.authenticate_user(credentials, db)
        access_token_expires = timedelta(weeks=config.ACCESS_TOKEN_EXPIRE_WEEKS)
        return generate_access_token(data={"sub": user.id}, expires_delta=access_token_expires)

    @staticmethod
    def authenticate_user(credentials: UserCredentialsSchema, db: Session) -> EntrepreneurModel | ClientModel:
        from error_handler.error_handler_service import user_not_found_exception, credentials_exception

        user: EntrepreneurModel | ClientModel = EntrepreneurModel.get_by_username(credentials.username, db) if EntrepreneurModel.get_by_username(
            credentials.username, db) else ClientModel.get_by_username(credentials.username, db)
        if not user:
            raise user_not_found_exception
        if not pwd_context.verify(credentials.password, user.password):
            raise credentials_exception
        return user
