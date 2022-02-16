from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.layout import LTRect,LTTextBoxHorizontal,LTText,LTTextLineHorizontal,LTTextBox,LTTextLine,LTChar,LTFigure
from pdfminer.converter import PDFPageAggregator
import io
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter

dosyaadi="Kitaplar/2018/2.pdf"
eksi_sayfa=0
ozet_pages = []
abstract_pages = []
keywords_pages = []
anahtar_pages = []



def is_header(metin,pageNo):
    #print(metin)
    
    
    metin=metin.lower()
    
    abs_ = metin.find("abstract")
    key_ = metin.find("keywords")
    
    ozet_ = metin.find("özet")
    anahtar_ = metin.find("anahtar")
    
    if abs_!=-1:
        abstract_pages.append(pageNo)
        
    if ozet_!=-1:
        ozet_pages.append(pageNo)
        
    if key_!=-1:
        keywords_pages.append(pageNo)
        
    if anahtar_!=-1:
        anahtar_pages.append(pageNo)
                      
                      
#    abs_ = metin.find("abstract")
#    ozet_ = metin.find("anahtar")
#    key_ = metin.find("keywords")
#    int_ = metin.find("introduction")
#    if(abs_ != -1) or (abs_ != -1 and key_ != -1 ) or (abs_ != -1 and int_ != -1 ) or ((abs_ != -1 and ozet_ != -1 )):
#        return True
#    return False
    
                      
def parse_layout(layout):
    abs_=-1
    key_=-1
    metin = ""
    """Function to recursively parse the layout tree."""
    for obj in layout:
        print(obj.__class__.__name__)
        if isinstance(obj, (LTTextBoxHorizontal,LTText,LTTextBox,LTTextLine)):
            for c in obj:
                metin+= (c.get_text().lower())
            
            abs_ = metin.find("abstract")
            key_ = metin.find("keywords")
            
            key_ = metin.find("keywords")
            key_ = metin.find("keywords")

            
            if abs_==-1:
                 metin.find("abstract")
                 
            if key_ ==-1:
                 metin.find("keywords")
                 
                 
                     
        # if it's a container, recurse
        elif isinstance(obj, LTFigure):
            pass
        else:
            pass
    if(abs_ != -1 and key_ != -1 ):
        return True
    return False


    
          

# Open a PDF file.
fp = open(dosyaadi, 'rb')
rsrcmgr = PDFResourceManager()
retstr = io.StringIO()
print(type(retstr))
codec = 'utf-8'
laparams = LAParams()
device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
pages = []
page_no = 0
for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
    interpreter.process_page(page)

    data = retstr.getvalue()
    
    is_header(data,page_no)
    
    
#    if(is_header(data)):
#        pages.append(page_no)
    retstr.truncate(0)
    retstr.seek(0)

    page_no += 1
    
fp.close()

bildiri_sayfa = []

import numpy as np
for abst in abstract_pages:
    ozet_distances = [(x-abst) for x in ozet_pages]
    anahtar_distances = [(x-abst) for x in anahtar_pages]
    keywords_distances = [(x-abst) for x in keywords_pages]
    
    if ( np.any(np.in1d([-1,0,1], ozet_distances)) ) or ( np.any(np.in1d([-1,0,1], keywords_distances)) ):
        if(np.any(np.in1d([-1], ozet_distances))):
            abst = abst -1
        bildiri_sayfa.append(int(abst))
        #print(abst)
    else:
        bildiri_sayfa.append(abst)
from PyPDF2 import PdfFileWriter, PdfFileReader

inputpdf = PdfFileReader(open(dosyaadi, "rb"))
for startPage in range(len(bildiri_sayfa)):
    st = bildiri_sayfa[startPage]
    if st == bildiri_sayfa[-1]:
        endPage = inputpdf.numPages-eksi_sayfa
    else:
        endPage=bildiri_sayfa[startPage+1]
    output = PdfFileWriter()
    for i in range(st,endPage):
        
        output.addPage(inputpdf.getPage(i))
    with open("Parcali/incos2018/%s.pdf" % startPage, "wb") as outputStream:
        output.write(outputStream)