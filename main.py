#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spring_fetch import SpringIO
from vertex_fetch import VertexIO
from wildfly_fetch import WildflyIO


if __name__ == '__main__':
    ecosystems = [('spring', SpringIO),
                  ('vertex', VertexIO),
                  ('wildfly', WildflyIO)
                  ]
    for eco, runner in ecosystems:
        runner(eco + '_dump.json').run()
