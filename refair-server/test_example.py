def test_missing_page(client):
    response = client.get('/thispagedoesnotexist')
    assert response.status_code == 404
