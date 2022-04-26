def test_get_all_movies(client):
    response = client.get('/movies')
    assert b'Toy Story' in response.data
    assert b'Jumanji' in response.data
    assert b'Snowmageddon' in response.data