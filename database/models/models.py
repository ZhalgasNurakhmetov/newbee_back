from sqlalchemy import Column, String, ForeignKey, Boolean, Table, Integer
from database.database import Base

entrepreneur_category_association_table = Table('entrepreneur_category', Base.metadata,
                                                Column('entrepreneurId', ForeignKey('entrepreneurs.id'),
                                                       primary_key=True),
                                                Column('categoryId', ForeignKey('categories.id'), primary_key=True)
                                                )

client_category_association_table = Table('client_category', Base.metadata,
                                          Column('clientId', ForeignKey('clients.id'),
                                                 primary_key=True),
                                          Column('categoryId', ForeignKey('categories.id'), primary_key=True)
                                          )

course_category_association_table = Table('course_category', Base.metadata,
                                          Column('courseId', ForeignKey('courses.id'), primary_key=True),
                                          Column('categoryId', ForeignKey('categories.id'), primary_key=True)
                                          )

tutor_course_association_table = Table('tutor_course', Base.metadata,
                                       Column('tutorId', ForeignKey('tutors.id'), primary_key=True),
                                       Column('courseId', ForeignKey('courses.id'), primary_key=True)
                                       )

course_filial_association_table = Table('course_filial', Base.metadata,
                                        Column('courseId', ForeignKey('courses.id'), primary_key=True),
                                        Column('filialId', ForeignKey('filials.id'), primary_key=True)
                                        )

client_course_association_table = Table('client_course', Base.metadata,
                                        Column('clientId', ForeignKey('clients.id'), primary_key=True),
                                        Column('courseId', ForeignKey('courses.id'), primary_key=True)
                                        )


class EntrepreneurModel(Base):
    from sqlalchemy.orm import relationship, Session

    __tablename__ = 'entrepreneurs'

    id = Column(String, primary_key=True, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    title = Column(String, nullable=False)
    videoPath = Column(String, nullable=True)
    photoPath = Column(String, nullable=True)
    categories = relationship('CategoryModel', secondary=entrepreneur_category_association_table)
    tutors = relationship('TutorModel', back_populates='entrepreneur')
    courses = relationship('CourseModel', back_populates='entrepreneur')
    filials = relationship('FilialModel', back_populates='entrepreneur')
    feedbacks = relationship('FeedbackModel')
    role = Column(String, nullable=False, default='ENTREPRENEUR')

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    @staticmethod
    def get_by_username(username: str, db: Session):
        return db.query(EntrepreneurModel).filter(EntrepreneurModel.username == username).first()

    @staticmethod
    def get_by_id(_id: str, db: Session):
        return db.query(EntrepreneurModel).filter(EntrepreneurModel.id == _id).first()


class CategoryModel(Base):
    from sqlalchemy.orm import Session

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    groupc = Column(String, nullable=False)
    title = Column(String, nullable=False)

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    @staticmethod
    def get_by_id(_id: int, db: Session):
        return db.query(CategoryModel).filter(CategoryModel.id == _id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(CategoryModel).all()


class TutorModel(Base):
    from sqlalchemy.orm import relationship, Session

    __tablename__ = 'tutors'

    id = Column(String, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    birthDate = Column(String, nullable=False)
    photoPath = Column(String, nullable=True)
    experience = Column(String, nullable=False)
    description = Column(String, nullable=False)
    entrepreneurId = Column(String, ForeignKey('entrepreneurs.id'))
    entrepreneur = relationship('EntrepreneurModel', back_populates='tutors')
    courses = relationship('CourseModel', secondary=tutor_course_association_table, back_populates='tutors')
    feedbacks = relationship('FeedbackModel')

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    @staticmethod
    def get_by_id(_id: str, db: Session):
        return db.query(TutorModel).filter(TutorModel.id == _id).first()

    def delete_from_db(self, db: Session):
        db.delete(self)
        db.commit()

    @staticmethod
    def get_tutors_by_entrepreneur_id(_id: str, db: Session):
        return db.query(TutorModel).where(TutorModel.entrepreneurId == _id).all()


class FeedbackModel(Base):
    from sqlalchemy.orm import relationship, Session

    __tablename__ = 'feedbacks'

    id = Column(String, primary_key=True, unique=True)
    content = Column(String, nullable=False)
    clientId = Column(String, ForeignKey('clients.id'))
    client = relationship('ClientModel')
    entrepreneurId = Column(String, ForeignKey('entrepreneurs.id'), nullable=True)
    tutorId = Column(String, ForeignKey('tutors.id'), nullable=True)
    courseId = Column(String, ForeignKey('courses.id'), nullable=True)

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)


class CourseModel(Base):
    from sqlalchemy.orm import relationship, Session

    __tablename__ = 'courses'

    id = Column(String, primary_key=True, unique=True)
    title = Column(String, nullable=False)
    price = Column(String, nullable=False)
    description = Column(String, nullable=False)
    # syllabus
    videoPath = Column(String, nullable=True)
    photoPath = Column(String, nullable=True)
    isActive = Column(Boolean, nullable=False, default=True)
    finishedCount = Column(String, nullable=False, default=0)
    entrepreneurId = Column(String, ForeignKey('entrepreneurs.id'))
    entrepreneur = relationship('EntrepreneurModel', back_populates='courses')
    categories = relationship('CategoryModel', secondary=course_category_association_table)
    tutors = relationship('TutorModel', secondary=tutor_course_association_table, back_populates='courses')
    clients = relationship('ClientModel', secondary=client_course_association_table, back_populates='courses')
    filials = relationship('FilialModel', secondary=course_filial_association_table, back_populates='courses')
    feedbacks = relationship('FeedbackModel')

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    @staticmethod
    def get_by_id(_id: str, db: Session):
        return db.query(CourseModel).filter(CourseModel.id == _id).first()

    def delete_from_db(self, db: Session):
        db.delete(self)
        db.commit()

    @staticmethod
    def get_courses_by_entrepreneur_id(_id: str, db: Session):
        return db.query(CourseModel).where(CourseModel.entrepreneurId == _id).all()


class FilialModel(Base):
    from sqlalchemy.orm import relationship, Session

    __tablename__ = 'filials'

    id = Column(String, primary_key=True, unique=True)
    city = Column(String, nullable=False)
    address = Column(String, nullable=False)
    entrepreneurId = Column(String, ForeignKey('entrepreneurs.id'))
    entrepreneur = relationship('EntrepreneurModel', back_populates='filials')
    courses = relationship('CourseModel', secondary=course_filial_association_table, back_populates='filials')

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    @staticmethod
    def get_by_id(_id: str, db: Session):
        return db.query(FilialModel).filter(FilialModel.id == _id).first()

    def delete_from_db(self, db: Session):
        db.delete(self)
        db.commit()

    @staticmethod
    def get_filials_by_entrepreneur_id(_id: str, db: Session):
        return db.query(FilialModel).where(FilialModel.entrepreneurId == _id).all()


class ClientModel(Base):
    from sqlalchemy.orm import relationship, Session

    __tablename__ = 'clients'

    id = Column(String, primary_key=True, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    birthDate = Column(String, nullable=False)
    photoPath = Column(String, nullable=True)
    city = Column(String, nullable=False)
    courses = relationship('CourseModel', secondary=client_course_association_table, back_populates='clients')
    categories = relationship('CategoryModel', secondary=client_category_association_table)
    finishedIds = Column(String, nullable=True)
    role = Column(String, nullable=False, default='CLIENT')

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    @staticmethod
    def get_by_username(username: str, db: Session):
        return db.query(ClientModel).filter(ClientModel.username == username).first()

    @staticmethod
    def get_by_id(_id: str, db: Session):
        return db.query(ClientModel).filter(ClientModel.id == _id).first()
