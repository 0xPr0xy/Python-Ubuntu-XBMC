#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import sys
import gtk

import gettext
from gettext import gettext as _
gettext.textdomain('simple-player1')
from quickly import prompts
import os
from quickly.widgets.media_player_box import MediaPlayerBox
from quickly.widgets.dictionary_grid import DictionaryGrid
import goocanvas
from gtk import VolumeButton
import gst





# optional Launchpad integration
# this shouldn't crash if not found as it is simply used for bug reporting
try:
    import LaunchpadIntegration
    launchpad_available = True
except:
    launchpad_available = False

# Add project root directory (enable symlink, and trunk execution).
PROJECT_ROOT_DIRECTORY = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))

python_path = []
if os.path.abspath(__file__).startswith('/opt'):
    syspath = sys.path[:] # copy to avoid infinite loop in pending objects
    for path in syspath:
        opt_path = path.replace('/usr', '/opt/extras.ubuntu.com/simple-player1')
        python_path.insert(0, opt_path)
        sys.path.insert(0, opt_path)
if (os.path.exists(os.path.join(PROJECT_ROOT_DIRECTORY, 'simple_player1'))
    and PROJECT_ROOT_DIRECTORY not in sys.path):
    python_path.insert(0, PROJECT_ROOT_DIRECTORY)
    sys.path.insert(0, PROJECT_ROOT_DIRECTORY)
if python_path:
    os.putenv('PYTHONPATH', "%s:%s" % (os.getenv('PYTHONPATH', ''), ':'.join(python_path))) # for subprocesses    os.putenv('PYTHONPATH', PROJECT_ROOT_DIRECTORY) # for subprocesses

from simple_player1 import (
    AboutSimplePlayer1Dialog, PreferencesSimplePlayer1Dialog)
from simple_player1.helpers import get_builder
from simple_player1.helpers import get_media_file
from simple_player1.sound_menu import SoundMenuControls

#Try adding AppIndicator. Will work after "qucikly add indicator"
try:
    from simple_player1 import indicator
except:
    indicator = False


class SimplePlayer1Window(gtk.Window):
    __gtype_name__ = "SimplePlayer1Window"
    
    # To construct a new instance of this method, the following notable 
    # methods are called in this order:
    # __new__(cls)
    # __init__(self)
    # finish_initializing(self, builder)
    # __init__(self)
    #
    # For this reason, it's recommended you leave __init__ empty and put
    # your inialization code in finish_intializing
    
    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated SimplePlayer1Window object.
        """
        builder = get_builder('SimplePlayer1Window')
        new_object = builder.get_object("simple_player1_window")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initalizing should be called after parsing the UI definition
        and creating a SimplePlayer1Window object with it in order to finish
        initializing the start of the new SimplePlayer1Window instance.
        
        Put your initilization code in here and leave __init__ undefined.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)
        
        self.supported_album_art_formats = [".png"]
        self.supported_video_formats = [".avi",".ogv",]
        self.supported_audio_formats = [".mp3",".ogg",]
        
        #open button
        open_button = gtk.ToolButton()
        open_button.set_stock_id(gtk.STOCK_OPEN)
        open_button.show()
        open_button.connect("clicked", self.openbutton)
        
        #player controls  
        self.player = MediaPlayerBox(True)
        self.player.remove(self.player.controls)
        #insert open button
        self.player.controls.insert(open_button, 0)
        hbox = self.builder.get_object('hbox1')
        hbox.pack_start(self.player.controls, True)
        self.player.connect("end-of-file", self.play_next_file)
        self.player.show()
        hpaned = self.builder.get_object('hpaned1')
        hpaned.add2(self.player)
        
        #create album art canvas
        self.goocanvas = goocanvas.Canvas()
        self.goocanvas.show()
        
        #icon
        app_icon = get_media_file("icon1.png")
        self.set_icon_from_file(app_icon)
        
        #create volume button
        #self.volumebutton = VolumeButton()
        #self.volumebutton.set_value(0.5)
        #self.volumebutton.show()
        #hbox.pack_start(self.volumebutton, fill=False)
        #hbox.pack_end(open_button, 1)

        #get and set background image for canvas
        #logo_file = get_media_file("background.png")
        #logo_file = get_media_file(self.image_url)
        #logo_pb = gtk.gdk.pixbuf_new_from_file(logo_file)
         
        #self.image = goocanvas.Image(parent=root_item, pixbuf=logo_pb, x=20, y=40)
        self.image = goocanvas.Image()
        logo_file1 = get_media_file("black.png")
        logo_pb1 = gtk.gdk.pixbuf_new_from_file(logo_file1)
        root_item = self.goocanvas.get_root_item()
        self.image = goocanvas.Image(parent=root_item, pixbuf=logo_pb1, x=0, y=0)

        #set up to paint text on the canvas on play_next_song
        self.song_text = goocanvas.Text(parent=root_item,text="", x=5, y=5, fill_color="white")
        self.song_text.set_property("font","Ubuntu")
        self.song_text.scale(1,1)
        
        #sound menu
        self.sound_menu = SoundMenuControls('simple-player1')
        self.sound_menu._sound_menu_next = self._sound_menu_next
        self.sound_menu._sound_menu_previous = self._sound_menu_previous
        self.sound_menu._sound_menu_is_playing = self._sound_menu_is_playing
        self.sound_menu._sound_menu_play = self._sound_menu_play
        self.sound_menu._sound_menu_pause = self._sound_menu_pause
        self.sound_menu._sound_menu_raise = self._sound_menu_raise 
        self.player.play_button.connect("toggled",self.play_button_toggled)

        global launchpad_available
        if launchpad_available:
            # see https://wiki.ubuntu.com/UbuntuDevelopment/Internationalisation/Coding for more information
            # about LaunchpadIntegration
            helpmenu = self.builder.get_object('helpMenu')
            if helpmenu:
                LaunchpadIntegration.set_sourcepackagename('simple-player1')
                LaunchpadIntegration.add_items(helpmenu, 0, False, True)
            else:
                launchpad_available = False
            
        
        #AppIndicator support
        #see http://owaislone.org/quickly-add-indicator/ 
        # use 'quickly add indicator' to get started
        # self is passed so methods of this class can be called from indicator.py
        # Comment to disable appindicator
        if indicator:
            self.indicator = indicator.new_application_indicator(self)
        # self.indicator is an appindicator instance.
        # learn more about it here http://LINK-to-AppIndicator-Docs
        
        
        # Uncomment the following code to read in preferences at start up.
        #dlg = PreferencesSimplePlayer1Dialog.PreferencesSimplePlayer1Dialog()
        #self.preferences = dlg.get_preferences()

        # Code for other initialization actions should be added here.
   
    def openbutton(self, widget, data=None):
        response, path = prompts.choose_directory()
        if response == gtk.RESPONSE_OK:
            media_files = []
            formats = self.supported_audio_formats + self.supported_video_formats
            for root, dirs, files in os.walk(path):
                for f in files:
                    for format in formats:
                        if f.lower().endswith(format):
                            file_url = "file://" + os.path.join(root, f)
                            data = {"File" : f,
                                    "url" : file_url,
                                    "format" : format,
                                    }
                            media_files.append(data)
                    for format in self.supported_album_art_formats:
                        if f.lower().endswith(format):
                            self.image_url = os.path.join(root, f)
                            
            #exception if no supported is found..
            if self.image_url is '':
                self.image_url = "background.png"
                
            #print media_files
            scrolledwindow = self.builder.get_object('scrolledwindow1')
            #print scrolledwindow
            for c in scrolledwindow.get_children():
                scrolledwindow.remove(c)
            media_grid = DictionaryGrid(media_files, keys=["File"])
            media_grid.connect("selection_changed", self.play_file)
            media_grid.show()
            #print media_files
            scrolledwindow.add(media_grid)
    
    def get_media_file(media_file_name):
        media_filename = get_data_file('media', '%s' % (media_file_name,))
        if not os.path.exists(media_filename):
            media_filename = None

        return "file:///"+media_filename
    
            
    def play_file(self, widget, selected_rows, data=None):
        #print selected_rows[-1]["url"]
        self.player.stop()
        hpaned = self.builder.get_object('hpaned1')
        format = selected_rows[0]["format"]
        current_visual = hpaned.get_child2()
        
        if format in self.supported_audio_formats:

            self.song_text.set_property("text",selected_rows[0]["File"])
            logo_file = self.image_url
            logo_pb = gtk.gdk.pixbuf_new_from_file(logo_file)
            root_item = self.goocanvas.get_root_item()
            #logo_file1 = get_media_file("black.png")
            #logo_pb1 = gtk.gdk.pixbuf_new_from_file(logo_file1)
            #self.image = goocanvas.Image(parent=root_item, pixbuf=logo_pb1, x=0, y=0)
            self.image = goocanvas.Image(parent=root_item, pixbuf=logo_pb, x=0, y=60)
            
            if current_visual is not self.goocanvas:
                hpaned.remove(current_visual)
                hpaned.add2(self.goocanvas)
        else:
            if current_visual is not self.player:
                hpaned.remove(current_visual)
                hpaned.add2(self.player)
        
        self.player.uri = selected_rows[-1]["url"]
        self.player.play()
        self.sound_menu.song_changed(title = selected_rows[-1]["File"])
        #self.sound_menu.song_changed(album = selected_rows[-1]["format"])
        #self.sound_menu.song_changed(artist = selected_rows[-1]["url"])
        
        self.sound_menu.signal_playing()
        
    def play_next_file(self, widget, file_url):
        scrolledwindow = self.builder.get_object('scrolledwindow1')
        grid = scrolledwindow.get_children()[0]
        selection = grid.get_selection()
        model, rows = selection.get_selected_rows()
        if len(rows) == 0:
            return
        next_to_select = rows[-1][0] + 1
        if next_to_select < len(grid.rows):
            selection.unselect_all()
            selection.select_path(next_to_select)
            self.play_file(self, grid.selected_rows)
    
    def play_previous_file(self):
        #get a reference to the current grid
        scrolledwindow = self.builder.get_object('scrolledwindow1')
        grid = scrolledwindow.get_children()[0]

        #get a gtk selection object from that grid
        selection = grid.get_selection()

        #get the selected row, and just return if none are selected
        model, rows = selection.get_selected_rows()
        if len(rows) == 0:
            return

        #calculate the next row to be selected by finding
        #the last selected row in the list of selected rows
        #and decrementing by 1
        prev_to_select = rows[-1][0] -1

        #if this is not the last row in the last
        #unselect all rows, select the next row, and call the
        #play_file handle, passing in the now selected row
        if prev_to_select != 0:
            selection.unselect_all()
            selection.select_path(prev_to_select)
            self.play_file(self,grid.selected_rows)
            
    def play_button_toggled(self, widget, data=None):
        if widget.get_active():
            self.sound_menu.signal_playing()
        else:
            self.sound_menu.signal_paused()
            
    def _sound_menu_is_playing(self):
        """return True if the player is currently playing, otherwise, False"""
        return self.player.playbin.get_state()[1] == gst.STATE_PLAYING

    def _sound_menu_play(self):
        """start playing if ready"""
        scrolledwindow = self.builder.get_object('scrolledwindow1')
        if len(scrolledwindow.get_children()[0].selected_rows) > 0:
            self.player.play()

    def _sound_menu_pause(self):
        """pause if playing"""
        if self.player.playbin.get_state()[1] == gst.STATE_PLAYING:
            self.player.pause()

    def _sound_menu_next(self):
        """go to the next song in the list"""
        self.play_next_file(self, None)

    def _sound_menu_previous(self):
        """go to the previous song in the list"""
        self.play_previous_file()

    def _sound_menu_raise(self):
       """raise the window to the top of the z-order"""
       self.get_window().show()
    
    
        
        
    def about(self, widget, data=None):
        """Display the about box for simple-player1."""
        about = AboutSimplePlayer1Dialog.AboutSimplePlayer1Dialog()
        response = about.run()
        about.destroy()

    def preferences(self, widget, data=None):
        """Display the preferences window for simple-player1."""
        prefs = PreferencesSimplePlayer1Dialog.PreferencesSimplePlayer1Dialog()
        response = prefs.run()
        if response == gtk.RESPONSE_OK:
            # Make any updates based on changed preferences here.
            pass
        prefs.destroy()

    def quit(self, widget, data=None):
        """Signal handler for closing the SimplePlayer1Window."""
        self.destroy()

    def on_destroy(self, widget, data=None):
        """Called when the SimplePlayer1Window is closed."""
        # Clean up code for saving application state should be added here.
        gtk.main_quit()

if __name__ == "__main__":
    # Support for command line options.
    import logging
    import optparse
    parser = optparse.OptionParser(version="%prog %ver")
    parser.add_option(
        "-v", "--verbose", action="store_true", dest="verbose",
        help=_("Show debug messages"))
    (options, args) = parser.parse_args()

    # Set the logging level to show debug messages.
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('logging enabled')
        
    #turn on the dbus mainloop
    from dbus.mainloop.glib import DBusGMainLoop
    DBusGMainLoop(set_as_default=True)
    
    # Run the application.
    window = SimplePlayer1Window()
    window.show()
    gtk.main()
