import pygtk
pygtk.require('2.0')
import gtk
import gobject
import gettext
import pango
from sys import argv

import os.path

from gazpacho.loader.loader import ObjectBuilder


class NewProjectDialog(gtk.Dialog):

    def getSelectorRow(self, name, selector):
        row = gtk.HBox(spacing=6)
        row.pack_start(gtk.Label(name))
        row.pack_start(selector)
        return row

    def __init__(self):

        gtk.Dialog.__init__(self, "Nuevo proyecto",
                            None,
                            gtk.DIALOG_MODAL |
                            gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                             gtk.STOCK_OK, gtk.RESPONSE_OK))

        srtFilter = gtk.FileFilter()
        srtFilter.set_name("SRT subtitles")
        srtFilter.add_pattern("*.srt")

        self.subtitlesSelector = gtk.FileChooserButton('Subtitulos')
        self.subtitlesSelector.add_filter(srtFilter)

        moviesFilter = gtk.FileFilter()
        moviesFilter.set_name("Movie file")
        moviesFilter.add_pattern("*.avi")
        moviesFilter.add_pattern("*.mpeg")
        
        self.filmSelector = gtk.FileChooserButton('Pelicula')
        self.filmSelector.add_filter(moviesFilter)

        subs = self.getSelectorRow("Subtitulos", self.subtitlesSelector)
        film = self.getSelectorRow("Pelicula", self.filmSelector)

        self.vbox.pack_start(subs)
        self.vbox.pack_start(film)
        self.vbox.show_all()


    def run(self):
        return gtk.Dialog.run(self)

    def get_values(self):
        return self.subtitlesSelector.get_filename(), self.filmSelector.get_filename()


if ( __name__ == '__main__'):

    def print_response(response):
        if ( response == gtk.RESPONSE_OK ):
            print "Aceptar"
        else:
            print "Cancelar"

    dialog = NewProjectDialog()
    print_response(dialog.run())
    print dialog.get_values()

