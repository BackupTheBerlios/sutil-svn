# -*- coding: utf-8 -*-
""" srtLoader.py

 Subtitles movies interface. Movie class contains a list of lines. A movie can load and save
both SRT and XML formats.
"""
__copyright__ = "Copyright (c) 2006 Free Software Foundation, Inc."
__license__ = """
Sutil is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

Sutil is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place - Suite 330, Boston, MA 02111-1307, USA. """

import xml.dom.minidom

class Line:
       def __init__(self, number, stime, etime, text, translation=''):
              self.number = number
              self.stime = stime
              self.etime = etime
              self.text = text
              self.translation = translation

       def serialize_to_xml(self):
              return """    <line number=\"%i\">
       <startTime>%s</startTime>
       <endTime>%s</endTime>
       <originalText>%s</originalText>
       <translation>%s</translation>
   </line>\n""" % (self.number, self.stime, self.etime,
                   self.get_text(), self.translation)

       def serialize_to_srt(self):
              try:
                     return """%i
%s --> %s
%s\n\n""" % (self.number, self.stime, self.etime,self.get_translation())
              except UnicodeDecodeError,e:
                     print e

       def get_text(self):
              return self.text

       def set_translation(self, trans):
              self.translation = trans

       def get_translation(self):
              if ( not self.translation ):
                     return "* " + self.get_text()
              else:
                     return self.translation


class Movie:
       def __init__(self):
              self.lines = []
              self.movieFilename = ""

       def set_movie_filename(self, filename):
              self.movieFilename = filename

       def append_line(self, line):
              self.lines.append(line)

       def serialize_to_xml(self):
              text =  "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
              text += "<movie file=\"" + self.movieFilename + "\">"
              for line in self.lines:
                     text += line.serialize_to_xml()
              text += "</movie>"
              return text

       def serialize_to_srt(self):
              text = ''
              for line in self.lines:
                     text += line.serialize_to_srt()
              return text

       def get_text(self, position):
              if ( position < 1 or position > len(self.lines)):
                     return ""
              return self.lines[position-1].get_text()

       def get_translation(self, position):
              if ( position < 1 or position > len(self.lines)):
                     return ""
              return self.lines[(position-1)].translation

       def set_translation(self, position, translation):
              self.lines[(position-1)].set_translation(translation)
       

       def load_srt(self, subfile):
              srtfile = open(subfile).read().replace('\r','')
              clean = str.split(srtfile, '\n\n')
              clean = filter(None, map(str.strip, clean))
              for sub in clean:
                     sub = sub.split('\n')
                     number = int(sub[0])
                     stime, etime = sub[1].split(' --> ')
                     lines = sub[2:]
                     if ( len(lines) > 1 ):
                            text = '\n'.join(sub[2:])
                     else:
                            text = sub[2]
                     self.append_line(Line(number, stime, etime, text))
              return self

       def getElement(self, document, element):
              d = document.getElementsByTagName(element)[0].firstChild
              if d != None :
                     if ( d.nodeType == d.ELEMENT_NODE):
                            return d.toxml()
                     else:
                            return d.data
              else:
                     return ""

       def load_xml(self, subfile):
              raw_xml = open(subfile,'r').read()
              dom = xml.dom.minidom.parseString(raw_xml) 
              lines = dom.getElementsByTagName('line') 
              for line in lines:
                     number = int(line.getAttribute('number'))
                     stime = self.getElement(line, 'startTime')
                     etime = self.getElement(line, 'endTime')
                     originalText = self.getElement(line, 'originalText')
                     translation = self.getElement(line, 'translation')
                     self.append_line(Line(number, stime, etime,
                                           originalText, translation))
              return self

       
if ( __name__ == '__main__'):
       movie = Movie()
       movie.load_srt('test.srt')
       output = open('tmp-test.delete.me','w')
       output.write(movie.serialize_to_xml())
       output.close()
       movie2 = Movie()
       movie2.load_xml('test.sml')
       print movie2.serialize_to_srt().encode('utf-8')
