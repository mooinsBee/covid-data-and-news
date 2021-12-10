from covid_news_handling import news_API_request
from covid_news_handling import update_news

def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()
    assert isinstance(data, list)

def test_update_news():
    update_news(update_interval=10, update_name='test', repeat=True)
    update_news(update_interval=17, update_name='test 2', repeat=False)
