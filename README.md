recagqr.py
============

agqrの番組を録画するためのプログラム

[agqr.rb](https://gist.github.com/ybenjo/9904543) をPythonに書き直して手を加えた．

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
`time_diff()`用のtestdoc

  `python -m doctest -v doctest.txt` で実行
  
## crontab.bk
crontabの設定ファイルのバックアップ

`contab -e` でcrontabに設定後，以下のコマンドを実行して生成する．

```sh
crontab -l > crontab.bk
```

crontab に指定するコマンドは絶対パスで指定しないとエラーになる．

```sh
MAILTO=""
29,59 * * * * python3 /path/to/recagqr.py >> /path/to/cron.log
```

# その他メモ
## 実行ログの確認

```sh
tail /var/log/syslog
tail ~/RTMPDump/cron.log
```

## Windowsにファイルを転送する
Ubuntu の nautilus の 「サーバーへ接続」で `smb://192.168.11.3` などと入力して Windows に接続，手動でファイルを移す．


# リンク

- [超！A&G | AM1134kHz 文化放送 JOQR](http://www.agqr.jp/index.php)
- [agqr.rb](https://gist.github.com/ybenjo/9904543)
