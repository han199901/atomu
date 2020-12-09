package com.atomu.apiserver.service.impl;

import com.atomu.apiserver.entity.Meeting;
import com.atomu.apiserver.entity.Meetingserver;
import com.atomu.apiserver.entity.Msgserver;
import com.atomu.apiserver.mapper.MeetingMapper;
import com.atomu.apiserver.mapper.MeetingserverMapper;
import com.atomu.apiserver.mapper.MsgserverMapper;
import com.atomu.apiserver.service.MeetingService;
import com.atomu.apiserver.util.CommonUtil;
import com.atomu.apiserver.util.ErrorCode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;


@Service
public class MeetingServiceImpl implements MeetingService {

    @Autowired
    MeetingMapper meetingMapper;
    @Autowired
    MeetingserverMapper meetingserverMapper;
    @Autowired
    MsgserverMapper msgserverMapper;

    @Override
    public Meeting createMeeting(Meeting meeting) {
        if(meeting==null || meeting.getStart() == null || meeting.getEnd() == null)
            return null;
        meeting.setCode(CommonUtil.genUUIDSimple());
        if(meeting.getStart().after(meeting.getEnd()))
            return null;
        List<Meeting> meetingList = this.listMeeting(meeting);
        if(meetingList.size()>=10) {
            Meeting res = new Meeting();
            res.setId(-1);
            return res;
        }
        for(int i=0; i<meetingList.size();i++) {
            if(CommonUtil.IsInterSection(meetingList.get(i).getStart(),meetingList.get(i).getEnd(),meeting.getStart(),meeting.getEnd()))
                return null;
        }
        meetingMapper.insertSelective(meeting);
        Meetingserver meetingserver = new Meetingserver();
        meetingserver.setMid(meeting.getId());
        int num = msgserverMapper.countAll();
        if(num == 0)
            return null;
        meetingserver.setSid(meeting.getId()%num+1);
        meetingserverMapper.insert(meetingserver);
        return meeting;
    }

    @Override
    public int cancelMeeting(Meeting meeting) {
        if(meeting==null || meeting.getId() == null)
            return ErrorCode.UNABLE_TO_PARSE_SUBMITTED_DATA;
        if(meetingMapper.selectByPrimaryKey(meeting).getRealend()!=null)
            return ErrorCode.MEETING_IS_ENDED;
        int num = meetingMapper.deleteByPrimaryKey(meeting);
        if(num==1)
            return 0;
        else
            return ErrorCode.NO_MEETING;
    }

    @Override
    public Meeting searchMeetingById(Meeting meeting) {
        if(meeting==null || meeting.getId()==null)
            return null;
        Meeting seachedMeeting = meetingMapper.selectByPrimaryKey(meeting);
        return seachedMeeting;
    }


    @Override
    public List<Meeting> listMeeting(Meeting meeting) {
        if(meeting==null || meeting.getUid()==null)
            return null;
        Meeting temp = new Meeting();
        temp.setUid(meeting.getUid());
        Date date = new Date(System.currentTimeMillis());
        temp.setEnd(date);
        List<Meeting> meetingArrayList = meetingMapper.selectByUid(temp);
        return meetingArrayList;
    }

    @Override
    public int overMeeting(Meeting meeting) {
        if(meeting==null || meeting.getId()==null)
            return ErrorCode.UNABLE_TO_PARSE_SUBMITTED_DATA;
        Meeting searchedMeeting = this.searchMeetingById(meeting);
        if(searchedMeeting==null)
            return ErrorCode.NO_MEETING;
        else if(searchedMeeting.getRealend()==null) {
            Date date = new Date(System.currentTimeMillis());
            meeting.setRealend(date);
            meetingMapper.updateByPrimaryKeySelective(meeting);
            return 0;
        } else {
            return ErrorCode.MEETING_IS_ENDED;
        }

    }
}
