from sqlalchemy.orm import Session
from . import models, schemas

def get_recipes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Recipe).offset(skip).limit(limit).all()

def get_recipe(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(
        name=recipe.name,
        instructions=recipe.instructions,
        notes=recipe.notes,
        image_url=recipe.image_url
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    for ing in recipe.ingredients:
        db_ing_link = models.RecipeIngredient(
            recipe_id=db_recipe.id,
            ingredient_id=ing.ingredient_id,
            quantity=ing.quantity,
            unit=ing.unit
        )
        db.add(db_ing_link)

    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def create_ingredient(db: Session, ingredient: schemas.IngredientCreate):
    db_ingredient = models.Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

def get_ingredients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ingredient).offset(skip).limit(limit).all()
