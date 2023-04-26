from typing import List
from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud, models, schemas, session
import main

from .pantry import your_pantries

from utils import utils
from database import SessionLocal, engine


from starlette.responses import RedirectResponse

from database import get_db

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR,'templates')))

router = APIRouter()

@router.get("/manager-inventories", response_class=HTMLResponse, tags=["Inventory Item"])
def manager_inventories(request: Request, db: Session = Depends(get_db)):
    items = []
    pantries = your_pantries(db)
    print(pantries)
    for i in pantries:
        inventory_items = crud.get_inventory_by_pantryID(db, i.id)
        items += inventory_items

    print(items)
    data = []
    item_summary = []
    for i in items:
        item = crud.get_inventoryItem_by_id(db, i.item_id)
        pantry = crud.get_pantry_by_id(db, i.pantry_id)
        data.append([pantry.name, item.item_type, item.quantity, item.expiration_date, item.summary])
        item_summary.append(item.summary)
    print(data)
    return templates.TemplateResponse('manager-inventories.html',{'request': request,
                                                                  'data': data,
                                                                  'items': item_summary})

@router.post("/add_item", response_class=HTMLResponse, tags=["Item Inventory"])
def add_item(db: Session = Depends(get_db), pantry: str = Form(), item_type: str = Form(), quantity: int = Form(), expiration_date: str = Form(), summary: str = Form()):
    rtn = crud.create_inventoryItem(db=db, inventoryItem=schemas.InventoryItemCreate(item_type = item_type, 
                                                                                     quantity=quantity, 
                                                                                     expiration_date=expiration_date, 
                                                                                     summary=summary))
    print(rtn)
    if rtn is None:
        raise HTTPException(status_code=404, detail="Item could not be created")
    pantry_id = crud.get_pantryID_by_name(db, pantry)
    print(pantry_id)
    rtn = crud.add_item_to_pantry(db=db, item_id=rtn.id, pantry_id=pantry_id[0])
    print(rtn)
    if rtn is None:
        raise HTTPException(status_code=404, detail="Inventory item could not be added")
    return RedirectResponse("/manager-inventories", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/remove_item", response_class=HTMLResponse, tags=["Item Inventory"])
def remove_item(db: Session = Depends(get_db), item_summary: str = Form(), quantity: int = Form()):
    print(item_summary)
    item = crud.get_inventoryItem_by_summary(db, item_summary)
    print(item)
    item_id = item.id
    pantry_id = crud.get_inventory_pantryID_by_itemID(db, item_id)
    if quantity == item.quantity:
        rtn = crud.remove_item_from_inventory(db=db, pantry_id=pantry_id, item_id=item_id)
        if rtn is None:
            raise HTTPException(status_code=404, detail="Inventory item could not be removed from pantry")
    elif quantity < item.quantity:
        crud.update_inventoryItem_quantity(db, pantry_id, item_id, quantity, False)
    elif quantity > item.quantity:
        raise HTTPException(status_code=404, detail="Not enough quantity in inventory")
    return RedirectResponse("/manager-inventories", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/inventoryItem/", response_model=schemas.InventoryItem, tags=["Inventory Item"])
def create_inventory_item(inventoryItem: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    return crud.create_inventoryItem(db=db, inventoryItem=inventoryItem) #TODO: DEBUG

@router.get("/inventoryItem/{item_id}", response_model=schemas.InventoryItem, tags=["Inventory Item"])
def read_inventoryItem(item_id: int, db: Session = Depends(get_db)):
    db_inventoryItem= crud.get_inventoryItem_by_id(db, inventoryItem_id=item_id)
    if db_inventoryItem is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_inventoryItem

@router.get("/inventoryItem_by_Pantry/{pantry_id}", response_model=List[schemas.InventoryItem], tags=["Inventory Item"])
def read_inventoryItem_by_pantryID(pantry_id: int, db: Session = Depends(get_db)):

    inventory = crud.get_inventory_by_pantryID(db, id=pantry_id)
    # if inventory is None:
    #     raise HTTPException(status_code=404, detail="Pantry inventory is empty")

    items = []
    for pair in inventory:
        item_id = pair.item_id
        items.append(crud.get_inventoryItem_by_id(db, inventoryItem_id=item_id))

    return items


@router.get("/inventoryItems/", response_model=List[schemas.InventoryItem], tags=["Inventory Item"])
def read_inventoryItems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    inventoryItems = crud.get_inventoryItems(db, skip=skip, limit=limit)
    return inventoryItems

@router.post("/inventoryRemove/{pantry_id}/{item_id}", tags=["Inventory Item"])
def manager_remove_inventory_item(pantry_id: int, item_id: int, db: Session = Depends(get_db)):
    rtn = crud.remove_item_from_inventory(db=db, pantry_id=pantry_id, item_id=item_id)
    if rtn is None:
        raise HTTPException(status_code=404, detail="Inventory item could not be removed from pantry")
