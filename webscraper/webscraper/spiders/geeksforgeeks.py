# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request, FormRequest
import re
from scrapy.selector import Selector
from scrapy import Item,Field
from loginform import fill_login_form

class SampleItem(Item):
    text = Field()

class GeeksforgeeksSpider(scrapy.Spider):
    name = 'geeksforgeeks'
    allowed_domains = ['geeksforgeeks.org']
    start_urls = ['http://geeksforgeeks.org/']
    login_url='http://auth.geeksforgeeks.org/'
    login_verify_url='http://geeksforgeeks.org/'
    #args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)

    def parse(self, response):
        if re.search('nir0303', response.body):
            self.is_login = True
        sel = Selector(response)
        item = SampleItem()
        item["text"] = response.body[:50]
        yield item

    def __init__(self,username = 'nir0303',password='change44'):
        self.username = username
        self.password = password
        self.is_login = False

    def start_requests(self):
        return [FormRequest(
            self.login_url,
            formdata={
                'user': self.username,
                'pass': self.password
            },
            callback=self.after_login,
            dont_filter=True,
            method="POST"
        )]

    def after_login(self, response):
        return [Request(
            self.login_verify_url,
            callback=self.login_verify
        )]

    def login_verify(self, response):
        if re.search('Login/Register', response.body):
            self.is_login = True
        print self.is_login
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

