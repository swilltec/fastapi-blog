
from fastapi import  status, HTTPException

from .. import models
from ..hashing import get_password_hash


def create(request, db):
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


def get_user(id, db):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'User with this id {id} does not exist')
  
    return user