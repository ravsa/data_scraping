#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xmltodict import parse
from collections import defaultdict
import requests
import zipfile
import io
import json


class VertexIO:

    __config_filename = 'vertex_config.json'

    def __init__(self, output_file):
        try:
            with open(self.__config_filename) as file:
                self._config = json.load(file)
            self._base_url = self._config.get('base_url')
            self._output_file = output_file
            self.processed_data = defaultdict(list)
            self._versions = [
                '3.5.0',
                '3.4.2',
                '3.4.1',
                '3.4.0'
            ]
        except FileNotFoundError:
            print("Unable to find {} file in current dir".format(
                self.__config_filename))

    def process(self):
        description = {}
        for version in self._versions:
            print("VERSION: ", version)
            for item in self._config.get('dependencies', []):
                group = item.get('category')
                items = item.get('items')
                pkg_query = ','.join([it['artifactId']
                                      for it in items if it.get('artifactId')])
                description.update(
                    {it['artifactId']: it['description'] for it in items if it.get('artifactId') and it.get('description')})
                resp = self.get_query_result(version, pkg_query)
                self.processed_data[group] += [dict(pkg, **{'tag': group,
                                                            'description': description.get(pkg['artifactId'], ''),
                                                            'version': version
                                                            })
                                               for pkg in resp]
                print("GROUP: ", group)

    def delete_duplicates(self):
        __import__('pprint').pprint(self.processed_data)
        for grp, dependencies in self.processed_data.items():
            self.processed_data[grp] = [dict(t) for t in set(
                [tuple(d.items()) for d in dependencies])]

    def get_query_result(self, version, pkgs):
        url = self._base_url.format(ver=version, dep=pkgs)
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
