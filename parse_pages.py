# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:02:41 2020

@author: Win7
"""

from PyPDF2 import PdfFileWriter, PdfFileReader

input_file = "parcali/isesh2019/43.pdf"
output_file = "a"
endPage = 7


f = open(input_file, "rb")


inputpdf = PdfFileReader(f)
   
output = PdfFileWriter()
for i in range(endPage):
    output.addPage(inputpdf.getPage(i))
with open("parcali/isesh2019/p_1.pdf", "wb") as outputStream:
    output.write(outputStream)
output = PdfFileWriter()
for i in range(endPage,inputpdf.numPages):
    output.addPage(inputpdf.getPage(i))
with open("parcali/isesh2019/p_2.pdf", "wb") as outputStream:
    output.write(outputStream)
f.close()