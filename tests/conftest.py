from flask import request_finished
from app import db
import pytest
from app.models.cat import Cat 

from app import create_app

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender,response, **extra):
        db.session.remove()
    
    with app.app_context():
        db.create_all() 
        yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_cats(app):
    fluffy = Cat(id=1, name="fluffy", color="grey", personality="likes to cuddle")
    sleepy = Cat(id=2, name="sleepy", color="orange", personality="likes to take naps")

    db.session.add(fluffy)
    db.session.add(sleepy)
    db.session.commit()

