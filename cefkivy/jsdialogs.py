#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#===============================================================================
# Written by Rentouch 2013 - http://www.rentouch.ch
#===============================================================================

from kivy.lang import Builder
from kivy import resources
from kivy.factory import Factory

import os

#Add folder to the kivy resource path list
#We are able than to just define relative paths regarding from the module directory.
resources.resource_add_path(os.path.abspath(os.path.join(os.path.dirname(__file__))))
Builder.load_file(resources.resource_find("jsdialogs.kv"))


class JSDialogs(object):

    def __init__(self):
        # Create popups
        self.js_confirm = Factory.JSConfirm()
        self.js_alert = Factory.JSAlert()
        self.js_prompt = Factory.JSPrompt()

    def on_js_dialog(self, obj, browser, origin_url, accept_lang, dialog_type, message_text, default_prompt_text,
                         callback, suppress_message):
        self.open_js_popup(dialog_type, callback, message_text, default_prompt_text)

    def on_before_unload_dialog(self, obj, browser, message_text, is_reload, callback):
        self.open_js_popup(1, callback, message_text)

    def open_js_popup(self, alert_type, callback, text="", default_prompt_text=""):
        """
        Displays a js popup
        """
        if alert_type == 0:
            self.js_alert.text = text
            self.js_alert.js_continue = callback.Continue
            self.js_alert.open()
        elif alert_type == 1:
            self.js_confirm.text = text
            self.js_confirm.js_continue = callback.Continue
            self.js_confirm.open()
        elif alert_type == 2:
            self.js_prompt.text = text
            self.js_prompt.default_prompt_text = default_prompt_text
            self.js_prompt.js_continue = callback.Continue
            self.js_prompt.open()