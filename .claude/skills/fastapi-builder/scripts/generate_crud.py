#!/usr/bin/env python3
"""
Generate CRUD endpoints for a FastAPI model.

Usage:
    python generate_crud.py <ModelName> --fields "name:str,age:int,email:str"
"""

import argparse
from pathlib import Path
import re


def to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case."""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def parse_field(field_str: str) -> tuple:
    """Parse field string like 'name:str' into (name, type)."""
    parts = field_str.split(':')
    if len(parts) != 2:
        raise ValueError(f"Invalid field format: {field_str}. Use 'field_name:type'")
    return parts[0].strip(), parts[1].strip()


def generate_model_code(model_name: str, fields: list) -> str:
    """Generate SQLAlchemy model code."""
    snake_name = to_snake_case(model_name)
    field_lines = []

    for field_name, field_type in fields:
        if field_type in ['str', 'string']:
            field_lines.append(f"    {field_name} = Column(String, nullable=False)")
        elif field_type in ['int', 'integer']:
            field_lines.append(f"    {field_name} = Column(Integer, nullable=False)")
        elif field_type in ['float']:
            field_lines.append(f"    {field_name} = Column(Float, nullable=False)")
        elif field_type in ['bool', 'boolean']:
            field_lines.append(f"    {field_name} = Column(Boolean, default=False)")
        else:
            field_lines.append(f"    {field_name} = Column(String, nullable=False)  # Type: {field_type}")

    return f'''class {model_name}(Base):
    __tablename__ = "{snake_name}s"

    id = Column(Integer, primary_key=True, index=True)
{chr(10).join(field_lines)}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
'''


def generate_schema_code(model_name: str, fields: list) -> str:
    """Generate Pydantic schema code."""
    field_lines = []

    for field_name, field_type in fields:
        if field_type in ['str', 'string']:
            field_lines.append(f'    {field_name}: str')
        elif field_type in ['int', 'integer']:
            field_lines.append(f'    {field_name}: int')
        elif field_type in ['float']:
            field_lines.append(f'    {field_name}: float')
        elif field_type in ['bool', 'boolean']:
            field_lines.append(f'    {field_name}: bool = False')
        else:
            field_lines.append(f'    {field_name}: str  # Adjust type as needed')

    return f'''class {model_name}Base(BaseModel):
{chr(10).join(field_lines)}


class {model_name}Create({model_name}Base):
    pass


class {model_name}Update(BaseModel):
{chr(10).join(f'    {name}: Optional[{type}] = None' for name, type in fields)}


class {model_name}Response({model_name}Base):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
'''


def generate_routes_code(model_name: str) -> str:
    """Generate FastAPI routes code."""
    snake_name = to_snake_case(model_name)
    plural = f"{snake_name}s"

    return f'''from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db import models
from app import schemas

router = APIRouter()


@router.get("/{plural}", response_model=List[schemas.{model_name}Response])
def list_{plural}(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all {plural} with pagination"""
    items = db.query(models.{model_name}).offset(skip).limit(limit).all()
    return items


@router.get("/{plural}/{{item_id}}", response_model=schemas.{model_name}Response)
def get_{snake_name}(item_id: int, db: Session = Depends(get_db)):
    """Get a specific {snake_name} by ID"""
    item = db.query(models.{model_name}).filter(models.{model_name}.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_name} with id {{item_id}} not found"
        )
    return item


@router.post("/{plural}", response_model=schemas.{model_name}Response, status_code=status.HTTP_201_CREATED)
def create_{snake_name}(item: schemas.{model_name}Create, db: Session = Depends(get_db)):
    """Create a new {snake_name}"""
    db_item = models.{model_name}(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/{plural}/{{item_id}}", response_model=schemas.{model_name}Response)
def update_{snake_name}(
    item_id: int,
    item: schemas.{model_name}Update,
    db: Session = Depends(get_db)
):
    """Update an existing {snake_name}"""
    db_item = db.query(models.{model_name}).filter(models.{model_name}.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_name} with id {{item_id}} not found"
        )

    # Update only provided fields
    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{plural}/{{item_id}}", status_code=status.HTTP_204_NO_CONTENT)
def delete_{snake_name}(item_id: int, db: Session = Depends(get_db)):
    """Delete a {snake_name}"""
    db_item = db.query(models.{model_name}).filter(models.{model_name}.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_name} with id {{item_id}} not found"
        )

    db.delete(db_item)
    db.commit()
    return None
'''


def generate_crud(model_name: str, fields_str: str):
    """Generate CRUD code for a model."""
    # Parse fields
    fields = [parse_field(f) for f in fields_str.split(',')]

    print(f"🔨 Generating CRUD for model: {model_name}")
    print(f"📋 Fields: {', '.join(f'{name}:{type}' for name, type in fields)}")
    print()

    # Generate code
    model_code = generate_model_code(model_name, fields)
    schema_code = generate_schema_code(model_name, fields)
    routes_code = generate_routes_code(model_name)

    # Print instructions
    print("=" * 60)
    print("📝 ADD TO app/db/models.py:")
    print("=" * 60)
    print(model_code)
    print()

    print("=" * 60)
    print("📝 ADD TO app/schemas.py:")
    print("=" * 60)
    print(schema_code)
    print()

    print("=" * 60)
    snake_name = to_snake_case(model_name)
    print(f"📝 CREATE FILE app/api/routes/{snake_name}s.py:")
    print("=" * 60)
    print(routes_code)
    print()

    print("=" * 60)
    print("📝 UPDATE main.py - Add this import and router:")
    print("=" * 60)
    print(f"from app.api.routes import {snake_name}s")
    print(f"app.include_router({snake_name}s.router, prefix=\"/api/v1\", tags=[\"{snake_name}s\"])")
    print()

    print("✅ Done! Copy the code above to your project files.")


def main():
    parser = argparse.ArgumentParser(description="Generate CRUD endpoints for a FastAPI model")
    parser.add_argument("model_name", help="Name of the model (e.g., Product, User)")
    parser.add_argument(
        "--fields",
        "-f",
        required=True,
        help="Comma-separated fields (e.g., 'name:str,age:int,email:str')"
    )

    args = parser.parse_args()
    generate_crud(args.model_name, args.fields)


if __name__ == "__main__":
    main()
