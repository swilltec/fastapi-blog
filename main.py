from fastapi import FastAPI


from blog.database import engine

from blog.routers import blog, users
from blog import models

app = FastAPI()
app.include_router(blog.router)
app.include_router(users.router)

models.Base.metadata.create_all(engine)



