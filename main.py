from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database.database import Base, engine, categories
from routes.routes import initialize_routes

Base.metadata.create_all(engine, checkfirst=True)

# TODO uncomment before production

# with engine.connect() as con:
#     statement = text("""INSERT INTO categories (groupc, title) VALUES (:groupc, :title)""")
#     for category in categories:
#         con.execute(statement, **category)

app = FastAPI(title="Newbee server", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_routes(app)
