#!/usr/bin/env python3

import asyncio
import websockets
import jwt
import json
from itertools import islice

from . import config
from .signaling import *

meetings = dict()
meetings_stats = dict()

class MeetingStats:
    def __init__(self):
        self.is_ending = False

class Member:
    def __init__(self, mid, uid, name, socket):
        self.uid = uid
        self.name = name
        self.socket = socket

class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Member):
            return {
                "uid": o.uid,
                "name": o.name
            }
        else:
            return super().default(o)

async def broadcast(mid, signaling, ignore_uid=None, kill=False):
    tmp = meetings[mid].copy()
    for u, member in tmp.items():
        if ignore_uid and u == ignore_uid:
            continue
        try:
            text = json.dumps(signaling.__dict__, cls=MyJSONEncoder)
            print(f"> {mid} {u}: {text}")
            await member.socket.send(text)
            if kill:
                await unreg(mid, u, unreg_only=True)
        except websockets.ConnectionClosed:
            await unreg(mid, u, unreg_only=True)

async def unreg(mid, uid, unreg_only=False):
    if mid not in meetings or \
            uid not in meetings[mid]:
        return

    member = meetings[mid][uid]
    del meetings[mid][uid]

    await member.socket.close()
    if not unreg_only and not meetings_stats[mid].is_ending:
        await broadcast(mid, SignalingMembersNotify([{"a": "remove", "uid": uid}]), ignore_uid=uid)

    if not meetings[mid]:
        del meetings[mid]
        if mid in meetings_stats:
            del meetings_stats[mid]

async def reg(s, uid, name, mid):
    if mid in meetings:
        if uid in meetings[mid]:
            await unreg(mid, uid)

    if mid not in meetings:
        meetings[mid] = dict()
        meetings_stats[mid] = MeetingStats()

    tmp = Member(mid, uid, name, s)
    meetings[mid][uid] = tmp
    return tmp

async def worker(websocket, path):
    hs = parse_signaling(await websocket.recv(), req="handshake")
    payload = jwt.decode(hs.token, config.secret, algorithms=config.algorithms)

    uid = payload['uid']
    name = payload['name']
    mid = payload['mid']
    admin = payload['isAdmin']
    member = await reg(websocket, uid, name, mid)

    resp = SignalingMembersListResponse(None, members=meetings[mid])
    await websocket.send(json.dumps(resp.__dict__, cls=MyJSONEncoder))

    await broadcast(mid, SignalingMembersNotify([{"a": "add", "m": member}]), ignore_uid=uid)

    while True:
        try:
            signaling = parse_signaling(await websocket.recv())
        except websockets.ConnectionClosed:
            print(f"info: {uid} in {mid} terminated")
            break

        print(f"< {signaling}")
        if signaling.type == "broadcast":
            if 'op' in signaling.msg:
                signaling.from_user = { "id": uid, "name": name }
                if signaling.msg['op'] == 'live':
                    _ = jwt.decode(signaling.msg['token'], config.secret, algorithms=config.algorithms)
                    del signaling.msg['token']
                    await broadcast(mid, signaling, ignore_uid=uid)
                elif signaling.msg['op'] == 'text':
                    await broadcast(mid, signaling, ignore_uid=uid)
                else:
                    # FIXME: error notify to user
                    pass
        elif signaling.type == "end":
            if admin:
                meetings_stats[mid].is_ending = True
                await broadcast(mid, signaling, ignore_uid=uid, kill=True)
        else:
            #FIXME: error notify to user
            pass

    await unreg(mid, uid)

def main():
    start_server = websockets.serve(worker, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
