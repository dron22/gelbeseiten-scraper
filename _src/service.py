
import scraper
import downloader


def get_company(company_id):
    url = 'http://www.gelbeseiten.de/{0}'.format(company_id)
    html = downloader.fetch(url)
    company = scraper.get_company(html)
    return company


def get_companies(query, postcode):
    url = 'http://www.gelbeseiten.de/yp/search.yp'
    params = {
        'subject': query,
        'location': postcode,
    }
    html = downloader.fetch(url, params)
    return scraper.get_companies(html)
