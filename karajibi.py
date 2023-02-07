import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

ZEN = "".join(chr(0xff01 + i) for i in range(94))
HAN = "".join(chr(0x21 + i) for i in range(94))
ZEN2HAN = str.maketrans(ZEN, HAN)


def toHan(s):
    return s.translate(ZEN2HAN)


def toInt(s):
    return int(re.search(r'\d+', toHan(s)).group(0))


def getNums():
    res = requests.get("https://ssc3.doctorqube.com/karajibi/")
    soup = BeautifulSoup(res.text)
    smpcurrent = soup.find(id="smpcurrent")
    callnum = toInt(smpcurrent.contents[1].contents[1])  # 呼出番号
    waitnum = toInt(smpcurrent.contents[2].contents[1])  # 待ち人数
    waitmin = toInt(smpcurrent.contents[6].contents[1].string)  # 次にお取りできる順番での目安待ち時間
    return (callnum, waitnum, waitmin)


def doit():
    callnum, waitnum, waitmin = getNums()
    print("%s, %d, %d, %d" % (datetime.now().isoformat(), callnum, waitnum, waitmin))


def main():
    doit()


if __name__ == "__main__":
    main()
