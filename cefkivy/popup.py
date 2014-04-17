#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#===============================================================================
# Written by Rentouch 2013 - http://www.rentouch.ch
#===============================================================================

from kivy.lang import Builder
from kivy import resources
from kivy.factory import Factory
from kivy.core.window import Window

from browser import CefBrowser
from browser import cefpython
from jsdialogs import JSDialogs

import os

#Add folder to the kivy resource path list
#We are able than to just define relative paths regarding from the module directory.
resources.resource_add_path(os.path.abspath(os.path.join(os.path.dirname(__file__))))
Builder.load_file(resources.resource_find("popup.kv"))

RESOURCE_DIR = ""


class PopupBrowser(CefBrowser):

    def __init__(self, **kwargs):
        super(PopupBrowser, self).__init__(resources_dir=RESOURCE_DIR, **kwargs)

    def on_touch_down(self, touch, *kwargs):
        if not self.collide_point(*touch.pos):
            return
        if self.keyboard_mode == "global":
            self.request_keyboard()
        else:
            Window.release_all_keyboards()
            self.browser.GetFocusedFrame().ExecuteJavascript("__kivy__keyboard_requested = false;")

        touch.moving = False
        self.touches.append(touch)
        touch.grab(self)

        if len(self.touches) == 1:
            # Only mouse click when single touch
            y = self.height-touch.pos[1] + self.pos[1]
            x = touch.x - self.pos[0]
            self.browser.SendMouseClickEvent(
                x,
                y,
                cefpython.MOUSEBUTTON_LEFT,
                mouseUp=False,
                clickCount=1
            )
        return True

    def on_touch_move(self, touch, *kwargs):
        if touch.grab_current is not self:
            return

        if len(self.touches) == 1:
            # Moving
            if (abs(touch.dx) > 5 or abs(touch.dy) > 5) or touch.moving:
                y = self.height-touch.pos[1] + self.pos[1]
                x = touch.x - self.pos[0]
                self.browser.SendMouseMoveEvent(x, y, mouseLeave=False)
        else:
            # Scrolling
            touch1, touch2 = self.touches[:2]
            dx = touch2.dx / 2. + touch1.dx / 2.
            dy = touch2.dy / 2. + touch1.dy / 2.
            self.browser.SendMouseWheelEvent(touch.x, self.height-touch.pos[1], dx, -dy)
        return True

    def on_touch_up(self, touch, *kwargs):
        if touch.grab_current is not self:
            return
        y = self.height-touch.pos[1] + self.pos[1]
        x = touch.x - self.pos[0]
        self.browser.SendMouseClickEvent(
            x,
            y,
            cefpython.MOUSEBUTTON_LEFT,
            mouseUp=True, clickCount=1
        )
        self.touches.remove(touch)
        touch.ungrab(self)
        return True


class PopupController(object):

    def __init__(self, resource_dir=None):
        # Define data path
        if resource_dir:
            global RESOURCE_DIR
            RESOURCE_DIR = resource_dir

        # Create popup
        self.popup = Factory.CEFPopup()
        self.popup.bind(on_dismiss=self.on_close_popup)
        self.jsdialogs = JSDialogs()
        self.popup.browser.bind(on_js_dialog=self.jsdialogs.on_js_dialog)
        self.popup.browser.bind(on_before_unload_dialog=self.jsdialogs.on_before_unload_dialog)

    def on_before_popup(self, obj, browser, frame, targetUrl, targetFrameName,
                        popupFeatures, windowInfo, client, browserSettings, noJavascriptAccess):
        print windowInfo, popupFeatures, targetFrameName
        self.popup.url = targetUrl
        self.popup.open()

    def on_close_popup(self, *kwargs):
        self.popup.url = "about:blank"