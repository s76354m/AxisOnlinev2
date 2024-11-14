from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi.encoders import jsonable_encoder
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, record_id: Any) -> Optional[ModelType]:
        try:
            return db.query(self.model).filter(self.model.RecordID == record_id).first()
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        try:
            return db.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        try:
            obj_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[Dict[str, Any], ModelType]
    ) -> ModelType:
        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def remove(self, db: Session, *, record_id: int) -> ModelType:
        try:
            obj = db.query(self.model).get(record_id)
            db.delete(obj)
            db.commit()
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise e 