package com.atomu.apiserver.service;

import com.atomu.apiserver.entity.Meeting;

public interface JoinService {
    Meeting getMeetingInfo(int mid, String code);
}
