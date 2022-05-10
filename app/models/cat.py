from app import db

class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)
    personality = db.Column(db.String, nullable=False)
    caretaker_id = db.Column(db.Integer, db.ForeignKey('caretaker.id'))
    caretaker = db.relationship("Caretaker", back_populates="cats")

    def to_dict(self):
        caretaker_name = self.caretaker.name if self.caretaker else ""

        return dict(
            id=self.id,
            name=self.name,
            color=self.color,
            personality=self.personality,
            caretaker=caretaker_name,
        )

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            name=data_dict["name"],
            color=data_dict["color"],
            personality=data_dict["personality"],
            )

    def replace_details(self, data_dict):
        self.name = data_dict["name"]
        self.personality = data_dict["personality"]
        self.color = data_dict["color"]

