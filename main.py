from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from database import engine, get_db
from routers import post, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World this is ok "}


@app.get('/alchemy')
def alchemy(db: Session = Depends(get_db)):
    return db.query(models.post).all()


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


