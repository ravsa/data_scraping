#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base_functions import BaseFunctions


class SpringIO(BaseFunctions):

    def __init__(self):
        self.sub_eco = 'spring'
        self._output_file = None
        super().__init__(self.sub_eco)

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

    def __str__(self):
        return self.sub_eco


class VertxIO(BaseFunctions):

    def __init__(self):
        self.sub_eco = 'vertx'
        self._output_file = None
        super().__init__(self.sub_eco)

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

    def __str__(self):
        return self.sub_eco


class WildflyIO(BaseFunctions):

    def __init__(self):
        self.sub_eco = 'wildfly'
        self._output_file = None
        super().__init__(self.sub_eco)

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

    def __str__(self):
        return self.sub_eco
