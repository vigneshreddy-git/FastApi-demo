from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session
app=FastAPI()
#cors error is a security feature implemented by web browsers to prevent malicious websites from making requests to a different domain than the one that served the web page. It stands for Cross-Origin Resource Sharing. When a web page makes a request to a different domain, the browser checks if the server allows it by looking for specific headers in the response. If the headers are not present or do not allow the request, the browser blocks the request and raises a CORS error.
#the frontend runs on 3000 port and the backend runs on 8000 port. so we need to allow the forntend to access the backend. for that we need to install the fastapi-cors package and then we need to add the middleware to the app.
# here we are allowing the frontend to access the backend by adding the middleware to the app. we are allowing all the origins to access the backend. but in production we should allow only the specific origins to access the backend.
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["*"],
    allow_origins=["http://localhost:3000"],
    #allow_credentials=True,
    allow_methods=["*"],
    #allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")

def greet():
    return "Hello, welcome to the telusko"



products=[
    Product(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
    Product(id=2, name="Mouse", description="A wireless mouse", price=29.99, quantity=50),
    Product(id=3, name="Keyboard", description="A mechanical keyboard", price=149.99, quantity=25)
]

# def get_db():
#     db=session()
#     yield db
#     db.close()
# ^ yeild db may cause error but we should close the db connnection after the request is completed. so we use the below method.

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()



def init_db():
    db=session()
    count=db.query(database_models.Product).count()
    if count==0:
        for product in products:
            #we should add the product of database_models instead of models.py.beacuse models.py is a pydnatic model.we are adding to the database so we created the database_models.py file which is a sqlalchemy model.
            # for that we should use the model_dump() method of pydantic model to convert it into a dictionary and then we can use that dictionary to create an instance of the sqlalchemy model. ** unpacks the dictionary into keyword arguments for the Product constructor.
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
init_db()

@app.get("/products")
# def get_all_products():
#     #db connecion
#     db= session()
#     #db query
#     db.query()
#     return products

# ^ instead of again using the session() method to create a new database session , we can make the session itself asks us the session by followong method.
def get_all_products(db: Session=Depends (get_db)): #injecting the depenedency's
    db_products=db.query(database_models.Product).all()
    return db_products


@app.get("/product/{id}")

def get_product_by_id(id: int,db: Session=Depends(get_db)):
    #db_products=db.query(database_models.Product).all() #for all products but we want only only product that matches the id
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first() # filter may result in multiple products but we need only one  that matches to us. so we ask for the first one.
    if db_product:
        return db_product
    
    return "product not found."

@app.post("/products")
#this is for the list of products not the database
# def add_product(product: Product):
#     products.append(product)
#     return product
#now this is for the database
def add_product(product: Product,db: Session=Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    #after changing anything in the database we should commit the changes to the database.
    db.commit()
    return product

@app.put("/products/{id}")

#for the list of products not the database


# def update_product(id: int,product: Product):
#     for i in range(len(products)):
#         if products[i].id==id:
#             products[i]=product
#             return "product updated successfully."
#     return "product not found."

# for the database
def update_product(id:int,product:Product,db: Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return "product updated successfully."
    return "product not found."



@app.delete("/products/{id}")
#for the list of products not the database


# def delete_product(id: int):
#     for i in range(len(products)):
#         if products[i].id==id:
#             del products[i]
#             return "deleted product succesfully."
#     return "product not found."

# for the database
def delete_product(id:int,db: Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "deleted product succesfully."
    else:
        return "product not found."


