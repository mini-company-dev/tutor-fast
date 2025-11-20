from fastapi import FastAPI

from app.api.routes.grammer_test_route import router as garammerTestRouter
from app.api.routes.ai_test_route import router as aiTestRouter
from auth.auth_route import router as userRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000", "https://easyfunspeak.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 origin
    allow_credentials=True,  # 쿠키/인증 허용
    allow_methods=["*"],  # GET, POST, DELETE 등 모두 허용
    allow_headers=["*"],  # 헤더 전체 허용
)


app.include_router(garammerTestRouter)
app.include_router(aiTestRouter)
app.include_router(userRouter)
