from fastapi import FastAPI

from router import router as app_router

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(app_router)




