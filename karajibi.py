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


def getNums_old():
    res = requests.get("https://ssc3.doctorqube.com/karajibi/")
    soup = BeautifulSoup(res.text)
    smpcurrent = soup.find(id="smpcurrent")
    callnum = toInt(smpcurrent.contents[1].contents[1])  # 呼出番号
    waitnum = toInt(smpcurrent.contents[2].contents[1])  # 待ち人数
    waitmin = toInt(smpcurrent.contents[6].contents[1].string)  # 次にお取りできる順番での目安待ち時間
    return (callnum, waitnum, waitmin)


def getNums():
    res = requests.get("https://ssc3.doctorqube.com/karajibi/")
    """
[<re.Match object; span=(5, 26), match='<div id="smpcurrent">'>,
 <re.Match object; span=(26, 29), match='<p>'>,
 <re.Match object; span=(29, 32), match='<b>'>,
 <re.Match object; span=(32, 59), match='<font color="green">【午前の順番】'>,
 <re.Match object; span=(59, 66), match='</font>'>,
 <re.Match object; span=(66, 70), match='</b>'>,
 <re.Match object; span=(70, 74), match='</p>'>,
 <re.Match object; span=(74, 102), match='<p class="nowinfo waitlist">'>,
 <re.Match object; span=(102, 142), match='<p class="aroundline6 aroundnarrow">呼出番号'>,
 <re.Match object; span=(142, 149), match='</p>２３番'>,
 <re.Match object; span=(149, 156), match='</span>'>,
 <re.Match object; span=(156, 160), match='</p>'>,
 <re.Match object; span=(160, 188), match='<p class="nowinfo waitlist">'>,
 <re.Match object; span=(188, 228), match='<p class="aroundline6 aroundnarrow">待ち人数'>,
 <re.Match object; span=(228, 235), match='</p>１９人'>,
 <re.Match object; span=(235, 242), match='</span>'>,
 <re.Match object; span=(242, 246), match='</p>'>,
 <re.Match object; span=(246, 250), match='<p>\u3000'>,
 <re.Match object; span=(250, 254), match='</p>'>,
 <re.Match object; span=(254, 283), match='<p class="nowinfo">次にお取りできる番号'>,
 <re.Match object; span=(283, 307), match='<span>予定数に達したため受付を終了しました'>,
 <re.Match object; span=(307, 314), match='</span>'>,
 <re.Match object; span=(314, 318), match='</p>'>,
 <re.Match object; span=(318, 355), match='<p class="nowinfo">次にお取りできる順番での目安待ち時間'>,
 <re.Match object; span=(355, 364), match='<span>１０５'>,
 <re.Match object; span=(364, 372), match='</span>分'>,
 <re.Match object; span=(372, 376), match='</p>'>,
 <re.Match object; span=(376, 380), match='<p>\u3000'>,
 <re.Match object; span=(380, 384), match='</p>'>]
"""
    callnum = -1  # 呼出番号
    waitnum = -1  # 待ち人数
    waitmin = -1  # 次にお取りできる順番での目安待ち時間

    f_call = False
    f_waitnum = False
    f_waittime = False
    for tag_text in re.finditer(r"<(.*?)>(.*?)(?=<)", res.text):
        txt = tag_text.group(2)
        print(tag_text)
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


def doit():
    callnum, waitnum, waitmin = getNums()
    print("%s, %d, %d, %d" % (datetime.now().isoformat(), callnum, waitnum, waitmin))


def main():
    doit()


if __name__ == "__main__":
    main()
