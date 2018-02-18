#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xmltodict import parse
from collections import defaultdict
import requests
import zipfile
import io
import json


class SpringIO:

    __config_filename = 'spring_config.json'

    def __init__(self, output_file):
        try:
            with open(self.__config_filename) as file:
                self._config = json.load(file)
            self._base_url = self._config.get('base_url')
            self._output_file = output_file
            self.processed_data = defaultdict(list)
        except FileNotFoundError:
            print("Unable to find {} file in current dir".format(
                self.__config_filename))

    def process(self):
        for item in self._config.get('dependencies', []):
            for version, content in item.items():
                print("VERSION: ", version)
                for group, dependencies in content.items():
                    pkg_query = '&style=' + \
                        '&style='.join([dep['id'] for dep in dependencies])
                    description = dependencies[0]['description']
                    resp = self.get_query_result(version, pkg_query)
                    self.processed_data[group] += [dict(pkg, **{'tag': group,
                                                                'description': description})
                                                   for pkg in resp]
                    print("GROUP: ", group)

    def delete_duplicates(self):
        for grp, dependencies in self.processed_data.items():
            self.processed_data[grp] = [dict(t) for t in set(
                [tuple(d.items()) for d in dependencies])]

    def get_query_result(self, version, pkgs):
        url = self._base_url.format(ver=version) + pkgs
        response = requests.get(url)
        _zip = zipfile.ZipFile(io.BytesIO(response.content))
        return parse(_zip.read('demo/pom.xml'),
                     dict_constructor=dict).get('project').get('dependencies').get('dependency')

    def run(self):
        self.process()
        self.delete_duplicates()
        with open(self._output_file, 'w') as file:
            json.dump(self.processed_data, file, indent=4)
        print("SAVED: ", self._output_file)
