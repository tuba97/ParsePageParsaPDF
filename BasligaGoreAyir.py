# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 16:29:12 2020

@author: Win7
"""

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer


def createPDFDoc(fpath):
    fp = open(fpath, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise "Not extractable"
    else:
        return document


def createDeviceInterpreter():
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    return device, interpreter

font_sayilari = []

def parse_obj(objs):
    last_font_size=0
    metin=""
    for obj in objs:
        if isinstance(obj, pdfminer.layout.LTTextBox):
            for o in obj._objs:
                if isinstance(o,pdfminer.layout.LTTextLine):
                    text=o.get_text()
                    if text.strip():
                        for c in  o._objs:
                            if isinstance(c, pdfminer.layout.LTChar):
                                if(c.size==last_font_size):
                                    metin = metin + c.get_text()
                                    
                                else:
                                    if(len(metin) > 3 and last_font_size>=24):
                                       return True
#                                    print(last_font_size)
#                                    print(metin)
                                    metin=""
                                last_font_size=c.size
                                
        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs)
        else:
            pass
    return False

input_file = "Kitaplar/2017/6.pdf"
output_file = "a"
pageNo = 33
fp = open(input_file, 'rb')
document=createPDFDoc(input_file)
bildiri_sayfalari=[]
device,interpreter=createDeviceInterpreter()
for pageNumber, page in enumerate(PDFPage.create_pages(document)):
#    if pageNumber==pageNo:
    interpreter.process_page(page)
    layout = device.get_result()
    if(parse_obj(layout._objs)):
        bildiri_sayfalari.append(pageNumber)


from PyPDF2 import PdfFileWriter, PdfFileReader
eksi_sayfa=0
inputpdf = PdfFileReader(open(input_file, "rb"))
for startPage in range(len(bildiri_sayfalari)):
    st = bildiri_sayfalari[startPage]
    if st == bildiri_sayfalari[-1]:
        endPage = inputpdf.numPages-eksi_sayfa
    else:
        endPage=bildiri_sayfalari[startPage+1]
    output = PdfFileWriter()
    for i in range(st,endPage):
        
        output.addPage(inputpdf.getPage(i))
    with open("Parcali/udcs2017/%s.pdf" % startPage, "wb") as outputStream:
        output.write(outputStream)