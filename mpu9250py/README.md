mpu9250py
======================

mpu9250pyは、シリアル入力された加速度(x,y,z)・ジャイロ(x,y,z)・磁気(x,y,z)・温度(t)をリアルタイムで描画します。描画はシリアル入力に同期して行われます。

## 1) 実行環境
[Python](https://www.python.org) 2.7.13で開発しています。

### 1.1) 環境構築 ###
実行環境はネット上の情報などを参考にして、各自の責任で整えてください。<br/>Pythonのバージョンは、<br/>`$ python -V`<br/>で確認できます。

### 1.2) 依存ライブラリ ###
本ツールは以下のライブラリに依存しています。`pip`等でインストールし、Pathを通してください。<br/> `$ pip install パッケージ名`<br/>ライブラリのバージョンは、<br/>`$ pip freeze`<br/>で確認できます。

- numpy 1.12.0
- matplotlib 2.0.0
- pyserial 3.3

## 2) 使用方法
本プログラムの簡単な使用方法を説明します。
### 2.1) シリアルデバイス指定 ###
対象とするシリアルデバイス名を調べます。<br/><br/>Mac: `$ ls /dev/tty.*`<br/>Win: Tera Termに表示されるデバイス名<br/><br/> ***serial.Serial('デバイス名',ボーレート)*** で、デバイス名とボーレートを指定してください。

```
#TODO set serial port, baud rate. e.g. mac:'/dev/tty.usbserial-DJ00M1QE' win:'COM3'
ser = serial.Serial('/dev/tty.usbserial-DJ00M1QE', 115200)
```

### 2.2) 実行 ###
シリアルデバイスを接続し、<br/>`$ python mpu9250py.py`<br/>でプログラムを実行してください。<br/>加速度(x,y,z)・ジャイロ(x,y,z)・磁気(x,y,z)・温度(t)のグラフが表示されます。


### 2.3) 注意点 ###
+ 描画されない場合は、デバイスを差し直して、プログラムを再実行してみてください。
+ グラフの日本語が文字化けする場合は、半角英数で書き直してみてください。
+ センサの電源投入直後は値がおかしい場合があります。少し待ってから再実行してみてください。

## 3) 仕様
2017年3月会で配布されたサンプルプログラムを元に表示仕様を決定しています。入力データの書式は、 **3.5) 参考** 及び、**3月会のサンプルプログラム** を参照してください。

### 3.1) X軸の時間幅 ###
グラフ描画はシリアル入力に同期して行われます。横軸の幅は ***dx*** で設定されています。 ***dx*** はシリアル入力の1周期とするのがおすすめです。

```
class GraphManager:
    """Graph Manager class"""

    #dx:delta Time.
    dx = 0.5
```

### 3.2) グラフの初期化 ###
グラフの初期化は ***GraphManager(軸数)*** で、グラフの軸数を指定してください。

グラフの初期設定は ***setup("グラフ名","軸名(list)",y軸最小値,y軸最大値,表示倍率)*** を適宜修正してください。<br/>軸名は **軸数と同じ個数のリスト** です。

### 3.3) データの更新 ###
データ更新は ***update("int型(list)")*** で設定してくだい。<br/>データは、**軸数と同じ個数のリスト** です。シリアル入力からのデータ取得・パースに失敗した場合、更新はスキップされます。

### 3.4) グラフの描画 ###
加速度ACCから温度Tのデータ取得までを1周期とし、温度Tのデータを取得できた場合にグラフをインタラクティブモードで再描画します。

```
	#replot
	plt.ion()
	plt.pause(0.0001)
```

### 3.5) 参考 ###

#### デフォルトの表示書式 ####

||ラベル|タイトル|単位|範囲|表示倍率|
|:---|:---|:---|:---|:---|:---|
|加速度| ACC |Acceleration|g|-2:2|0.001|
|ジャイロ| GYR |Gyro|°/sec|-250:250|0.25|
|磁気| MAG |Magnetic|uT|-100:100|1|
|温度| T |Temperature|°C|0:50|0.1|


#### 入力データサンプル ####
```
ACC: x: 0009, y: 0020, z: 1034
GYR: x: 0003, y: 0001, z: 0001
MAG: x: 0019, y: 0006, z: 0009
T: 275
ACC: x: 0010, y: 0021, z: 1036
GYR: x: 0002, y: 0000, z: 0001
MAG: x: 0014, y: 0004, z: 0005
T: 276
ACC: x: 0007, y: 0023, z: 1039
GYR: x: 0002, y: 0001, z: 0000
MAG: x: 0012, y: 0007, z: 0004
T: 275
ACC: x: 0013, y: 0022, z: 1041
GYR: x: 0002, y: 0000, z: 0001
MAG: x: 0012, y: 0001, z: 0007
T: 276
ACC: x: 0008, y: 0023, z: 1034
.
.
.
```

## 4)更新履歴

2017/03/23  1.0.0    公開
2017/04/02  1.0.1    グラフタイトルを英語に修正

## 5)ライセンス
Copyright &copy; 2017 IoT研究会<br/>
IoT研究会以外での使用はご遠慮ください。
