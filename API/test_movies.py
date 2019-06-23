from apistar import test
from movies import app, movies, MOVIE_NOT_FOUND

client = test.TestClient(app)


def test_list_movies():
    response = client.get("/")
    assert response.status_code == 200
    movies = response.json()
    assert len(movies) == 1000
    assert type(movies) == list
    movie = movies[0]
    expected = {'id': 1, 'title': 'Wake Wood ', 'genre': 'Drama|Horror|Mystery',
                'year': 2000, 'studio': 'Plymouth'}
    assert movie == expected
    last_id = movies[-1]["id"]
    assert last_id == 1000


def test_create_movie():
    new_movie = dict(
        title = 'New Movie', 
        genre = 'Mystery',
        year = 2000, 
        studio = 'Plymouth'
    )
    response = client.post("/", data=new_movie)
    assert response.status_code == 201
    assert len(movies) == 1001
    
    response = client.get("/")
    assert response.status_code == 200
    assert len(movies) == 1001
    new_movie["id"] = 1001
    assert response.json()[1000] == new_movie


def test_create_movie_missing_field():
    new_movie = dict(
        title = 'New Movie', 
        genre = 'Mystery',
        year = 2000
    )
    response = client.post("/", data=new_movie)
    assert response.status_code == 400

    error = response.json()
    assert error["studio"] == 'The "studio" field is required.'

def test_create_movie_field_validation():
    new_movie = dict(
        title = 'New Movie', 
        genre = 'Mystery',
        year = 1899, 
        studio = 'Plymouth'
    )
    response = client.post("/", data=new_movie)
    assert response.status_code == 400

    error = response.json()
    assert error["year"] == "Must be greater than or equal to 1900."


def test_get_movie():
    response = client.get("/")
    assert response.status_code == 200

    expected = {'id': 1, 'title': 'Wake Wood ', 'genre': 'Drama|Horror|Mystery',
                'year': 2000, 'studio': 'Plymouth'}
    assert response.json()[0] == expected


def test_get_movie_not_found():
    response = client.get("/2000/")
    assert response.status_code == 404
    assert response.json() == {"error": MOVIE_NOT_FOUND}


def test_update_movie():
    updated_movie = {'title': 'Wake Wood ', 'genre': 'Drama',
                    'year': 2000, 'studio': 'Plymouth'}
    response = client.put("/1/", data=updated_movie)
    assert response.status_code == 200

    # test put response
    expected = {'id': 1, 'title': 'Wake Wood ', 'genre': 'Drama',
                'year': 2000, 'studio': 'Plymouth'}
    assert response.json() == expected

    # check if data persisted
    response = client.get("/1")
    expected = "Drama"
    assert response.json()["genre"] == "Drama"


def test_update_movie_not_found():
    updated_movie = {'title': 'Wake Wood ', 'genre': 'Drama',
                    'year': 2000, 'studio': 'Plymouth'}
    response = client.put("/2000/", data=updated_movie)
    assert response.status_code == 404
    assert response.json() == {"error": MOVIE_NOT_FOUND}


def test_update_movie_validation():
    updated_movie = {'title': 'Wake Wood ', 'genre': 'Drama',
                    'year': 1899, 'studio': 'Plymouth'}
    response = client.put("/1/", data=updated_movie)
    assert response.status_code == 400

    error = response.json()
    assert error == {"year": "Must be greater than or equal to 1900."}


def test_delete_movie():
    movies_count = len(movies)
    response = client.delete("/1/")
    assert response.status_code == 204
    assert len(movies) == movies_count - 1
    
    response = client.get("/1/")
    assert response.status_code == 404