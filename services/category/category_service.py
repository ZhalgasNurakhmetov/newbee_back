from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter


router = InferringRouter()


@cbv(router)
class CategoryService:
    from database.schemas.schemas import CategoryBaseSchema
    from typing import List
    from sqlalchemy.orm import Session
    from fastapi import Depends
    from database.database import get_db

    @router.get('/api/category/list', response_model=List[CategoryBaseSchema])
    def get_category_list(self, db: Session = Depends(get_db)):
        from database.models.models import CategoryModel

        return CategoryModel.get_all(db)
