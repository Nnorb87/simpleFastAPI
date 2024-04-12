from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", status_code = status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: Session = Depends(get_db)):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    pass

@app.post("/posts/", status_code = status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

@app.get("/posts/{post_id}", status_code = status.HTTP_200_OK)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post == None:
        raise HTTPException(status_code = 404, detail = "Post was not found")
    return post

@app.delete("/posts/{post_id}", status_code = status.HTTP_200_OK)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post == None:
        raise HTTPException(status_code = 404, detail = "Post was not found")
    db.delete(db_post)
    db.commit()


@app.get("/users/", status_code = status.HTTP_200_OK)
async def read_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user

@app.get("/users/{user_id}", status_code = status.HTTP_200_OK)
async def read_user(user_id: int,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user == None:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user