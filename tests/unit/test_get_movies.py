from flaskr.db import get_movies

def test_get_movies(app):
    results = []
    with app.app_context():
        results = get_movies()

    assert len(results) == 3
    assert results[0]["title"] == "Toy Story"
    assert results[1]["title"] == "Jumanji"
    assert results[2]["title"] == "Snowmageddon"
    assert len(results[0]) == 24
    assert len(results[1]) == 24
    assert len(results[2]) == 24