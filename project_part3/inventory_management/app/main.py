from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import Inventory, Base
from schemas import InventoryBase, InventoryCreate, InventoryInDB, InventoryUpdate
from db import engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Endpoint to create a new Inventory
@app.post("/inventory/", response_model=InventoryInDB)
def create_inventory_item(inventory: InventoryCreate, db: Session = Depends(get_db)):
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

# Endpoint to retrieve inventory by ID
@app.get("/inventory/{item_id}", response_model=InventoryInDB)
def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    db_inventory = db.query(Inventory).filter(Inventory.id == item_id).first()
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_inventory

# Endpoint to retrieve all inventory items
@app.get("/inventory/", response_model=List[InventoryInDB])
def get_all_inventory_items(db: Session = Depends(get_db)):
    return db.query(Inventory).all()

# Endpoint to update a inventory item by ID
@app.put("/inventory/{item_id}", response_model=InventoryInDB)
def update_inventory_item(item_id: int, inventory: InventoryUpdate, db: Session = Depends(get_db)):
    db_inventory = db.query(Inventory).filter(Inventory.id == item_id).first()
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory Item is not found")
    for field, value in inventory.dict().items():
        setattr(db_inventory, field, value)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

# Endpoint to delete an inventory item by ID
@app.delete("/inventory/{item_id}", response_model=InventoryInDB)
def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    db_inventory = db.query(Inventory).filter(Inventory.id == item_id).first()
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory Item is not found")
    db.delete(db_inventory)
    db.commit()
    return db_inventory
