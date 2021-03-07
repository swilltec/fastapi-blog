from fastapi import FastAPI, Depends, status, Response, HTTPException

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


@app.post('/blog/', status_code=status.HTTP_201_CREATED)
def create_blogpost(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog/')
def get_all_blogpost(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def get_blogpost_by_id(id, response:Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'blog post with this id {id} does not exist')
  
    return blog


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blogpost_by_id(id, request: schemas.Blog, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'blog post with this id {id} does not exist')
    blog.update(request)
    db.commit()
    
    return {'msg':'operation was sucessful'}


@app.delete('/blog/{id}', status_code=status.HTTP_200_OK)
def delete_blogpost_by_id(id, response:Response, db: Session = Depends(get_db)):
    blog =  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'blog post with this id {id} does not exist')

    blog.delete(synchronize_session=False)
    db.commit()
  
    return {'msg':'operation was sucessful'}