from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from fastapi_login.users.router import router
    app.include_router(router, prefix='/users')

    @app.get("/")
    async def root():
        return {"msg": "Hello World"}

    return app
