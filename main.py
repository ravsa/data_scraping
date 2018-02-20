#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from process import SpringIO, VertxIO, WildflyIO


def main():
    for runner in (SpringIO, VertxIO, WildflyIO):
        try:
            _temp_obj = runner()
            print("RUNNING Job for {}".format(str(_temp_obj)))
            _temp_obj.run()
        except Exception as e:
            print('ERROR: fetching data from {}'.format(str(_temp_obj)))
            print(str(e))


if __name__ == '__main__':
    main()
