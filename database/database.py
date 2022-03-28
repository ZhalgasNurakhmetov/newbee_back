from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.config import config

SQLALCHEMY_DATABASE_URL = config.SQLALCHEMY_DATABASE_URI
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

categories = [
    {'groupc': 'Образование', 'title': 'IT'},
    {'groupc': 'Образование', 'title': 'Языки'},
    {'groupc': 'Образование', 'title': 'Личностный рост и психология'},
    {'groupc': 'Образование',
     'title': 'Исследования в области управления, экономические и бизнес-исследования'},
    {'groupc': 'Образование', 'title': 'Руководство и лидерство'},
    {'groupc': 'Образование', 'title': 'Менеджмент'},
    {'groupc': 'Образование', 'title': 'Финансовая грамотность'},
    {'groupc': 'Образование', 'title': 'Бухгалтерский учет'},
    {'groupc': 'Образование', 'title': '1С'},
    {'groupc': 'Образование', 'title': 'Бизнес менеджмент'},
    {'groupc': 'Образование', 'title': 'Бизнес аналитика'},
    {'groupc': 'Образование', 'title': 'Деловое администрирование'},
    {'groupc': 'Образование', 'title': 'Инвестированию'},
    {'groupc': 'Образование', 'title': 'Курсы для школьников'},
    {'groupc': 'Образование', 'title': 'Дошкольная подготовка'},
    {'groupc': 'Образование', 'title': 'Подготовка к ЕНТ'},
    {'groupc': 'Образование', 'title': 'Подготовка к поступлению в зарубежные университеты'},
    {'groupc': 'Образование', 'title': 'IELTS / TOEFL'},
    {'groupc': 'Образование', 'title': 'Курсы с репетитором по предметам'},
    {'groupc': 'Образование', 'title': 'Фотошоп'},
    {'groupc': 'Образование', 'title': 'Видео монтаж'},
    {'groupc': 'Образование', 'title': 'UI Дизайнер'},
    {'groupc': 'Образование', 'title': 'Motion design'},
    {'groupc': 'Здоровье и красота', 'title': 'Маникюр'},
    {'groupc': 'Здоровье и красота', 'title': 'Педикюр'},
    {'groupc': 'Здоровье и красота', 'title': 'Сам себе визажист'},
    {'groupc': 'Здоровье и красота', 'title': 'Профессиональный курс визажа'},
    {'groupc': 'Здоровье и красота', 'title': 'Шугаринг'},
    {'groupc': 'Здоровье и красота', 'title': 'Бровивист'},
    {'groupc': 'Здоровье и красота', 'title': 'Наращивание ресниц'},
    {'groupc': 'Здоровье и красота', 'title': 'Прически и укладки'},
    {'groupc': 'Здоровье и красота', 'title': 'Перманентный макияж'},
    {'groupc': 'Здоровье и красота', 'title': 'Микроблейдинг бровей, век и губ'},
    {'groupc': 'Здоровье и красота', 'title': 'Колористы'},
    {'groupc': 'Здоровье и красота', 'title': 'Кометология'},
    {'groupc': 'CMM', 'title': 'SMM-специалист с нуля'},
    {'groupc': 'CMM', 'title': 'Таргетолог / Маркетолог с нуля'},
    {'groupc': 'CMM', 'title': 'Креативный копирайтинг для соцсетей'},
    {'groupc': 'CMM', 'title': 'Influence / messenger - Маркетинг'},
    {'groupc': 'CMM', 'title': 'Контент - мейкер'},
    {'groupc': 'CMM', 'title': 'Курсы мобилографии'},
    {'groupc': 'Спорт', 'title': 'Сертифицированный тренер'},
    {'groupc': 'Спорт',
     'title': 'Марафоны - Похудения, набора массы, улучшения выносливости , спорта в привычку'},
    {'groupc': 'Спорт', 'title': 'Индивидуальные тренировки (при фитнесе)'},
    {'groupc': 'Спорт', 'title': 'Правильное питание'},
    {'groupc': 'Творчество', 'title': 'Игра на инструментах'},
    {'groupc': 'Творчество', 'title': 'Вокал'},
    {'groupc': 'Творчество', 'title': 'Звукорежиссер с нуля'},
    {'groupc': 'Творчество', 'title': 'Аудио дизайн с нуля'},
    {'groupc': 'Творчество',
     'title': 'Создание битов, музыки, по программам (Steinberg Cubase, Adobe audition, FL studio etc.)'},
    {'groupc': 'Творчество', 'title': 'Танцы'},
    {'groupc': 'Творчество', 'title': 'Курсы кройки и шитья'},
    {'groupc': 'Творчество', 'title': 'Художественные курсы'},
    {'groupc': 'Творчество', 'title': 'Бисероплетение'},
    {'groupc': 'Кулинария', 'title': 'Кондитер'},
    {'groupc': 'Кулинария', 'title': 'Курс кулинарии'},
    {'groupc': 'Кулинария', 'title': 'Курс по готовке изысканных блюд'},
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
