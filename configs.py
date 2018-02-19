#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from selenium.common.exceptions import WebDriverException
from warnings import filterwarnings
from collections import defaultdict
from selenium import webdriver
import requests
import sys


filterwarnings("ignore")


class Config:

    def __init__(self):
        try:
            self.driver = webdriver.PhantomJS(
                executable_path='phantomjs/bin/phantomjs')
        except WebDriverException as e:
            print(str(e))
            sys.exit(1)
        self.wildfly_baseurl = (
            "http://generator.wildfly-swarm.io/generator?g=com.example&a=demo"
            "&sv=2018.1.0{pkg}"
        )
        self.spring_baseurl = (
            "https://start.spring.io/starter.zip?type=maven-project&language="
            "java&bootVersion={ver}&baseDir=demo&groupId=com.example&artifact"
            "Id=demo&name=demo&description=Demo+project+for+Spring+Boot&packa"
            "geName=com.example.demo&packaging=jar&javaVersion=1.8&autocomple"
            "te=&generate-project={pkg}"
        )
        self.vertx_baseurl = (
            "http://start.vertx.io/starter.zip?artifactId=demo&build=Maven&de"
            "pendencies={pkg}&groupId=com.example&language=Java&version={ver}"
        )

    def get_config(self, key):
        return {
            'spring': self.get_spring_config(),
            'vertx': self.get_vertx_config(),
            'wildfly': self.get_wildfly_config()
        }.get(key, {})

    def get_wildfly_config(self):
        _url = "http://wildfly-swarm.io/generator/"
        self.driver.get(_url)
        response = self.driver.execute_script(
            "return angular.element(document.querySelector('body > div.wrapper"
            " > div.container > div > div > form > div:nth-child(6)')).scope()"
            ".categories")
        _result = list()
        for item in response:
            for obj in item['fractions']:
                del obj['fractionDependencies']
            _result.append(item)
        return {
            'base_url': self.wildfly_baseurl,
            'dependencies': _result
        }

    def get_spring_config(self):
        _url = 'https://start.spring.io/'
        self.driver.get(_url)
        versions = list()
        try:
            for index in range(10):
                versions.append(self.driver.execute_script(
                    "return document.getElementById('bootVersion').options[{ver}].value"
                    .format(ver=index)))
        except Exception as e:
            print("You can skip this excepiton: ", type(e))
        _url = 'https://start.spring.io/ui/dependencies.json?version={ver}'
        _result = list()
        for ver in versions:
            _res = {ver: requests.get(_url.format(ver=ver)).json()}
            _temp = defaultdict(list)
            for key, value in _res.items():
                for x in value.get('dependencies', []):
                    _temp[x['group'].lower()].append(x)
            _result.append({key: _temp})
        return {
            'base_url': self.spring_baseurl,
            'dependencies': _result
        }

    def get_vertx_config(self):
        _url = 'http://start.vertx.io/dependencies'
        versions = [
            "3.5.0",
            "3.4.2",
            "3.4.1",
            "3.4.0"
        ]
        _resp = requests.get(_url).json()
        return {
            'base_url': self.vertx_baseurl,
            'versions': versions,
            'dependencies': _resp
        }
