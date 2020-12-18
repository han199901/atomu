#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gio, GLib, Gdk
from gi.repository import Soup
from gettext import gettext as _

import sys
import json
from iso8601 import parse_date
from datetime import datetime, timezone

from .api import *
from .window import Window
from .asynchelper import async_function
from .misc import dark_mode_switch, format_date_ml, sharelink
from .config import *
from .dialog_create_meeting import CreateMeetingDialog
from .dialog_start_live import StartLiveDialog
from .widget_meeting_list_row import MeetingListRow
from .widget_member_list_row import MemberListRow
from .widget_message_bubble import MessageBubbleRow
from .vlc import VLCWidget
from .push import StreamPush

class MainWindow(Window):
    def __init__(self, app):
        super().__init__(app, "main")

        self.builder_add_file("main_menu")

        self.window.set_application(app)

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        menu = self.get("app-menu")
        button = self.get("menu_button")
        popover = Gtk.Popover.new_from_model(button, menu)
        button.set_popover(popover)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        app.add_action(action)

        action = Gio.SimpleAction.new("logout", None)
        action.connect("activate", self.on_logout)
        app.add_action(action)

        self.list_all_my_meetings()

        self.window.show_all()

        self.madmin = False
        self.mid = None
        self.mcode = None
        self.vlc = None
        self.session = None
        self.wsconn = None
        self.push = StreamPush()

    def on_meeting_delete_clicked(self, button, row, id, code):
        def on_done(r, e):
            try:
                result = finish(r, e)
                lb = self.get("listbox_meetings")
                lb.remove(row.get_parent())
            except CError as e:
                self.defexphandler(e)

        api_async("/meeting/cancel", {
            "id": id
        }, on_done)

    def on_meeting_share_clicked(self, button, id, code):
        self.clipboard.set_text(sharelink(id, code), -1)

        def infobar_response(infobar, rid, data):
            if rid == Gtk.ResponseType.CLOSE:
                infobar.destroy()

        def infobar_timeout(infobar):
            infobar.destroy()

        infobar = Gtk.InfoBar.new()
        infobar.set_show_close_button(True)
        infobar.set_message_type(Gtk.MessageType.INFO)
        infobar.get_content_area().pack_start(Gtk.Label.new(_("Shared link copied to clipboard")), False, True, 0)
        infobar.connect("response", infobar_response, None)

        self.get("main_box").pack_start(infobar, False, True, 0)
        infobar.show_all()

        GLib.timeout_add(5000, infobar_timeout, infobar)

    def on_listbox_meetings_row_activated(self, lb, row):
        lr = row.get_child()
        id = lr.x_id
        code = lr.x_code

        lb.set_sensitive(False)
        def cb():
            lb.set_sensitive(True)

        self.mjoin(id, code, cb)

    def list_all_my_meetings(self):
        lb = self.get("listbox_meetings")
        for i in lb.get_children():
            lb.remove(i)

        def on_done(r, e):
            try:
                result = finish(r, e)

                if result:
                    for i in result:
                        if "name" not in i or i["name"] == None or i["name"] == "":
                            i["name"] = _("Unnamed meeting")

                        lr = MeetingListRow()
                        lr.title.set_text(i["name"])
                        btime = parse_date(i["start"])
                        etime = parse_date(i["end"])
                        lr.description.set_text(format_date_ml(btime, etime))
                        lr.delete.connect("clicked", self.on_meeting_delete_clicked, lr, i["id"], i["code"])
                        lr.share.connect("clicked", self.on_meeting_share_clicked, i["id"], i["code"])
                        lr.x_id = i["id"]
                        lr.x_code = i["code"]
                        lb.add(lr)
            except CNetworkError as e:
                print("network error, will re-try soon ...")
                GLib.timeout_add_seconds(2, self.list_all_my_meetings)
            except CError as e:
                self.defexphandler(e)

        api_async("/meeting/list", {}, on_done)
        return False

    def on_create_meeting_clicked(self, button):
        CreateMeetingDialog(self)

    def ws_send(self, data):
        if self.wsconn:
            data['version'] = 1
            text = json.dumps(data)
            print(f"ws> {text}")
            self.wsconn.send_text(text)

    def on_ws_message(self, connection, msg_type, message):
        text = message.get_data().decode()
        print(f"ws< {text}")
        obj = json.loads(text)
        if obj['type'] == "members_list_response":
            lb = self.get("members")
            for i in lb.get_children():
                lb.remove(i)

            for id, member in obj['members'].items():
                lr = MemberListRow(id, member['name'])
                lb.add(lr)
        elif obj['type'] == "members_notify":
            lb = self.get("members")

            for i in obj['members_changed']:
                if i["a"] == "add":
                    lr = MemberListRow(i["m"]["uid"], i["m"]["name"])
                    lb.add(lr)
                elif i["a"] == "remove":
                    for row in lb.get_children():
                        if row.get_child().id == i["uid"]:
                            lb.remove(row)
        elif obj['type'] == "end":
            self.mexit()
        elif obj['type'] == "broadcast":
            msg = obj['msg']
            if msg['op'] == "text":
                self.add_msg_bubble(obj['from_user']['id'], obj['from_user']['name'], msg['text'])
            else:
                print(f"unknown msg op {msg['op']}")
        else:
            print(f"unknown ws msg type {obj['type']}")

    def add_msg_bubble(self, uid, name, text):
        lb = self.get("messages")
        lr = MessageBubbleRow(uid)
        if name != "":
            name = name + ":\n"
        else:
            lr.reverse()
        lr.text.set_text(name + text)
        lb.add(lr)
        lr.get_parent().set_activatable(False)

    def on_send_message_clicked(self, button):
        entry = self.get("send_message")
        text = entry.get_text()
        self.ws_send({
            "type": "broadcast",
            "msg": {
                "op": "text",
                "text": text
            }
        })
        self.add_msg_bubble(get_uid(), "", text)
        entry.set_text("")

    def on_ws_closed(self, connection):
        print("on_ws_closed")
        self.mexit()

    def on_ws_connected(self, session, result, meeting, token):
        try:
            self.wsconn = session.websocket_connect_finish(result)
            self.wsconn.connect('message', self.on_ws_message)
            self.wsconn.connect('closed', self.on_ws_closed)
            self.wsconn.set_keepalive_interval(5)

            self.ws_send({
                "type": "handshake",
                "token": token
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(e)
            self.session = None
            self.err(_("Can not enter meeting room."))
            self.mexit()
        finally:
            pass
            #self.get("spinner").stop()

    def menter(self, msgserver, meeting, token):
        if not self.vlc:
            self.vlc = VLCWidget(self.get("vlc"))
            #self.vlc.set_mrl("/media/th/disk2/th/bitcoin.mp4")

        tmp = self.get("messages")
        for i in tmp:
            tmp.remove(i)

        tmp = self.get("members")
        for i in tmp:
            tmp.remove(i)

        self.mid = meeting["id"]
        self.mcode = meeting["code"]
        self.session = Soup.Session()
        msg = Soup.Message.new("GET", msgserver["ip"])
        self.session.websocket_connect_async(msg, None, None, None, self.on_ws_connected, meeting, token)

        if meeting["uid"] == get_uid():
            self.madmin = True
            self.get("mexit").set_label(_("End meeting"))
        else:
            self.madmin = False
            self.get("mexit").set_label(_("Exit"))

        self.get("stack_main").set_visible_child_name("meeting")

    def mjoin(self, mid, code, callback):
        def on_done(r, e):
            try:
                callback()
                result = finish(r, e)
                self.menter(result["msgserver"], result["meeting"], result["token"])
            except CError as e:
                self.defexphandler(e)

        api_async("/room/enter", {
            "id": mid,
            "code": code
        }, on_done)

    def destroy_meeting(self, mid):
        def on_done(r, e):
            try:
                result = finish(r, e)
            except CError as e:
                self.defexphandler(e)

        api_async("/room/close", {
            "id": mid
        }, on_done)

    def mexit(self):
        if self.wsconn:
            self.wsconn.close(0)
            self.wsconn = None

        if self.vlc:
            self.vlc.stop()

        self.push.stop()
        self.get("stack_main").set_visible_child_name("join")

    def on_mexit_only_clicked(self, button):
        self.mexit()

    def on_share_clicked(self, button):
        self.on_meeting_share_clicked(button, self.mid, self.mcode)

    def on_fullscreen_clicked(self, button):
        if self.window.get_window().get_state() & Gdk.WindowState.FULLSCREEN:
            self.window.unfullscreen()
        else:
            self.window.fullscreen()

    def on_mexit_clicked(self, button):
        if self.madmin:
            self.destroy_meeting(self.mid)
            self.ws_send({
                "type": "end"
            })
            self.list_all_my_meetings()

        self.mexit()

    def on_start_live_clicked(self, button):
        StartLiveDialog(self)

    def on_join_clicked(self, button):
        tmp = self.get("mcode").get_text().split(":")

        if len(tmp) != 2:
            self.err(_("Invalid meeting code"))
            return

        code = tmp[1]
        mid = tmp[0]

        button.set_sensitive(False)
        def cb():
            button.set_sensitive(True)

        self.mjoin(mid, code, cb)

    def on_about(self, action, param):
        pass

    def on_logout(self, action, param):
        def on_done(r, e):
            try:
                result = finish(r, e)
                config_set("user_auth_uid", None)
                config_set("user_auth_code", None)
                self.window.close()
            except CSystemError as e:
                config_set("user_auth_uid", None)
                config_set("user_auth_code", None)
                self.window.close()
            except CError as e:
                self.defexphandler(e)

        api_async("/user/logout", {
            "code": config_get("user_auth_code", None),
        }, on_done)


    def on_dark_switch_button_clicked(self, button):
        dark_mode_switch(True)
