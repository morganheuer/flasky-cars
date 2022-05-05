def test_get_all_cats_with_empty_db_return_empty_list(client):
    response = client.get('/cats')

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_one_cat(client, two_cats):
    response = client.get("cats/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "fluffy",
        "color": "grey",
        "personality": "likes to cuddle"
    }