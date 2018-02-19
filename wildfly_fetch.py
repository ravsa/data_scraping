#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base_functions import BaseFunctions


class WildflyIO(BaseFunctions):

    def __init__(self, eco, output_file):
        super().__init__(eco, output_file)

    def process(self):
        for item in self._config.get('dependencies', []):
            group = item.get('category')
            pkg_query = '&d=' + \
                ('&d='.join([frac['artifactId']
                             for frac in item.get('fractions')]))
            resp = self.get_query_result('', pkg_query)
            self.processed_data[group] += [dict(pkg, **{'categories': group})
                                           for pkg in resp]
            print("GROUP: ", group)
