from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from blog import schemas, models
from blog.database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()

    try: 
        yield db

    finally:
        db.close()


@app.post('/blog/')
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
