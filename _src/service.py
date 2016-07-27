# -*- coding: utf-8 -*-

import downloader
import scraper


def get_companies(query, postcode):
    url = 'http://www.gelbeseiten.de/yp/search.yp'
    params = {
        'subject': query,
        'location': postcode,
    }
    html = downloader.fetch(url, params)
    return scraper.parse_companies(html)


def get_company(company_id):
    url = 'http://www.gelbeseiten.de/{0}'.format(company_id)
    html = downloader.fetch(url)
    return scraper.parse_company(html)


def handler(data, context):
    if data['method'] == 'company':
        return get_company(data['company_id'])
    elif data['method'] == 'companies':
        companies = get_companies(data['q'], data['postcode'])
        return {'companies': companies}
    else:
        raise Exception('Invalid method: {0}'.format(data['method']))
