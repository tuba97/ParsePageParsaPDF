# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 13:08:02 2020

@author: Win7
"""

from PyPDF2 import PdfFileWriter, PdfFileReader


input_file = "Kitaplar/2018/3.pdf"
output_file = "a"
pageNo = 12


f = open(input_file, "rb")
inputpdf = PdfFileReader(f)
page = inputpdf.pages[pageNo]
for o in page.getObject():
    print(type(o))
    for i in o:
        print(type(i))
        print(i)
    print(o.__class__.__name__)
f.close()   