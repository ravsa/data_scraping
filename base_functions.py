#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xmltodict import parse
from collections import defaultdict
import requests
import zipfile
import io
import json


class BaseFunctions:

    def __init__(self, config_file, output_file):
        try:
            self.config_file = config_file
            self._output_file = output_file
            with open(self.config_file) as file:
                self._config = json.load(file)
            self._base_url = self._config.get('base_url')
            self.processed_data = defaultdict(list)
            self._versions = self._config.get('versions', [])
        except FileNotFoundError:
            print("Unable to find {} file in current dir".format(
                self.config_file))

    def delete_duplicates(self):
        for grp, dependencies in self.processed_data.items():
            self.processed_data[grp] = [dict(t) for t in set(
                [tuple(d.items()) for d in dependencies])]

    def get_query_result(self, version, pkgs):
        url = self._base_url.format(ver=version, pkg=pkgs)
        response = requests.get(url)
        _zip = zipfile.ZipFile(io.BytesIO(response.content))
        return parse(_zip.read('demo/pom.xml'),
                     dict_constructor=dict).get('project').get('dependencies').get('dependency')

    def run(self):
        self.process()
        self.delete_duplicates()
        try:
            with open(self._output_file, 'w') as file:
                json.dump(self.processed_data, file, indent=4)
            print("SAVED: ", self._output_file)
        except FileNotFoundError:
            print("Unable to process {} file in current dir".format(
                self.config_file))
