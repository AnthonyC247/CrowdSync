def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"CrowdSync" in response.data

def test_results_page(client):
    response = client.get('/results')
    assert response.status_code == 200
    assert b"Search events near you!" in response.data