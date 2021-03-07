from typing import List

from fastapi import (FastAPI, Depends, status, Response,
                     HTTPException, APIRouter)

from sqlalchemy.orm import Session

from .. import schemas, database, models

from ..hashing import get_password_hash

router = APIRouter()

@router.post('/user/', response_model = schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    hashed_password = get_password_hash(request.password)

    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password,
        )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["users"])
def get_user_by_id(id: int, response:Response, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'User with this id {id} does not exist')
  
    return user