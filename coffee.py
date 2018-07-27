#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Coffee Extraction Timer
# -Hunter Horsman

import gobject
import gtk
import os
import pygtk

pygtk.require('2.0')

time_total = 240.0
time_remaining = 240
dir_name = os.path.dirname(__file__)

def play_endsound():
    sound_file = os.path.join(dir_name, "done.wav")
    os.system("aplay {} --q -N -d 4 &".format(sound_file))


def progress_timeout(progress_bar):
    global time_remaining, time_total
    time_remaining -= 1
    new_val = 1 - (time_remaining / time_total)
    if new_val >= 1:
        progress_bar.pb.set_text("Coffee extraction done.")
        play_endsound()
        return False
    progress_bar.pb.set_fraction(new_val)
    progress_bar.pb.set_text("{0:.1f} % Brewed ({1:01d}:{2:02d} Remaining)"
                             .format(new_val * 100, time_remaining / 60, time_remaining % 60))
    return True


class CoffeeTimer:
    @staticmethod
    def delete_event():
        return False

    @staticmethod
    def destroy():
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_wmclass("floating_test", "floating")
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        # Containers
        self.timerBox = gtk.HBox()
        self.window.add(self.timerBox)

        # Icon
        self.icon = gtk.Image()
        icon_path = os.path.join(dir_name, "coffee.png")
        pixel_buffer = gtk.gdk.pixbuf_new_from_file(icon_path)
        scaled_buf = pixel_buffer.scale_simple(30, 30, gtk.gdk.INTERP_BILINEAR)
        self.icon.set_from_pixbuf(scaled_buf)
        self.timerBox.pack_start(self.icon)
        self.icon.set_usize(30, 30)
        self.icon.show()

        # Progress Bar
        self.pb = gtk.ProgressBar()
        self.pb.set_usize(300, 30)
        self.pb.set_text("Brewing coffee...")
        self.pb.set_fraction(0.0)
        self.timer = gobject.timeout_add(1000, progress_timeout, self)
        self.timerBox.pack_start(self.pb, True, True, 10)
        self.pb.show()

        # Close Button
        self.closeBtn = gtk.Button("")
        self.closeBtn.connect_object("clicked", gtk.Widget.destroy, self.window)
        self.closeBtn.set_usize(30, 30)
        self.timerBox.pack_end(self.closeBtn)
        self.closeBtn.show()

        # and the window
        self.timerBox.show()
        self.window.show()

        # play the start sound
        sound_file = os.path.join(dir_name, "beans.wav")
        os.system("aplay {} -q -N -d 3&".format(sound_file))

    @staticmethod
    def main():
        gtk.main()


if __name__ == "__main__":
    hello = CoffeeTimer()
    hello.main()
