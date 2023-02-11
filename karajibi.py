import requests
import re
import os.path as p
from datetime import datetime
import json
import time

ZEN = "".join(chr(0xff01 + i) for i in range(94))
HAN = "".join(chr(0x21 + i) for i in range(94))
ZEN2HAN = str.maketrans(ZEN, HAN)


def toHan(s):
    return s.translate(ZEN2HAN)


def toInt(s):
    return int(re.search(r'\d+', toHan(s)).group(0))


def getNums():
    callnum = -1  # 呼出番号
    waitnum = -1  # 待ち人数
    waitmin = -1  # 次にお取りできる順番での目安待ち時間

    try:
        res = requests.get("https://ssc3.doctorqube.com/karajibi/")
    except requests.exceptions.ConnectionError:
        return (callnum, waitnum, waitmin)




    f_call = False
    f_waitnum = False
    f_waittime = False
    for tag_text in re.finditer(r"<(.*?)>(.*?)(?=<)", res.text):
        txt = tag_text.group(2)
        #print(tag_text)
        if f_call:
            callnum = toInt(txt)  # 呼出番号
        elif f_waitnum:
            waitnum = toInt(txt)  # 待ち人数
        elif f_waittime:
            waitmin = toInt(txt)  # 次にお取りできる順番での目安待ち時間
            break
        if txt == '呼出番号':
            f_call = True
        elif txt == '待ち人数':
            f_waitnum = True
        elif txt == '次にお取りできる順番での目安待ち時間':
            f_waittime = True
        else:
            f_call = False
            f_waitnum = False
            f_waittime = False
    return (callnum, waitnum, waitmin)


def jsondump(fn, datas):
    txt = json.dumps(datas)
    txt = txt.replace("],", "],\n")
    open(fn, 'w').write(txt)

def writeFile(fn, newData):
    datas = []
    if p.isfile(fn):
        datas = json.load(open(fn, 'r'))
    if type(datas) != list:
        datas = []
    if not datas or datas[-1][1:] != newData[1:]:
        datas.append(newData)
        #json.dump(datas, open(fn, 'w'), indent=1)
        jsondump(fn, datas)
        return True
    return False


def isoDateToTxt(d):
    d = datetime.fromisoformat(d)
    return d.astimezone().replace(tzinfo=None).isoformat(" ")


def doit():
    FN = "karajibi.json"
    toCSV(FN)

    i_sec = 10  # interval sec
    # loop num
    n_min = int(60 / i_sec)
    n_hour = n_min * 60
    n_day = n_hour * 24
    for i in range(n_day):
        callnum, waitnum, waitmin = getNums()
        ts = datetime.now().astimezone().isoformat()
        data = [ts, callnum, waitnum, waitmin]
        if writeFile(FN, data):
            #print(json.dumps(data))
            data[0] = isoDateToTxt(data[0])
            print("%s, %d, %d, %d" % tuple(data))

        time.sleep(10)


def toCSV(fn):
    datas = json.load(open(fn, 'r'))
    for data in sorted(datas):
        data[0] = isoDateToTxt(data[0])
        print("%s, %d, %d, %d" % tuple(data))


def main():
    doit()


if __name__ == "__main__":
    main()
