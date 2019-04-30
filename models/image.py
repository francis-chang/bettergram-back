from db import db
from typing import List
from PIL import Image
from sqlalchemy import desc


class ImageModel(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(150))
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(200), nullable=False)
    full_size_url = db.Column(db.String(200), nullable=False)
    is_long = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    @classmethod
    def find_by_id(cls, _id: int) -> "ImageModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ImageModel"]:
        return cls.query.all()

    @classmethod
    def find_by_offset(cls, offset: int):
        query = cls.query.order_by(desc(ImageModel.id)).limit(12).offset(offset).all()
        has_next = False
        _next = len(cls.query.all()) - (int(offset) + 12)
        if _next >= 0:
            has_next = True
        return {"images": [image.json() for image in query], "has_next": has_next}

    @classmethod
    def find_dimensions(cls, file: str) -> List[int]:
        im = Image.open(file)
        return list(im.size)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self):
        dict = {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "full_url": self.full_size_url,
            "height": self.height,
            "is_long": self.is_long,
        }
        return dict