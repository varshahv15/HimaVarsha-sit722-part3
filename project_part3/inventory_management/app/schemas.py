from pydantic import BaseModel

class InventoryBase(BaseModel):
    name: str
    description: str
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(InventoryBase):
    pass

class InventoryInDB(InventoryBase):
    id: int

    class Config:
        orm_mode = True
