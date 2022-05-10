from app import db

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    team = db.Column(db.String)
    country = db.Column(db.String)
    handsome = db.Column(db.Boolean)
    cars = db.relationship("Car", backref="driver")

    def to_dict(self):
        cars_list = []
        for car in self.cars:
            cars_list.append(car.to_dict_basic())


        return {
            "id": self.id,
            "name": self.name,
            "team": self.team,
            "country": self.country,
            "handsome": self.handsome,
            "cars": cars_list
            #"num_cars": len(self.cars)          
        }