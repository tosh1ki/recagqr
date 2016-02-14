#!/usr/bin/env python
# -*- coding: utf-8 -*-


__doc__ = '''Record AGQR

Usage:
    recagqr.py --schedule <schedule> --savedir <savedir> [--rtmpdump <rtmpdump>]

Options:
    --schedule <schedule>  path of schedule file of yaml format
    --savedir <savedir>  path of output directory
    --rtmpdump <rtmpdump>  (optional) path of rtmpdump [default: /usr/local/bin/rtmpdump]
'''


import subprocess
import yaml
import time
import datetime as dt
from docopt import docopt


def time_diff(t1, t2):
    ''' 時刻 t1, t2 の差を計算する．
    t1 > t2 の場合を考慮しているので面倒なことをしている．
    '''
    dt1 = dt.datetime(2011, 1, 1, t1.hour, t1.minute, t1.second)
    dt2 = dt.datetime(2011, 1, 1, t2.hour, t2.minute, t2.second)
    dt3 = dt.datetime(2011, 1, 2, t2.hour, t2.minute, t2.second)

    # min(key=abs)だとなぜか正しく動作しない
    return min(map(abs, [dt3 - dt1, dt2 - dt1]))


if __name__ == '__main__':

    # コマンドライン引数の取得
    args = docopt(__doc__)
    rtmpdump = args['--rtmpdump']
    schedule = args['--schedule']
    save_dir = args['--savedir']

    agqr_stream_url = 'rtmp://fms-base1.mitene.ad.jp/agqr/aandg22'

    wday = dict(zip(tuple('月火水木金土日'), range(7)))
    datetime_now = dt.datetime.today()

    with open(schedule, 'r') as f:
        schedule_yaml = yaml.load(f)

    # 60秒前にcronが起動するので45秒sleepさせておく
    # ちょうどCM一本分の余裕になる(はず)
    time.sleep(45)

    for program in schedule_yaml:
        hour, minute = map(int, program['time'].split(':'))
        program_wday = wday[program['wday']]
        program_time = dt.time(hour, minute, 0)

        # 0:00に始まる番組だった場合:
        if hour == 0 and minute == 0:
            next_wday = (datetime_now.weekday() + 1) % 7
            is_appropriate_wday = (program_wday == next_wday)
            program_date = datetime_now.date() + dt.timedelta(days=+1)
        else:
            is_appropriate_wday = (program_wday == datetime_now.weekday())
            program_date = datetime_now.date()

        # 番組が2分以内に始まる/始まったか?
        is_appropriate_time \
            = time_diff(datetime_now.time(), program_time) < dt.timedelta(minutes=2)

        if is_appropriate_wday and is_appropriate_time:
            program_start = dt.datetime.combine(program_date, program_time)
            length = str(program['length'] * 60)
            title = program_date.strftime('%Y%m%d') + '_' + program['title']
            path = '{0}/{1}.flv'.format(save_dir, title)
            rec_command = [rtmpdump, '--quiet', '-r', agqr_stream_url,
                           '--live', '-B', length, '-o', path]
            print(' '.join(rec_command))

            retval = subprocess.Popen(rec_command,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

            break
