
import pytest
from mock import Mock, call


@pytest.fixture(scope='function')
def downloader_mock(monkeypatch):
    import service
    html = 'This should be html'
    fetch_mock = Mock(return_value=html)
    monkeypatch.setattr(service.downloader, 'fetch', fetch_mock)
    return fetch_mock


@pytest.fixture(scope='function')
def scraper_mocks(monkeypatch):
    import service

    company = {'companyName': 'PizzaQueen', 'id': 12345}
    companies_result = [company]
    companies_mock = Mock(return_value=companies_result)
    monkeypatch.setattr(service.scraper, 'parse_companies', companies_mock)

    company_result = company
    company_mock = Mock(return_value=company_result)
    monkeypatch.setattr(service.scraper, 'parse_company', company_mock)

    return {'companies': companies_mock, 'company': company_mock}


def test_get_companies(monkeypatch, downloader_mock, scraper_mocks):
    import service

    html = 'This should be html'
    url = 'http://www.gelbeseiten.de/yp/search.yp'
    query = 'Pizza'
    postcode = 10111
    expected = [{'companyName': 'PizzaQueen', 'id': 12345}]

    r = service.get_companies(query, postcode)
    assert r == expected

    expected_call = call(url, {'subject': query, 'location': postcode})
    assert downloader_mock.call_args_list == [expected_call]

    expected_call = call(html)
    assert scraper_mocks['companies'].call_args_list == [expected_call]


def test_get_company(monkeypatch, downloader_mock, scraper_mocks):
    import service

    html = 'This should be html'
    company_id = 12345
    url = 'http://www.gelbeseiten.de/{0}'.format(company_id)
    expected = {'companyName': 'PizzaQueen', 'id': 12345}

    r = service.get_company(company_id)
    assert r == expected

    expected_call = call(url,)
    assert downloader_mock.call_args_list == [expected_call]

    expected_call = call(html)
    assert scraper_mocks['company'].call_args_list == [expected_call]
