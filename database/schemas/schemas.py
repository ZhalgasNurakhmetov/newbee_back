from typing import List, Optional

from pydantic import BaseModel


class CategoryBaseSchema(BaseModel):
    id: str
    title: str

    class Config:
        orm_mode = True


class EntrepreneurDependencySchema(BaseModel):
    id: str
    username: str
    title: str
    videoPath: Optional[str] = None
    photoPath: Optional[str] = None

    class Config:
        orm_mode = True


class FilialDependencySchema(BaseModel):
    id: str
    city: str
    address: str
    entrepreneur: EntrepreneurDependencySchema

    class Config:
        orm_mode = True


class TutorDependencySchema(BaseModel):
    id: str
    name: str
    birthDate: str
    photoPath: Optional[str]
    experience: str
    description: str
    entrepreneur: EntrepreneurDependencySchema

    class Config:
        orm_mode = True


class CourseDependencySchema(BaseModel):
    id: str
    title: str
    price: str
    description: str
    videoPath: Optional[str]
    photoPath: Optional[str]
    isActive: bool
    finishedCount: str
    entrepreneur: EntrepreneurDependencySchema
    categories: List[CategoryBaseSchema] = []
    filials: List[FilialDependencySchema] = []

    class Config:
        orm_mode = True


class ClientDependencySchema(BaseModel):
    id: str
    username: str
    name: str
    birthDate: str
    city: str
    photoPath: str

    class Config:
        orm_mode = True


class FeedbackBaseSchema(BaseModel):
    content: str
    entrepreneurId: Optional[str]
    tutorId: Optional[str]
    courseId: Optional[str]


class FeedbackCreateSchema(FeedbackBaseSchema):
    clientId: str


class FeedbackSchema(FeedbackBaseSchema):
    id: str
    client: ClientDependencySchema

    class Config:
        orm_mode = True


class EntrepreneurBaseSchema(BaseModel):
    username: str
    title: str
    categories: List[CategoryBaseSchema] = []
    filials: List[FilialDependencySchema] = []
    role: str


class EntrepreneurCreateSchema(EntrepreneurBaseSchema):
    password: str


class EntrepreneurSchema(EntrepreneurBaseSchema):
    id: str
    videoPath: Optional[str] = None
    photoPath: Optional[str] = None
    tutors: List[TutorDependencySchema] = []
    courses: List[CourseDependencySchema] = []
    feedbacks: List[FeedbackSchema] = []

    class Config:
        orm_mode = True


class TutorBaseSchema(BaseModel):
    name: str
    birthDate: str
    photoPath: Optional[str]
    experience: str
    description: str
    courses: Optional[List[CourseDependencySchema]] = []


class TutorCreateSchema(TutorBaseSchema):
    entrepreneurId: str


class TutorSchema(TutorBaseSchema):
    id: str
    feedbacks: List[FeedbackSchema] = []
    entrepreneur: EntrepreneurDependencySchema

    class Config:
        orm_mode = True


class CourseBaseSchema(BaseModel):
    title: str
    price: str
    description: str
    videoPath: Optional[str]
    photoPath: Optional[str]
    categories: List[CategoryBaseSchema] = []
    tutors: List[TutorDependencySchema] = []
    filials: List[FilialDependencySchema] = []


class CourseCreateSchema(CourseBaseSchema):
    entrepreneurId: str


class CourseSchema(CourseBaseSchema):
    id: str
    feedbacks: List[FeedbackSchema] = []
    isActive: bool
    finishedCount: str
    entrepreneur: EntrepreneurDependencySchema

    class Config:
        orm_mode = True


class ClientBaseSchema(BaseModel):
    username: str
    name: str
    birthDate: str
    city: str
    role: str


class ClientCreateSchema(ClientBaseSchema):
    password: str


class ClientSchema(ClientBaseSchema):
    id: str
    photoPath: str
    courses: List[CourseDependencySchema]
    categories: List[CategoryBaseSchema]
    finishedCount: str

    class Config:
        orm_mode = True


class FilialBaseSchema(BaseModel):
    city: str
    address: str


class FilialCreateSchema(FilialBaseSchema):
    entrepreneurId: str


class FilialSchema(FilialBaseSchema):
    id: str
    entrepreneur: EntrepreneurDependencySchema
    courses: List[CourseDependencySchema]

    class Config:
        orm_mode = True
