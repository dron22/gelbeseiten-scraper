
import re
import lxml.html


selectors_search = {
    'companyName': {
        'xpath': './/*[@itemprop="name"]//text()',
    },
    'id': {
        'xpath': './/a[@itemprop="url"]/@href',
        'regex': re.compile(r'gelbeseiten\.de/(\d+)'),
    },
}

selectors_company = {
    'locality': {
        'xpath': './/*[@itemprop="addressLocality"]//text()',
    },
    'postcode': {
        'xpath': './/*[@itemprop="postalCode"]//text()',
    },
    'streetAddress': {
        'xpath': './/*[@itemprop="streetAddress"]//text()',
    },
    'companyName': {
        'xpath': './/*[@itemprop="name"]//text()',
    },
    'phone': {
        'xpath': './/ul[@class="profile"]//li[@class="phone"]//span[@class="nummer"]/text()',
    },
    'website': {
        'xpath': './/ul[@class="profile"]//li[contains(@class, "website")]//span[@class="text"]/text()',
    },
}


def _build_tree(html):
    return lxml.html.fromstring(html)


def _get_property(name, obj, selectors):
    xpath = selectors[name]['xpath']
    value = obj.xpath(xpath)[0]
    if 'regex' in selectors[name]:
        rgx = selectors[name]['regex']
        value = rgx.findall(value)[0]
    return value


def _get_property_search(name, obj):
    return _get_property(name, obj, selectors_search)


def _get_property_company(name, obj):
    return _get_property(name, obj, selectors_company)


def parse_companies(html):
    tree = _build_tree(html)
    xpath = '//*[@itemtype="http://schema.org/LocalBusiness"]'
    companyObjs = tree.xpath(xpath)
    companies = []
    for n, i in enumerate(companyObjs):
        company = {}
        for name in selectors_search.keys():
            company[name] = _get_property_search(name, i)
        companies.append(company)
    return companies


def parse_company(html):
    tree = _build_tree(html)
    xpath = '//*[@itemtype="http://schema.org/LocalBusiness"]'
    obj = tree.xpath(xpath)[0]
    company = {}
    for name in selectors_company.keys():
        company[name] = _get_property_company(name, obj)
    return company
