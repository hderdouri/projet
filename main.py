

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Item
from datetime import datetime

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
engine = create_engine('sqlite:///database.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create user
@app.post("/signup")
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Authenticate user and return token
@app.post("/signin")
def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"access_token": user.id, "token_type": "bearer"}


# Logout user (not strictly necessary since this is a token-based authentication system)
@app.post("/logout")
def logout():
    # Remove token from database or blacklist it to invalidate it
    return {"message": "Logged out"}


# Get one item
@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Get list of items with optional filtering
@app.get("/items")
def read_items(created_at__gte: datetime, created_at__lte: datetime, db: Session = Depends(get_db)):
    filters = []
    if created_at__gte:
        filters.append(Item.created_at >= created_at__gte)
    if created_at__lte:
        filters.append(Item.created_at <= created_at__lte)
    if filters:
        items = db.query(Item).filter(*filters).all()
    else:
        items = db.query(Item).all()
    return items


# Create new item
@app.post("/items")
def create_item(name: str, description: str, db: Session = Depends(get_db)):
    item = Item(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# Update item
@app.put("/items/{item_id}")
def update_item(item_id: int, name: str = None, description: str = None, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if name:
        item.name = name
    if description:
        item.description = description
    db.commit()
    db.refresh(item)
    return item


# Delete item
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}
