from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter


router = InferringRouter()


@cbv(router)
class ClientService:
    from database.schemas.schemas import ClientSchema, ClientCreateSchema
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from database.database import get_db
    from services.schemas.service_schemas import CategoryAddSchema
    from database.models.models import ClientModel
    from services.auth.auth_service import get_current_user

    @router.post('/api/client/register', response_model=ClientSchema)
    def register_client(self, client: ClientCreateSchema, db: Session = Depends(get_db)):
        from database.models.models import ClientModel, CategoryModel
        from error_handler.error_handler_service import user_already_exist_exception
        import uuid
        from services.auth.auth_service import pwd_context

        client.username = client.username.lower()
        if ClientModel.get_by_username(client.username, db):
            raise user_already_exist_exception
        category_ids = client.categories.copy()
        client.categories = []
        new_client_id = str(uuid.uuid4())
        client.password = pwd_context.hash(client.password)
        new_client = ClientModel(**client.dict(), id=new_client_id)
        new_client.categories = [CategoryModel.get_by_id(_id, db) for _id in category_ids]
        new_client.save_to_db(db)
        return new_client

    @router.get('/api/client/self', response_model=ClientSchema)
    def get_current_user(self, current_client: ClientSchema = Depends(get_current_user)):
        return current_client

    @router.post('/api/client/category/manage', response_model=ClientSchema)
    def manage_client_category(self, categories: CategoryAddSchema, current_client: ClientModel = Depends(get_current_user), db: Session = Depends(get_db)):
        from database.models.models import CategoryModel

        current_client.categories = [CategoryModel.get_by_id(_id, db) for _id in categories.ids]
        current_client.save_to_db(db)
        return current_client
