from typing import List

from fastapi import (FastAPI, Depends, status, Response,
                     HTTPException, APIRouter)

from sqlalchemy.orm import Session

from .. import schemas, database, models

router = APIRouter()

@router.post('/blog/', status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create_blogpost(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=1, )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/blog/', response_model=List[schemas.ShowBlog], tags=["blogs"])
def get_all_blogpost(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["blogs"])
def get_blogpost_by_id(id, response:Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'blog post with this id {id} does not exist')
  
    return blog


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update_blogpost_by_id(id, request: schemas.Blog, db: Session=Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'blog post with this id {id} does not exist')
    blog.update(request)
    db.commit()

    return {'msg':'operation was sucessful'}


@router.delete('/blog/{id}', status_code=status.HTTP_200_OK, tags=["blogs"])
def delete_blogpost_by_id(id, response:Response, db: Session = Depends(database.get_db)):
    blog =  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'blog post with this id {id} does not exist')

    blog.delete(synchronize_session=False)
    db.commit()
  
    return {'msg':'operation was sucessful'}


