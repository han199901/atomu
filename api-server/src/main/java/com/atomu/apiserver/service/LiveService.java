package com.atomu.apiserver.service;

import com.atomu.apiserver.entity.Live;
import com.atomu.apiserver.entity.Meeting;

import java.util.Map;

public interface LiveService {
    Map<String, Object> startLive(Meeting meeting);
    Map<String, Object> endLive(Live id);
}
