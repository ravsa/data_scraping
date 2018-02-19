#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base_functions import BaseFunctions


class SpringIO(BaseFunctions):

    def __init__(self, config_file, output_file):
        super().__init__(config_file, output_file)

    def process(self):
        for item in self._config.get('dependencies', []):
            for version, content in item.items():
                print("VERSION: ", version)
                for group, dependencies in content.items():
                    pkg_query = '&style=' + \
                        '&style='.join([dep['id'] for dep in dependencies])
                    resp = self.get_query_result(version, pkg_query)
                    self.processed_data[group] += [dict(pkg, **{'categories': group,
                                                                'version': version})
                                                   for pkg in resp]
                    print("GROUP: ", group)
