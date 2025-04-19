from pydantic import BaseModel
from typing import Optional
from typing import List

class RecipeBase(BaseModel):
    name: str
    instructions: Optional[str] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None

# class RecipeIngredientBase(BaseModel):
#    ingredient_id: int
#    quantity: float
#    unit: Optional[str] = None

#class RecipeIngredientCreate(RecipeIngredientBase):
#    pass

class IngredientBase(BaseModel):
    name: str
    category: str

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int

    class Config:
        from_attributes = True

class IngredientForRecipeInput(BaseModel):
    name: str
    quantity: float
    unit: Optional[str] = None


class RecipeIngredient(BaseModel):
    id: int
    quantity: float
    unit: Optional[str] = None
    ingredient: Ingredient  # nested ingredient details

    class Config:
        from_attributes = True

# class RecipeCreate(RecipeBase):
#     ingredients: List[RecipeIngredientCreate] = []

class RecipeCreate(BaseModel):
    name: str
    instructions: Optional[str] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None
    ingredients: List[IngredientForRecipeInput]

class Recipe(RecipeBase):
    id: int
    ingredients: List[RecipeIngredient] = []

    class Config:
        from_attributes = True

class IngredientNameOnly(BaseModel):
    name: str

class IngredientValidationRequest(BaseModel):
    ingredients: List[IngredientNameOnly]

class MissingIngredient(BaseModel):
    name: str

class IngredientValidationResponse(BaseModel):
    missing_ingredients: List[MissingIngredient]

class IngredientNameCategory(BaseModel):
    name: str
    category: Optional[str] = None

class IngredientResolveRequest(BaseModel):
    ingredients: List[IngredientNameCategory]

class MissingIngredientField(BaseModel):
    name: str
    missing: List[str]

class IngredientResolveResponse(BaseModel):
    created: List[str]
    skipped: List[str]
    missing_info: List[MissingIngredientField]
