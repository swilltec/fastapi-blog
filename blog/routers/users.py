from typing import List

from fastapi import (Depends, status, Response,
                     HTTPException, APIRouter)

from sqlalchemy.orm import Session

from .. import schemas, database, models
from ..repository import users

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post('/', response_model = schemas.ShowUser)
def create_route(request: schemas.User, db: Session = Depends(database.get_db)):
    return users.create(request, db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user_route(id: int, response:Response, db: Session = Depends(database.get_db)):
    return users.get_user(id, db)