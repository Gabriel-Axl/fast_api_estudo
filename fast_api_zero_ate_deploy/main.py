from fastapi import FastAPI, APIRouter
from produtos.routers import router
from banco.database import Base, engine
from produtos.model import Produto

Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def home():
    return {"Hello": "World"}

app.include_router(router, tags=["produtos"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    