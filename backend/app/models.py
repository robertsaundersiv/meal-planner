from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, Boolean, Enum, Date
from sqlalchemy.orm import relationship, declarative_base
import enum
from .database import Base

# Base = declarative_base()

class TagType(str, enum.Enum):
    descriptive = "descriptive"
    preference = "preference"

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    instructions = Column(Text)
    image_url = Column(String)
    notes = Column(Text)
    ingredients = relationship("RecipeIngredient", back_populates="recipe")
    tags = relationship("RecipeTag", back_populates="recipe")

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String)

class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    quantity = Column(Float)
    unit = Column(String)
    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(Enum(TagType))

class RecipeTag(Base):
    __tablename__ = 'recipe_tags'
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    recipe = relationship("Recipe", back_populates="tags")
    tag = relationship("Tag")

class MealPlan(Base):
    __tablename__ = 'meal_plans'
    id = Column(Integer, primary_key=True)
    week_start = Column(Date)
    entries = relationship("MealPlanEntry", back_populates="meal_plan")

class MealPlanEntry(Base):
    __tablename__ = 'meal_plan_entries'
    id = Column(Integer, primary_key=True)
    meal_plan_id = Column(Integer, ForeignKey("meal_plans.id"))
    day = Column(String)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    is_locked = Column(Boolean, default=False)
    meal_plan = relationship("MealPlan", back_populates="entries")