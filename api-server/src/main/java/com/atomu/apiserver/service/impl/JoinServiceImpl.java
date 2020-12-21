package com.atomu.apiserver.service.impl;

import com.atomu.apiserver.entity.Meeting;
import com.atomu.apiserver.service.JoinService;
import com.atomu.apiserver.service.MeetingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class JoinServiceImpl implements JoinService {

    @Autowired
    MeetingService meetingService;

    @Override
    public Meeting getMeetingInfo(int mid, String code) {
        Meeting meeting = new Meeting();
        meeting.setId(mid);
        meeting.setCode(code);
        Meeting searched = meetingService.searchMeetingById(meeting);
        if (searched.getCode().equals(code)) {
            return searched;
        } else
            return null;
    }
}
