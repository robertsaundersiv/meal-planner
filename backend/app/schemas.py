from pydantic import BaseModel
from typing import Optional
from typing import List

class RecipeBase(BaseModel):
    name: str
    instructions: Optional[str] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None

class RecipeIngredientBase(BaseModel):
    ingredient_id: int
    quantity: float
    unit: Optional[str] = None

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class IngredientBase(BaseModel):
    name: str
    category: str

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int

    class Config:
        from_attributes = True




class RecipeIngredient(RecipeIngredientBase):
    id: int
    ingredient: Ingredient  # nested ingredient details

    class Config:
        from_attributes = True

class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredientCreate] = []

class Recipe(RecipeBase):
    id: int
    ingredients: List[RecipeIngredient] = []

    class Config:
        from_attributes = True

