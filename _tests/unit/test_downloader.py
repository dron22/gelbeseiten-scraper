
import pytest
from mock import Mock, call


@pytest.mark.parametrize('params', [
    ({}),
    ({'hello': 'world'}),
])
def test_fetch(monkeypatch, params):
    import downloader
    test_html = 'This should be html'

    class DummyResponse:
        status_code = 200
        text = test_html

    monkeypatch.setattr(downloader, 'useragents', ['test_useragent'])
    get_mock = Mock(return_value=DummyResponse())
    monkeypatch.setattr(downloader.requests, 'get', get_mock)

    if params:
        r = downloader.fetch('http://test.com', params)
    else:
        r = downloader.fetch('http://test.com')

    assert r == test_html

    expected_call = call(
        'http://test.com',
        headers={'User-Agent': 'test_useragent'},
        params=params
    )
    assert get_mock.call_args_list == [expected_call]
