from app import app

def test_home_route():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert b'Check sentimaent of comment' in response.data

# def test_get_sentiment_route():
#     tester = app.test_client()
#     response = tester.get('/get_sentiment?str=I+love+this+product')
#     assert response.status_code == 200
#     assert b'The sentiment of the comment is' in response.data


