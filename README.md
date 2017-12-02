# ComeKatsuBDM

## requirements
- MySQL-python
- simple-db-migrate
- nfcpy
- PyMySQL

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
    - input_id
        - ラズパイのこのroomに対する入力ポートのID
    - output_id
        - ラズパイのこのroomに対する出力ポートのID

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
