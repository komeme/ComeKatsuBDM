# ComeKatsuBDM

## 五月祭展示してくれる人向けの説明書

## 起動
1. ケーブルが正しく接続されているか確認
    - ステレオケーブル
    - Felica リーダー
    - LANケーブル
2. 電源ケーブルを接続してラズパイを起動
3. ラズパイに接続されたPCから以下のコマンドを実行して接続
```
$ ssh pi@{ip adress}
 password: (別途共有します)
 ```
 - ssh に必要なpasswordは別途連絡します！
 4. 接続できたら以下のコマンドを打って実行
 ```
$ cd Develop/ComeKatsuBDM
$ sudo python main.py
```
- `sudo`コマンドを忘れないように！ 

5. 使用後は `Ctrl` + `c` で終了

## トラブルシューティング
- OperationalError: (2013, ‘Lost connection to MySQL server during query’)
    - ctrl + Cでプロセスを落として再起動してください
 
## ポート対応表

|回路側|ラズパイ側|
|:---:|:---:|
| A | GND |
| B | 16 | 
| C | GND | 
| D | 20 | 
| E | GND | 
| F | 13 | 
| G | GND | 
| H | 19 | 
| I | 5V | 
| J | 21 | 
| K | GND | 
| L | 5V | 
| M | 26 | 
| N | GND | 

- 差し込むポートを間違えるとラズパイはすぐに壊れてしまうので、再接続の際は特に注意してください！
- ポートを結ぶコードは大変抜けやすくなっています！運搬の際は注意してください！

## 以下、仕様書(五月祭担当者は見なくていいです)

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
