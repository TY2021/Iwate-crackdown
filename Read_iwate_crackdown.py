# coding: utf-8
import urllib3
import sys
import datetime
import schedule
import time
import locale
import re
import mojimoji
import csv
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def job():
    url = "http://www2.pref.iwate.jp/~hp0802/oshirase/kou-sidou/torishimari/torishimari.pdf"
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    pre_line = ""
    pre_filter_time = ""
    weekday_list = ["月","火","水","木","金","土","日"]
    today_flag = 0
    not_write_flag = 0
    morioka_takizawa_count = 0
    rsrcmgr = PDFResourceManager()
    rettxt = StringIO()
    laparams = LAParams()
    request_methods = urllib3.PoolManager()
    response = request_methods.request('GET', url)

    fp = open('torishimari.pdf', 'wb')
    fp.write(response.data)
    fp.close()

    # 縦書き文字を横並びで出力する
    laparams.detect_vertical = True
    device = TextConverter(rsrcmgr, rettxt, codec='utf-8', laparams=laparams)

    # 処理するPDFを開く
    fp = open('torishimari.pdf', 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # maxpages：ページ指定（0は全ページ）
    for page in PDFPage.get_pages(fp, pagenos=None, maxpages=0, password=None,caching=True, check_extractable=True):
        interpreter.process_page(page)
        sentence = rettxt.getvalue()

    file = open('pdf.txt', 'w')
    file.write(sentence)

    fp.close()
    device.close()
    rettxt.close()
    file.close()

    fp = open('pdf.txt')
    lines = fp.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    fp.close()

    # lines: リスト。要素は1行の文字列データ
    for line in lines:
        #今日の取り締まりリスト化どうか判断 日中か夜間かも判断
        if re.search('(\d{1,2})月(\d{1,2})日',line) is not None:
            date = re.search('(\d{1,2})月(\d{1,2})日',line)
            pdf_month = mojimoji.zen_to_han(date.group(1))
            pdf_day = mojimoji.zen_to_han(date.group(2))
            pdf_month = int(pdf_month)
            pdf_day = int(pdf_day)
            if pdf_month == month and pdf_day == day:
                today_flag = 1
            else:
                today_flag = 0
        if line.find("日中") > 0:
            filter_time = "日中\n"
        elif line.find("夜間") > 0:
            filter_time = "夜間\n"

    crack_read = open("crackdown_statistics.csv", "r")
    crack_lines = csv.reader(crack_read)
    crack_write = open("crackdown_statistics.csv", "a", encoding="utf_8", errors="", newline="" )
    writer = csv.writer(crack_write)

    for line in lines:
        #取り締まりの内容抜き出し
        if re.search('(\d{1,2})月(\d{1,2})日',line) is not None:
            date = re.search('(\d{1,2})月(\d{1,2})日',line)
            pdf_month = mojimoji.zen_to_han(date.group(1))
            pdf_day = mojimoji.zen_to_han(date.group(2))
            pdf_month = int(pdf_month)
            pdf_day = int(pdf_day)
            pdf_day_of_week = weekday_list[datetime.date(year, pdf_month, pdf_day).weekday()]
            date = line.strip()
            if pdf_month == month and pdf_day == day:
                today_flag = 1
            else:
                today_flag = 0
        if line.find("日中") > 0:
            filter_time = "日中"
        elif line.find("夜間") > 0:
            filter_time = "夜間"

        #取り締まりリストを書き込み
        if (line.find("○") > 0 and line.find("道") > 0):
            if(pre_line != line):
                if pre_filter_time != filter_time:
                    pre_filter_time = filter_time
                date_csv = str(year) + '/' + str(pdf_month) + '/' + str(pdf_day)
                day_of_week_csv = pdf_day_of_week.strip()
                time_csv = filter_time.strip()
                area_csv = line.strip()
                area_csv = area_csv.strip('○')
                area_csv = area_csv.lstrip()
                for crack_line in crack_lines:
                    if date_csv == crack_line[0]:
                        not_write_flag = 1
                        break
                if not_write_flag != 1:
                    writer.writerow([date_csv,day_of_week_csv,time_csv,area_csv])
                not_write_flag = 0
                pre_line = line

    crack_read.close()
    crack_write.close()

job()
