from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class EntrepreneurService:
    from database.schemas.schemas import EntrepreneurSchema, EntrepreneurCreateSchema, FilialBaseSchema, FilialSchema, TutorSchema, TutorCreateSchema, CourseSchema, CourseCreateSchema
    from sqlalchemy.orm import Session
    from fastapi import Depends
    from database.database import get_db
    from database.models.models import EntrepreneurModel
    from services.entrepreneur.schemas.entrepreneur_schemas import CategoryAddSchema, EntrepreneurAddPhotoSchema
    from services.auth.auth_service import get_current_user
    from typing import List

    @router.post('/api/entrepreneur/register', response_model=EntrepreneurSchema)
    def register_entrepreneur(self, entrepreneur: EntrepreneurCreateSchema, db: Session = Depends(get_db)):
        from database.models.models import EntrepreneurModel
        from error_handler.error_handler_service import user_already_exist_exception
        import uuid
        from services.auth.auth_service import pwd_context
        from database.models.models import CategoryModel

        entrepreneur.username = entrepreneur.username.lower()
        if EntrepreneurModel.get_by_username(entrepreneur.username, db):
            raise user_already_exist_exception
        category_ids = entrepreneur.categories.copy()
        entrepreneur.categories = []
        new_entrepreneur_id = str(uuid.uuid4())
        entrepreneur.password = pwd_context.hash(entrepreneur.password)
        new_entrepreneur = EntrepreneurModel(**entrepreneur.dict(), id=new_entrepreneur_id)
        new_entrepreneur.categories = [CategoryModel.get_by_id(_id, db) for _id in category_ids]
        new_entrepreneur.save_to_db(db)
        return new_entrepreneur

    @router.get('/api/entrepreneur/self', response_model=EntrepreneurSchema)
    def get_current_user(self, current_entrepreneur: EntrepreneurSchema = Depends(get_current_user)):
        return current_entrepreneur

    @router.post('/api/entrepreneur/category/manage', response_model=EntrepreneurSchema)
    def manage_category(self, categories: CategoryAddSchema, current_entrepreneur: EntrepreneurModel = Depends(get_current_user), db: Session = Depends(get_db)):
        from database.models.models import CategoryModel

        current_entrepreneur.categories = [CategoryModel.get_by_id(_id, db) for _id in categories.ids]
        current_entrepreneur.save_to_db(db)
        return current_entrepreneur

    @router.post('/api/entrepreneur/photo-video/add', response_model=EntrepreneurSchema)
    def add_photo_and_video(self, data: EntrepreneurAddPhotoSchema, current_entrepreneur: EntrepreneurModel = Depends(get_current_user), db: Session = Depends(get_db)):
        import json

        if len(data.photoList) > 0:
            current_entrepreneur.photoPath = json.dumps(data.photoList)
        else:
            current_entrepreneur.photoPath = None
        current_entrepreneur.videoPath = data.video
        current_entrepreneur.save_to_db(db)
        return current_entrepreneur

    @router.post('/api/entrepreneur/filial/add', response_model=FilialSchema)
    def add_filial(self, filial: FilialBaseSchema, current_entrepreneur: EntrepreneurModel = Depends(get_current_user), db: Session = Depends(get_db)):
        import uuid
        from database.models.models import FilialModel

        new_filial_id = str(uuid.uuid4())
        new_filial = FilialModel(**filial.dict(), id=new_filial_id, entrepreneurId=current_entrepreneur.id)
        new_filial.save_to_db(db)
        return new_filial

    @router.delete('/api/entrepreneur/filial/remove/{filial_id}', response_model=FilialSchema)
    def remove_filial(self, filial_id: str, current_entrepreneur: EntrepreneurModel = Depends(get_current_user), db: Session = Depends(get_db)):
        from error_handler.error_handler_service import unauthorized_exception
        from database.models.models import FilialModel

        if not current_entrepreneur:
            raise unauthorized_exception
        filial: FilialModel = FilialModel.get_by_id(filial_id, db)
        filial.delete_from_db(db)
        return filial

    @router.get('/api/entrepreneur/filials', response_model=List[FilialSchema])
    def get_entrepreneur_filials(self, current_entrepreneur: EntrepreneurModel = Depends(get_current_user), db: Session = Depends(get_db)):
        from database.models.models import FilialModel

        return FilialModel.get_filials_by_entrepreneur_id(current_entrepreneur.id, db)

    @router.post('/api/entrepreneur/tutor/add', response_model=TutorSchema)
    def add_tutor(self, tutor: TutorCreateSchema, current_entrepreneur: EntrepreneurModel = Depends(get_current_user), db: Session = Depends(get_db)):
        import uuid
        from database.models.models import TutorModel, CourseModel

        new_tutor_id = str(uuid.uuid4())
        course_ids = tutor.courses.copy()
        tutor.courses = []
        new_tutor = TutorModel(**tutor.dict(), id=new_tutor_id, entrepreneurId=current_entrepreneur.id)
        new_tutor.courses = [CourseModel.get_by_id(_id, db) for _id in course_ids]
        new_tutor.save_to_db(db)
        return new_tutor

    @router.delete('/api/entrepreneur/tutor/remove/{tutor_id}', response_model=TutorSchema)
    def remove_tutor(self, tutor_id: str, current_entrepreneur: EntrepreneurModel = Depends(get_current_user), db: Session = Depends(get_db)):
        from error_handler.error_handler_service import unauthorized_exception
        from database.models.models import TutorModel

        if not current_entrepreneur:
            raise unauthorized_exception
        tutor: TutorModel = TutorModel.get_by_id(tutor_id, db)
        tutor.delete_from_db(db)
        return tutor

    @router.get('/api/entrepreneur/tutors', response_model=List[TutorSchema])
    def get_entrepreneur_tutors(self, current_entrepreneur: EntrepreneurModel = Depends(get_current_user), db: Session = Depends(get_db)):
        from database.models.models import TutorModel

        return TutorModel.get_tutors_by_entrepreneur_id(current_entrepreneur.id, db)

    @router.post('/api/entrepreneur/course/add', response_model=CourseSchema)
    def add_course(self, course: CourseCreateSchema, current_entrepreneur: EntrepreneurModel = Depends(get_current_user), db: Session = Depends(get_db)):
        import uuid
        import json
        from database.models.models import CourseModel, CategoryModel, TutorModel, FilialModel

        category_ids = course.categories
        tutor_ids = course.tutors
        filial_ids = course.filials

        course.categories = []
        course.tutors = []
        course.filials = []
        if len(course.photoPath) > 0:
            course.photoPath = json.dumps(course.photoPath)
        else:
            course.photoPath = None
        new_course_id = str(uuid.uuid4())
        new_course = CourseModel(**course.dict(), id=new_course_id, entrepreneurId=current_entrepreneur.id)
        new_course.categories = [CategoryModel.get_by_id(_id, db) for _id in category_ids]
        new_course.tutors = [TutorModel.get_by_id(_id, db) for _id in tutor_ids]
        new_course.filials = [FilialModel.get_by_id(_id, db) for _id in filial_ids]
        new_course.save_to_db(db)
        return new_course

    @router.delete('/api/entrepreneur/course/remove/{course_id}', response_model=CourseSchema)
    def remove_course(self, course_id: str, current_entrepreneur: EntrepreneurModel = Depends(get_current_user), db: Session = Depends(get_db)):
        from database.models.models import CourseModel
        from error_handler.error_handler_service import unauthorized_exception

        if not current_entrepreneur:
            raise unauthorized_exception
        course: CourseModel = CourseModel.get_by_id(course_id, db)
        course.delete_from_db(db)
        return course

    @router.get('/api/entrepreneur/courses', response_model=List[CourseSchema])
    def get_entrepreneur_courses(self, current_entrepreneur: EntrepreneurModel = Depends(get_current_user), db: Session = Depends(get_db)):
        from database.models.models import CourseModel

        return CourseModel.get_courses_by_entrepreneur_id(current_entrepreneur.id, db)
