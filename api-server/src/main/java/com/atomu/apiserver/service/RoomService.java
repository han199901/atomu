package com.atomu.apiserver.service;

import com.atomu.apiserver.entity.Meeting;

import java.util.Map;

public interface RoomService {

    Map<String, Object> enterRoom(Meeting meeting);

    int closeRoom(Meeting meeting);
}
