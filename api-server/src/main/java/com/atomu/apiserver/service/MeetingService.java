package com.atomu.apiserver.service;

import com.atomu.apiserver.entity.Meeting;

import java.util.List;

public interface MeetingService {

    Meeting createMeeting(Meeting meeting);

    int cancelMeeting(Meeting meeting);

    Meeting searchMeetingById(Meeting meeting);

    List<Meeting> listMeeting(Meeting meeting);

    int overMeeting(Meeting meeting);

}
