package com.atomu.apiserver.service.impl;

import com.atomu.apiserver.entity.Meeting;
import com.atomu.apiserver.mapper.MeetingMapper;
import com.atomu.apiserver.service.MeetingService;
import com.atomu.apiserver.util.CommonUtil;
import com.atomu.apiserver.util.ErrorCode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;


@Service
public class MeetingServiceImpl implements MeetingService {

    @Autowired
    MeetingMapper meetingMapper;

    @Override
    public Meeting createMeeting(Meeting meeting) {
        if(meeting==null || meeting.getStart() == null || meeting.getEnd() == null)
            return null;
        meeting.setCode(CommonUtil.genUUID());
        if(meeting.getStart().after(meeting.getEnd()))
            return null;
        List<Meeting> meetingList = this.listMeeting(meeting);
        for(int i=0; i<meetingList.size();i++) {
            if(CommonUtil.IsInterSection(meetingList.get(i).getStart(),meetingList.get(i).getEnd(),meeting.getStart(),meeting.getEnd()))
                return null;
        }
        meetingMapper.insertSelective(meeting);
        return meeting;
    }

    @Override
    public int cancelMeeting(Meeting meeting) {
        if(meeting==null || meeting.getCode() == null)
            return ErrorCode.UNABLE_TO_PARSE_SUBMITTED_DATA;
        int num = meetingMapper.deleteByCode(meeting);
        if(num==1)
            return 0;
        else
            return ErrorCode.NO_MEETING;
    }

    @Override
    public Meeting searchMeetingByCode(Meeting meeting) {
        if(meeting==null || meeting.getCode()==null)
            return null;
        Meeting seachedMeeting = meetingMapper.selectByCode(meeting);
        return seachedMeeting;
    }

    @Override
    public List<Meeting> listMeeting(Meeting meeting) {
        if(meeting==null)
            return null;
        if(meeting.getEnd()==null) {
            Date date = new Date(System.currentTimeMillis());
            meeting.setEnd(date);
        }
        List<Meeting> meetingArrayList = meetingMapper.selectByUid(meeting.getUid());
        return meetingArrayList;
    }

    @Override
    public int overMeeting(Meeting meeting) {
        if(meeting==null || meeting.getCode()==null)
            return ErrorCode.UNABLE_TO_PARSE_SUBMITTED_DATA;
        Meeting searchedMeeting = this.searchMeetingByCode(meeting);
        if(searchedMeeting==null)
            return ErrorCode.NO_MEETING;
        else if(searchedMeeting.getRealend()==null) {
            Date date = new Date(System.currentTimeMillis());
            meeting.setRealend(date);
            meetingMapper.updateByCode(meeting);
            return 0;
        } else {
            return ErrorCode.MEETING_IS_ENDED;
        }

    }
}
