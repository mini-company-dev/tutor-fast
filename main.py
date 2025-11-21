from fastapi import FastAPI

from app.api.routes.grammer_test_route import router as garammerTestRouter
from app.api.routes.ai_test_route import router as aiTestRouter

from app.exceptions.register import setup_exception_handlers
from auth.auth_route import router as userRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000", "https://easyfunspeak.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_exception_handlers(app)

app.include_router(garammerTestRouter)
app.include_router(aiTestRouter)
app.include_router(userRouter)
