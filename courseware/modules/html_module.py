import json

## TODO: Abstract out from Django
from django.conf import settings
from mitxmako.shortcuts import render_to_response, render_to_string

from x_module import XModule
from lxml import etree

class Module(XModule):
    id_attribute = 'filename'

    def get_state(self):
        return json.dumps({ })

    @classmethod
    def get_xml_tags(c):
        return ["html"]
        
    def get_html(self):
        if self.filename==None:
            xmltree=etree.fromstring(self.xml)
            textlist=[xmltree.text]+[etree.tostring(i) for i in xmltree]+[xmltree.tail]
            textlist=[i for i in textlist if type(i)==str]
            return "".join(textlist)
        try: 
            filename=settings.DATA_DIR+"html/"+self.filename
            return open(filename).read()
        except: # For backwards compatibility. TODO: Remove
            return render_to_string(self.filename, {'id': self.item_id})

    def __init__(self, xml, item_id, ajax_url=None, track_url=None, state=None, track_function=None, render_function = None):
        XModule.__init__(self, xml, item_id, ajax_url, track_url, state, track_function, render_function)
        xmltree=etree.fromstring(xml)
        self.filename = None
        filename_l=xmltree.xpath("/html/@filename")
        if len(filename_l)>0:
            self.filename=str(filename_l[0])
