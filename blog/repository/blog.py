
from .. import models

from fastapi import status, HTTPException


def get_all(db):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request, db):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=1
        )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_detail(id, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'blog post with this id {id} does not exist')
    return blog


def update(id, request, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'blog post with this id {id} does not exist')
    blog.update(request)
    db.commit()
    return {'detail': 'operation was successfully'}


def delete(id, db):
    blog =  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'blog post with this id {id} does not exist')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'detail': 'operation was successfully'}