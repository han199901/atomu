#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

__all__ = [
    "SignalingHandshake",
    "SignalingEnd",
    "SignalingBroadcast",
    "SignalingMembersNotify",
    "SignalingMembersListResponse",
    "parse_signaling"
]

class Signaling:
    def __init__(self, payload):
        self.version = 1

    def __str__(self):
        return json.dumps(self.__dict__)

class SignalingHandshake(Signaling):
    def __init__(self, payload, token=None):
        super().__init__(payload)
        self.type = "handshake"
        self.token = token if token else payload["token"]

class SignalingEnd(Signaling):
    def __init__(self, payload):
        super().__init__(payload)
        self.type = "end"

class SignalingBroadcast(Signaling):
    def __init__(self, payload):
        super().__init__(payload)
        self.type = "broadcast"
        self.msg = payload['msg']

class SignalingMembersNotify(Signaling):
    def __init__(self, payload):
        super().__init__(payload)
        self.type = "members_notify"
        self.members_changed = payload

class SignalingMembersListResponse(Signaling):
    def __init__(self, payload, members=None):
        super().__init__(payload)
        self.type = "members_list_response"
        self.members = members if members else payload["members"]

sigs = {
    "handshake": SignalingHandshake,
    "end": SignalingEnd,
    "broadcast": SignalingBroadcast,
    "members_notify": SignalingMembersNotify,
    "members_list_response": SignalingMembersListResponse
}

def parse_signaling(payload, req=None):
    obj = json.loads(payload)

    if req:
        if obj["type"] != req:
            raise RuntimeError(f"expect {req}, but recved {obj['type']}")

    if obj["type"] not in sigs:
        raise RuntimeError(f"unknown type {obj['type']}")

    return sigs[obj["type"]](obj)
