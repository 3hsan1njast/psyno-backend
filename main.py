from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, status
from sqlmodel import Session, select
from database import get_session, create_db_and_tables
from models import Post, User
from auth import get_user, get_current_user, authenticate_user, create_access_token, get_password_hash
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

class LoginData(BaseModel):
    username: str
    password: str

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/register")
async def register(user: User, db: Session = Depends(get_session)):
    if get_user(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    user.hashed_password = get_password_hash(user.hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully"}

@app.post("/login")
async def login(form_data: LoginData, db: Session = Depends(get_session)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get('/posts', response_model=List[Post])
async def get_posts(session: Session = Depends(get_session)):
    return session.exec(select(Post)).all()

@app.get('/posts/{post_id}', response_model=Post)
async def get_post(post_id: str, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post('/posts', response_model=Post)
async def new_post(post: Post, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    post.user_id = current_user.id
    post.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@app.put('/posts/{post_id}', response_model=Post)
async def edit_post(post_id: str, post: Post, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")
    post_data = post.model_dump(exclude_unset=True)
    for key, value in post_data.items():
        if key != "user_id":
            setattr(db_post, key, value)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@app.delete('/posts/{post_id}', response_model=Post)
async def delete_post(post_id: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    session.delete(post)
    session.commit()
    return post

if __name__ == "__main__":
    uvicorn.run(app, port=8000)