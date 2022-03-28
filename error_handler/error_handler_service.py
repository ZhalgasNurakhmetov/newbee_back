from fastapi import HTTPException, status


user_already_exist_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Учетная запись уже существует',
)

user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Пользователь не найден',
)

unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не авторизован",
    headers={"WWW-Authenticate": "Bearer"},
)

credentials_exception = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail='Неверный логин или пароль',
)
