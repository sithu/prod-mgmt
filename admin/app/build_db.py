from app import app, db
from app.model import Color, Machine, Product

def build_sample_db():
    db.drop_all()
    db.create_all()
    create_colors()
    db.session.commit()


def create_colors():
    color_names = [
        'White', 'Green', 'Blue', 'Red'
    ]
    color_codes = [
        '#100', '#101', '#102', '#103'
    ]

    for i in range(len(color_names)):
        color = Color()
        color.color_code = color_codes[i]
        color.name = color_names[i]
        db.session.add(color)


