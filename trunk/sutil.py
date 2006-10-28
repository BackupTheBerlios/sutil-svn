#!/usr/local/bin/python
# -*- coding: utf-8 -*-

""" sutil.py

 Main program and callbacks to gtk interface.
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



import pygtk
pygtk.require('2.0')
import gtk
import gobject
import gettext
import pango
from sys import argv

import os.path
import srtLoader
from saveconfirm import SaveConfirmationAlert
from dialogProject import NewProjectDialog
from gazpacho.loader.loader import ObjectBuilder

wt = ObjectBuilder('ui-v1.xml')

class Controller:

    def __init__(self):
        self.counter = 1
        self.movie = srtLoader.Movie()
        wt.get_widget('spinCurrentLine').set_value(0)
        wt.get_widget('hbox2').set_sensitive(False)
        wt.get_widget('tvOriginal2').get_buffer().create_tag("bold",
                                                             weight=pango.WEIGHT_BOLD)
        wt.get_widget('tvTranslation2').get_buffer().create_tag("bold",
                                                             weight=pango.WEIGHT_BOLD)
        wt.get_widget('tvTranslation2').set_overwrite(False)  
        self.unsaved_changes = False

    def pretty_title(self, filename):
        file = os.path.basename(filename)
        if ( len(file) > 20 ):
            return file[:25] + "..."
        return file

    def initialization_at_load(self, loadedFile):
        wt.get_widget('window1').set_title("Sutil - "
                                           + self.pretty_title(loadedFile))
        total = len(self.movie.lines)
        wt.get_widget('spinCurrentLine').set_range(1,total)
        wt.get_widget('labelLinesNumber').set_text('de ' + str(total))
        wt.get_widget('hbox2').set_sensitive(True)
        wt.get_widget('Save').set_sensitive(True)
        wt.get_widget('SaveAs').set_sensitive(True)
        wt.get_widget('ExportSRT').set_sensitive(True)
        self.unsaved_changes = False
        
    def load_srt_file(self, filename):
        self.movie = srtLoader.Movie()
        self.outputFilename = ""
        self.movie.load_srt(filename)
        self.initialization_at_load(filename)

    def load_sml_file(self, filename):
        self.movie = srtLoader.Movie()
        self.outputFilename = filename
        self.movie.load_xml(filename)
        self.initialization_at_load(filename)

    def save_project_as(self):
        dialog = gtk.FileChooserDialog("Save as...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        response = dialog.run()
        if response == gtk.RESPONSE_OK :
            self.outputFilename = dialog.get_filename()
            self.write_to_file(dialog.get_filename(),
                               self.movie.serialize_to_xml())
            dialog.destroy()
            return True
        else:
            dialog.destroy()
            return False

    def save_project(self):
        if ( self.check_unsaved_changes()):
            try:
                if self.outputFilename :
                    self.write_to_file(self.outputFilename,
                                       self.movie.serialize_to_xml())
                    return True
                else:
                    return self.save_project_as()
            except AttributeError:
                return self.save_project_as()
        else:
            print "Nothing new to save"
            return True


    def export_to_srt(self):
        dialog = gtk.FileChooserDialog("Export to...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        response = dialog.run()
        if response == gtk.RESPONSE_OK :
            self.outputFilename = dialog.get_filename()
            self.write_to_file(dialog.get_filename(),
                               self.movie.serialize_to_srt())
        dialog.destroy()


    def load_movie(self, filename):
        warning = gtk.MessageDialog(None, 0,
                                    gtk.MESSAGE_WARNING,
                                    gtk.BUTTONS_CLOSE,
                                    "Todavia no esta disponible la visualizacion de video")
        warning.run()
        warning.destroy()

    def write_to_file(self, outputFilename, content):
        output = open(outputFilename,'w')
        output.write(content)
        output.close()
        self.unsaved_changes = False
        print "Project saved."

    def set_text_in_textview(self, widgetName, text, bold=False, labeled=False):
        buffer = wt.get_widget(widgetName).get_buffer()
        buffer.set_text(text)
        begin, end = buffer.get_bounds()
        if bold:
            buffer.apply_tag_by_name("bold", begin, end)
        if labeled:
            buffer.place_cursor(buffer.get_iter_at_offset(3))
        buffer.set_modified(False)
        wt.get_widget(widgetName).set_buffer(buffer)

    def get_text_in_textview(self, widgetName):
        buffer = wt.get_widget(widgetName).get_buffer()
        if ( buffer == None):
            return ""
        beginIter, endIter = buffer.get_bounds()
        return buffer.get_text(beginIter, endIter)

    def print_line(self, lineToTranslate):

        self.set_text_in_textview('tvOriginal1',
                                  self.movie.get_text(lineToTranslate-1))
        self.set_text_in_textview('tvOriginal2',
                                  self.movie.get_text(lineToTranslate), True)
        self.set_text_in_textview('tvOriginal3',
                                  self.movie.get_text(lineToTranslate+1))

        self.set_text_in_textview('tvTranslation1',
                                  self.movie.get_translation(lineToTranslate-1))

        translationText = self.movie.get_translation(lineToTranslate)
        labeled = False
        if ( translationText == ''
             and self.movie.get_text(lineToTranslate).startswith('<i>')):
            translationText = '<i>' + translationText + '</i>'
            labeled = True

        self.set_text_in_textview('tvTranslation2',
                                  translationText, bold=True, labeled=labeled)
        self.set_text_in_textview('tvTranslation3',
                                  self.movie.get_translation(lineToTranslate+1),
                                  False, True)

        wt.get_widget('spinCurrentLine').set_value(lineToTranslate)

    def store_current_translation(self):
        #
        # FIXME modificacion can be detected with gtk.TextBuffer.get_modified()
        # 
        newText = self.get_text_in_textview('tvTranslation2')
        oldText = self.movie.get_translation(self.counter)
        if ( newText != oldText ):
            print "Unsaved changes!"
            self.unsaved_changes = True
            self.movie.set_translation(self.counter, newText)

    def first(self):
        self.counter = 1
        self.print_line(self.counter)

    def next(self):
        self.counter += 1
        self.print_line(self.counter)

    def previous(self):
        self.counter -= 1
        self.print_line(self.counter)

    def go_to(self, position):
        self.counter = position
        self.print_line(self.counter)

    def check_unsaved_changes(self):
        return self.unsaved_changes


controller = Controller()

class Callbacks:

    def cb_destroy(self, *args):
        if controller.check_unsaved_changes():
            dialog = SaveConfirmationAlert(wt.get_widget('window1'))
            answer = dialog.run()
            dialog.destroy()
            if answer == gtk.RESPONSE_YES:
                if controller.save_project():
                    gtk.main_quit()
                else:
                    return False
            elif answer == gtk.RESPONSE_NO:
                gtk.main_quit()
        else:
            gtk.main_quit()

    def cb_file_new(self):
        dialog = NewProjectDialog()
        response = dialog.run()
        if ( response == gtk.RESPONSE_OK ):
            srtFile, movie = dialog.get_values()
            if ( srtFile ):
                controller.load_srt_file(srtFile)
            if ( movie ):
                controller.load_movie(movie)
        dialog.destroy()

    def cb_file_open(self):
        dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("SML subtitles")
        filter.add_pattern("*.sml")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_OK :
            controller.load_sml_file(dialog.get_filename())
            controller.first()
        dialog.destroy()


    def cb_save_as(self):
        controller.store_current_translation()
        controller.save_project_as()

    def cb_save(self):
        controller.store_current_translation()
        controller.save_project()

    def cb_next_button(self):
        controller.store_current_translation()
        controller.next()

    def cb_back_button(self):
        controller.previous()

    def cb_spin_change(self):
        newValue = wt.get_widget('spinCurrentLine').get_value_as_int()
        controller.go_to(newValue)

    def cb_export_to_srt(self):
        controller.export_to_srt()

if __name__ == '__main__':
    wt.get_widget('window1').show_all()
    wt.signal_autoconnect(Callbacks.__dict__)
    wt.get_widget('Save').set_sensitive(False)
    wt.get_widget('SaveAs').set_sensitive(False)
    wt.get_widget('ExportSRT').set_sensitive(False)
    gtk.main()
