from app import db

class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)
    personality = db.Column(db.String, nullable=False)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            color=self.color,
            personality=self.personality,
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

