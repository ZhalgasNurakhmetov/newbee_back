from services.auth.auth_service import router as AuthServiceRouter
from services.entrepreneur.entrepreneur_service import router as EntrepreneurServiceRouter
from services.category.category_service import router as CategoryServiceRouter


def initialize_routes(app):
    app.include_router(AuthServiceRouter)
    app.include_router(EntrepreneurServiceRouter)
    app.include_router(CategoryServiceRouter)
