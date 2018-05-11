# ComeKatsuBDM

## 起動
```
$ ssh pi@{ip adress}
 password: fukuoka
$ cd Develop/ComeKatsuBDM
$ python main.py
```

## トラブルシューティング
- OperationalError: (2013, ‘Lost connection to MySQL server during query’)
 - ctrl + Cでプロセスを落として再起動してください

## requirements
- MySQL-python
- simple-db-migrate
- nfcpy
- PyMySQL
- pyserial
- Rpi.GPIO

## db setup
```
$ db-migrate
```

## tables
- umbrellas
    - in_room
        - 傘立てに入っているかどうか
    - nfc_id
    - room_id
- nfcs
    - tag_id
        - nfcから読み込める特有のID
- rooms (傘立ての穴)
    - switch_port
        - スイッチのポート番号
    - locked_led_port
        - ルームが埋まってる時に光らせるLEDのポート番号
    - unlocked_led_port
        - 傘を取れる状態のときに光らせるLEDのポート番号

## example
### input.py
傘立てに傘が入った時に動くプログラム
(デバイスとの繋ぎこみはまだ)
```
$ python input.py
1   // port_idを入力
tag0    // tag_idを入力
{u'room_id': 1, u'id': 6, u'in_room': 1, u'nfc_id': 5}  // 保存されたumbrellaが出力される
success!
```

### output.py
ユーザが傘を取るためにnfcをタップした時に動くプログラム(デバイスとの繋ぎこみはまだ)
```
$ python output.py
tag0    // tag_idを入力
{u'room_id': 1, u'id': 6, u'in_room': 1, u'nfc_id': 5}  // 対応するumbrellaが出力される
success!
```
