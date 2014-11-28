#!/usr/bin/env python
# -*- coding: utf-8 -*-

# agqrを録画したい
# https://gist.github.com/ybenjo/682efbf3829724743727

import yaml
import datetime

if __name__ == '__main__':
    rtmpdump = '~/RTMPDump/rtmpdump'
    agqr_stream_url = 'rtmp://fms-base1.mitene.ad.jp/agqr/aandg22'
    save_dir = "./recdata"
    schedule = "./schedule.yaml"
    avconv = '/usr/bin/avconv'
    now = datetime.datetime.today()

    wday = dict()
    for n, wday_jp in enumerate(list(u'日月火水木金土')):
        wday[wday_jp] = n

    with open(schedule, 'r') as f:
        schedule_yaml = yaml.load(f)

    for program in schedule_yaml:
        program_wday = wday[program['wday']]
        length = program['length'] * 60 + 15
        title = '_'.join([program['title'], now.strftime('%Y%m%d')])

        # # codecはデフォルトでmp4にする
        # if 'codec' in program:
        #     codec = program['codec']
        # else:
        #     codec = 'mp4'

        path_dict = {
            'avconv' : avconv,
            'flv_path' : '{0}/{1}.flv'.format(save_dir, title),
            'mpeg_path' : '{0}/{1}.{2}'.format(save_dir, title, codec)
        }

        rec_command = '{0} -r {1} --live -B {2} -o {flv_path}'\
            .format(rtmpdump, agqr_stream_url, length, **path_dict)
        # encode_command = '{avconv} -i {flv_path} --codec copy {mpeg_path}'\
        #     .format(**path_dict)

        print rec_command
        print encode_command
        print ''
