from fastapi import FastAPI
from api.storage_api import router as storage_router

app = FastAPI()

# middleware 설정
# app.add_middleware(
#     # CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# router 설정
app.include_router(storage_router, prefix="/api/v1", tags=["storage"])

@app.get("/")
async def read_root():
    return {"message": "Hello World"}