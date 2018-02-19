#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base_functions import BaseFunctions


class VertxIO(BaseFunctions):

    def __init__(self, config_file, output_file):
        super().__init__(config_file, output_file)

    def process(self):
        for version in self._versions:
            print("VERSION: ", version)
            for item in self._config.get('dependencies', []):
                group = item.get('category')
                items = item.get('items')
                pkg_query = ','.join([it['artifactId']
                                      for it in items if it.get('artifactId')])
                resp = self.get_query_result(version, pkg_query)
                self.processed_data[group] += [dict(pkg, **{'categories': group,
                                                            'version': version
                                                            })
                                               for pkg in resp]
                print("GROUP: ", group)
