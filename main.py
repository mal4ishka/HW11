from fastapi import FastAPI
from address_book.routes import contacts

app = FastAPI()
app.include_router(contacts.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}