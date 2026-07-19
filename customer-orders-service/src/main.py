from fastapi import FastAPI

from src.api.orders import router as orders_router

app = FastAPI()
app.include_router(orders_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}