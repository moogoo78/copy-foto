#!/usr/bin/env python
# -.- coding: utf-8 -.-

import argparse
import configparser
import os
import sys
from pathlib import Path
from datetime import datetime, date
import time
import shutil

def pp(*args):
    print ('copy-foto)', *args)

def main(args):
    config = configparser.ConfigParser()

    config_path = Path.cwd().joinpath(args.config)
    config.read(config_path)

    if args.set_config:
        with open(config_path, 'w') as configfile:
            source_dir = args.set_config[0]
            target_dir = args.set_config[1]
            source_path = Path(source_dir)
            target_path = Path(target_dir)
            is_dir_exist = True
            if not source_path.exists():
                pp('path: {} not exists'.format(source_path))
                is_dir_exist = False
            if not target_path.exists():
                pp('path: {} not exists'.format(target_path))
                is_dir_exist = False

            if is_dir_exist:
                pp('write config file: {}'.format(args.config))
                config['DEFAULT'] = {
                    'source_dir': source_dir,
                    'target_dir': target_dir,
                }
                config.write(configfile)

    source_dir = config.get('DEFAULT', 'source_dir')
    target_dir = config.get('DEFAULT', 'target_dir')
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    pp('source path:', source_path)
    pp('target path:', target_path)

    begin_date = None
    end_date = None
    if b:= args.begin_date:
        begin_date = b
    elif b:= config.get('DEFAULT', 'lastdate', fallback=''):
        begin_date = b

    if begin_date:
        begin_date = date(
            year=2000 + int(b[0:2]),
            month=int(b[2:4]),
            day=int(b[4:6]))
    pp('begin_date:', begin_date)


    new_dir = []
    last_dir = ''
    for i in source_path.iterdir():
        file_datetime = datetime.fromtimestamp(i.stat().st_mtime)#.strftime(args.date_format)
        file_date = file_datetime.date()
        last_dir = file_date.strftime(args.date_format)

        if file_date >= begin_date:
            target_date_path = target_path.joinpath(last_dir)
            pp('copy file', i.resolve(), datetime.fromtimestamp(i.stat().st_mtime), '=>', target_date_path)

            if last_dir not in new_dir:
                new_dir.append(last_dir)

                if not args.is_dry_run and \
                   not target_date_path.exists():
                    pp('create dir', target_date_path)
                    target_date_path.mkdir()

            end_date = file_date
            if not args.is_dry_run:
                shutil.copy2(i, target_date_path)
            else:
                pass

    pp ('create dirs:', ', '.join(new_dir))
    with open(config_path, 'w') as configfile:
        config.set('DEFAULT', 'last_date', last_dir)
        config.write(configfile)
        pp('update last_date:', last_dir)


parser = argparse.ArgumentParser(description='Copy foto from camera to disk')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
parser.add_argument('-c', '--config', dest='config', default='copy-foto.ini', help='config path')
parser.add_argument('-s', '--set-config', dest='set_config', nargs=2, help='set config: source dest')
parser.add_argument('-t', '--dry-run', dest='is_dry_run', action='store_true', help='dry run')
parser.add_argument('-d', '--date-format', dest='date_format', default='%y%m%d', help='set target folder format')
parser.add_argument('-b', '--begin-date', dest='begin_date', help='set begin from date')

args = parser.parse_args()
#conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.config)
#main(conf_path, args)
#print (conf_path)

if __name__ == '__main__':
    main(args)


