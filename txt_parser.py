# coding: utf-8
import json
import re
import uuid

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


class TxtParser(object):
    def __init__(self, template):
        self.template = template

    def parse(self, in_data):
        return {k.encode('utf-8'): self._parse(v, in_data) for k, v in self.template.items()}

    @staticmethod
    def _parse(pattern, in_data):
        res = re.match(pattern.encode('utf-8'), in_data)
        if res:
            return ''.join(res.groups()[1:])
        else:
            return ''


employee_stocks = {
    u'资金总额': u"([^x00-xff]|[x00-xff])*本员工持股计划筹集资金总额上限为[^x00-xff]{1}([0-9.,]+) ([^x00-xff]{6})",
    u'资管总额': u"([^x00-xff]|[x00-xff])*资产管理计划份额上限为[^x00-xff]{1}([0-9.,]+) ([^x00-xff]{6})",
    u'价格': u"([^x00-xff]|[x00-xff])*收盘价[^x00-xff]{1}([0-9.,]+) ([^x00-xff]{7})",
    u'比例': u"([^x00-xff]|[x00-xff])*占公司现有股本总额约为[^x00-xff]{1}([0-9.%]+)",
    u'锁定期': u"([^x00-xff]|[x00-xff])*锁定期为[^x00-xff]{1}([0-9.%]+)[^x00-xff]{2}([^x00-xff]{6})",
    u'购买方式': u"([^x00-xff]|[x00-xff])*通过(二级市场)购买",
    u'日期': u"([^x00-xff]|[x00-xff])*\n([0-9]+) (年) ([0-9]+) (月) ([0-9]+) (日)\n"
}

# 转换成txt文件
pdf_file = '/home/zhou/1202857140.PDF'
tmp_txt_file = str(uuid.uuid4())
out_fp = open(tmp_txt_file, 'w')
rsrcmgr = PDFResourceManager(caching=False)

in_fp = open(pdf_file, 'rb')
device = TextConverter(rsrcmgr, out_fp, codec='utf-8', laparams=LAParams(), imagewriter=None)
interpreter = PDFPageInterpreter(rsrcmgr, device)

for page in PDFPage.get_pages(in_fp, set(), maxpages=0, password='', caching=False, check_extractable=True):
    page.rotate = (page.rotate + 0) % 360
    interpreter.process_page(page)

in_fp.close()
out_fp.close()

# 提取需要信息
txt = TxtParser(employee_stocks)
fp = open(tmp_txt_file, 'r')
data = fp.read()
res = json.dumps(txt.parse(data), indent=4, ensure_ascii=False)
print res
print type(res.decode('utf-8'))
