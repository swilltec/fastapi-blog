from typing import List

from fastapi import (Depends, status, Response, APIRouter)

from sqlalchemy.orm import Session

from .. import schemas, database, models
from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blogpost_route(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.create(request, db)


@router.get('/', response_model=List[schemas.ShowBlog])
def all_post_route(db: Session = Depends(database.get_db)):
    return blog.get_all(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def blogpost_detail_route(id, response:Response, db: Session = Depends(database.get_db)):
    return blog.get_detail(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blogpost_by_id(id, request: schemas.Blog, db: Session=Depends(database.get_db)):
    return blog.update(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_blogpost_by_id(id, response:Response, db: Session = Depends(database.get_db)):  
    return blog.delete(id, db)


