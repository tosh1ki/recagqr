recagqr: AGQR の番組を録画する
============

[agqr.rb](https://gist.github.com/ybenjo/9904543) を Python に書き直して手を加えた．

# ファイルの説明
## recagqr.py
実際に録画をするプログラム

## schedule.yaml
予約設定ファイル

例えば『井口裕香のむ〜〜〜ん ⊂（　＾ω＾）⊃』を録画したい場合は以下のようにする．

```yaml
- title: mu_n
  wday: 月
  time: '22:00'
  length: 60
```

## doctest.txt
`time_diff()` 用の testdoc

`python3 -m doctest -v doctest.txt` で実行
  
## crontab.bk
crontab の設定ファイルのバックアップ

`crontab -e` で crontab に設定後，以下のコマンドを実行して生成する．

```sh
crontab -l > ~/crontab.bk
```

# 各種設定など
## crontab の設定
以下のように crontab を設定しておく．

```sh
MAILTO=""
29,59 * * * * python3 /path/to/recagqr.py --schedule /path/to/schedule.yaml --savedir /path/to/recdata >> ~/cron-recagqr.log
```

## 実行ログの確認

```sh
tail /var/log/syslog
tail ~/cron-recagqr.log
```

# リンク

- [超！A&G | AM1134kHz 文化放送 JOQR](http://www.agqr.jp/index.php)
- [agqr.rb](https://gist.github.com/ybenjo/9904543)
