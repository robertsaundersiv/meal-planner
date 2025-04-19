from fastapi import HTTPException, status, FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
import secrets
import os
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine, Base
from .auth import authenticate
from typing import List



app = FastAPI()
security = HTTPBasic()

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency: get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(user: str = Depends(authenticate)):
    return {"message": f"Welcome, {user}!"}

@app.post("/recipes/", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db), user: str = Depends(authenticate)):
    return crud.create_recipe(db=db, recipe=recipe)

@app.get("/recipes/", response_model=list[schemas.Recipe])
def read_recipes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user: str = Depends(authenticate)):
    return crud.get_recipes(db=db, skip=skip, limit=limit)

@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_db), user: str = Depends(authenticate)):
    db_recipe = crud.get_recipe(db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


# Allow frontend dev/test from localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ingredients/", response_model=schemas.Ingredient)
def create_ingredient(
    ingredient: schemas.IngredientCreate,
    db: Session = Depends(get_db),
    user: str = Depends(authenticate)
):
    return crud.create_ingredient(db=db, ingredient=ingredient)

@app.get("/ingredients/", response_model=List[schemas.Ingredient])
def read_ingredients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: str = Depends(authenticate)
):
    return crud.get_ingredients(db, skip=skip, limit=limit)

@app.post("/recipes/validate-ingredients", response_model=schemas.IngredientValidationResponse)
def validate_ingredient_names(
    payload: schemas.IngredientValidationRequest,
    db: Session = Depends(get_db),
    user: str = Depends(authenticate)
):
    missing = []

    for ing in payload.ingredients:
        existing = db.query(models.Ingredient).filter_by(name=ing.name).first()
        if not existing:
            missing.append({"name": ing.name})

    return {"missing_ingredients": missing}

@app.post("/ingredients/resolve", response_model=schemas.IngredientResolveResponse)
def resolve_missing_ingredients(
    payload: schemas.IngredientResolveRequest,
    db: Session = Depends(get_db),
    user: str = Depends(authenticate)
):
    created = []
    skipped = []
    missing_info = []

    for ing in payload.ingredients:
        existing = db.query(models.Ingredient).filter_by(name=ing.name).first()
        if existing:
            skipped.append(ing.name)
            continue

        missing_fields = []
        if not ing.category:
            missing_fields.append("category")

        if missing_fields:
            missing_info.append({
                "name": ing.name,
                "missing": missing_fields
            })
            continue

        # Create new ingredient
        new_ing = models.Ingredient(name=ing.name, category=ing.category)
        db.add(new_ing)
        db.commit()
        db.refresh(new_ing)
        created.append(ing.name)

    return {
        "created": created,
        "skipped": skipped,
        "missing_info": missing_info
    }
