# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.http import Request, HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import lxml.etree as et
from lxml.etree import HTMLParser
from io import StringIO

# from shakespeare.items import ShakespeareItem


class GenSpider(scrapy.Spider):
    name = 'gen'
    domain = "shakespeare.mit.edu"
    allowed_domains = ['shakespeare.mit.edu']
    start_urls = ['http://shakespeare.mit.edu/']

    def get_content(self, res):
        text = res.xpath('//div[@class="art-postcontent"]//text()').extract()
        return ''.join(text).strip()

    def get_name(self, res):
        text = res.xpath('//div[@class="content-cotainer"]//h1/text()').extract()
        return text

    def fix_url(self, url, orig_url):
        print(orig_url, url)
        if url.startswith("//"):
            url = "http:{}".format(url)
        else:
            if not url.startswith("http"):
                url = os.path.join(orig_url, url)
        return url

    def parse(self, response):
        orig_url = os.path.dirname(response.url)
        print(orig_url)
        links = response.xpath('//body//a/@href').extract()
        for i, url in enumerate(links):
            url = self.fix_url(url, orig_url)
            if '/full.' in url:
                continue
            if '/news.' in url:
                continue

            if '//shakespeare.mit.edu/' not in url:
                continue

            if '/poetry/sonnets' in url:
                yield Request(url, callback=self.parse_item)

            if '/poetry' in url:
                yield Request(url, callback=self.parse_scene)

            yield Request(url, callback=self.parse_item)

    def parse_item(self, res):
        orig_url = os.path.dirname(res.url)
        links = res.xpath('//body//a/@href').extract()
        for i, url in enumerate(links):
            url = self.fix_url(url, orig_url)
            if '/full.' in url:
                continue
            if 'shakespeare.mit.edu/Shakespeare' in url:
                continue
            if not url.startswith("http"):
                print(url)
                continue

            yield Request(url, callback=self.parse_scene)

    def parse_scene(self, res):
        parser = HTMLParser(encoding='utf-8', recover=True)
        tree = et.parse(StringIO(res.body.__str__()), parser)
        for element in tree.xpath('//body/table'):
            element.getparent().remove(element)

        html = et.tostring(tree, pretty_print=True, xml_declaration=True)
        response = HtmlResponse(url=res.url, body=html, encoding='utf-8')
        name = res.url.split('/')[-1]
        name = name.replace('html', 'txt')
        content = response.xpath('//text()').extract()
        lines = []
        for line in content:
            if line[:2] == "b\'":
                continue

            line = line.replace('\\n', '\n')
            line = line.replace("\\t", ' ')
            line = line.replace("\\'", '\'')
            lines.append(line)

        content = ''.join(lines)
        if not os.path.exists('output'):
            os.mkdir('output')

        with open('output/{}'.format(name), "w") as f:
            f.write(content)

        # item = ShakespeareItem()
        # item['url'] = res.url
        # item['name'] = name
        # item['content'] = content
        yield [name]

