from calendarapi.extensions import db


class Lawyer(db.Model):
    __tablename__ = "lawyers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    lawyer_mail = db.Column(db.String(100), unique=True)

    specializations = db.relationship(
        "Specialization",
        secondary="specializations_to_lawyers",
        lazy=True,
        backref=db.backref("lawyers", lazy=True),
    )

    cities = db.relationship(
        "City",
        secondary="layers_to_cities",
        lazy=True,
        backref=db.backref("lawyers", lazy=True),
    )

    schedules = db.relationship(
        "Schedule",
        secondary="layers_to_schedules",
        lazy=True,
        backref=db.backref("lawyers", lazy=True),
    )

    def __repr__(self):
        return f"Lawyer: {self.name} {self.surname}"
