import fastapi
import uvicorn as uvicorn

from routes.authors import authors
from routes.books import books
from routes.contracts import contracts
from routes.customers import customers
from routes.orders import orders
from routes.users import users

app = fastapi.FastAPI(title='Лабораторная работа № 4-5')

app.include_router(users, prefix='/users', tags=['Users'])
app.include_router(books, prefix='/books', tags=['Books'])
app.include_router(customers, prefix='/customers', tags=['Customers'])
app.include_router(orders, prefix='/orders', tags=['Orders'])
app.include_router(contracts, prefix='/contracts', tags=['Contracts'])
app.include_router(authors, prefix='/authors', tags=['Authors'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=5000, reload=True)
