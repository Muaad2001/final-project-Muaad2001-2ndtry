import tempfile
import os
import pytest
from flaskr import create_app
from flaskr.db import init_db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })
    with app.app_context():
        test_folder = os.path.dirname(__file__)
        test_csv = os.path.join(test_folder, 'test_data.csv')
        init_db(csv_path=test_csv)
    
    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()