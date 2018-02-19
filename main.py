#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spring_fetch import SpringIO
from vertx_fetch import VertxIO
from wildfly_fetch import WildflyIO


def main():
    ecosystems = [('spring', SpringIO),
                  ('vertx', VertxIO),
                  ('wildfly', WildflyIO)
                  ]
    for eco, runner in ecosystems:
        try:
            print("RUNNING Job for {}".format(eco))
            runner(eco, eco + '_dump.json').run()
        except Exception as e:
            print('ERROR: fetching data from {}'.format(eco))
            print(str(e))


if __name__ == '__main__':
    main()
