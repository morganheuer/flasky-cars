from app import db

class Caretaker(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    cats = db.relationship("Cat", back_populates="caretaker")

    def to_dict(self):
        cats_info = [cat.to_dict() for cat in self.cats]

        return {
            "id": self.id,
            "name": self.name,
            "cats": cats_info
            }

    @classmethod
    def from_dict(cls, data_dict):
        return Caretaker(name=data_dict["name"])