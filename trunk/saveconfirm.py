#!/usr/bin/env python

#
# Copyright (C) 2005 Red Hat, Inc.
# Copyright (C) 2004 GNOME Foundation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

#
# All the text was copied from gedit-close-confirmation-dialog.c
#

import gtk
import gettext

class SaveConfirmationAlert (gtk.MessageDialog):
    def __init__ (self, parent_window):
        gtk.MessageDialog.__init__ (self, parent_window, 0,
                                    gtk.MESSAGE_WARNING, gtk.BUTTONS_NONE)

        self.set_destroy_with_parent (True)
        self.set_title ("Salvar antes de salir")

        self.add_button ("Cerrar _sin salvar" , gtk.RESPONSE_NO)
        self.add_button (gtk.STOCK_CANCEL,           gtk.RESPONSE_CANCEL)
        self.add_button (gtk.STOCK_SAVE,             gtk.RESPONSE_YES)

        self.set_default_response (gtk.RESPONSE_YES)

        self.set_markup ("<b>¿Guardar cambios antes de salir?</b>")
        secondary_msg = "Si no guarda los cambios, se perderan permanentemente"
        self.format_secondary_text (secondary_msg)

if __name__ == "__main__":
    # gettext.install (PACKAGE, os.path.join (DATADIR, "locale"))
    global _
    _ = gettext.gettext

    def print_response (response):
        if response == gtk.RESPONSE_YES:
            print "YES"
        elif response == gtk.RESPONSE_NO:
            print "NO"
        elif response == gtk.RESPONSE_CANCEL:
            print "CANCEL"
        else:
            print "BITE ME"
            
    print_response (SaveConfirmationAlert (None).run ())
    print_response (SaveConfirmationAlert (None).run ())
    print_response (SaveConfirmationAlert (None).run ())
    print_response (SaveConfirmationAlert (None).run ())
    print_response (SaveConfirmationAlert (None).run ())
    print_response (SaveConfirmationAlert (None).run ())
