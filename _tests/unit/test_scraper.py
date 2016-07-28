
import pytest


@pytest.fixture(scope='function')
def companies_html():
    return """
    <html>
        <head></head>
        <body>
            <div itemtype="http://schema.org/LocalBusiness">
                <span itemprop="name">company_1</span>
                <a itemprop="url" href="http://www.gelbeseiten.de/12345/company_1.html">Link</a>
            </div>
            <div itemtype="http://schema.org/LocalBusiness">
                <span itemprop="name">company_2</span>
                <a itemprop="url" href="http://www.gelbeseiten.de/67890/company_2.html">Link</a>
            </div>
        </body>
    </html>
    """


@pytest.fixture(scope='function')
def company_html():
    return """
    """


def test_parse_companies(companies_html):
    import scraper
    expected = [
        {'companyName': 'company_1', 'id': '12345'},
        {'companyName': 'company_2', 'id': '67890'},
    ]
    r = scraper.parse_companies(companies_html)
    assert sorted(r) == sorted(expected)
