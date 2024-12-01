from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from pages.router import router as pages_router

app = FastAPI(
    title="Рабочее место Энкост"
)



app.mount('/static', StaticFiles(directory='static'), name="static")
app.include_router(pages_router)

origins = ["http://localhost:3000",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"], )
