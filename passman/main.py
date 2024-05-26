from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from passman.models.user import User
from passman.core.database import engine
from passman.api.userApi import router as user_router
from passman.api.passwordApi import router as password_router


app = FastAPI()

app.include_router(user_router, prefix='/api/user')
app.include_router(password_router, prefix='/api/password')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
def start():
    User.metadata.create_all(bind=engine)
