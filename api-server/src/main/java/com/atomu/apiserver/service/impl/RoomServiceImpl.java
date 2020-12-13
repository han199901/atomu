package com.atomu.apiserver.service.impl;

import com.atomu.apiserver.entity.*;
import com.atomu.apiserver.mapper.*;
import com.atomu.apiserver.service.MeetingService;
import com.atomu.apiserver.service.RoomService;
import com.atomu.apiserver.util.ErrorCode;
import com.atomu.apiserver.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Service
public class RoomServiceImpl implements RoomService {
    @Autowired
    MeetingService meetingService;
    @Autowired
    LiveMapper liveMapper;
    @Autowired
    LiveserverMapper liveserverMapper;
    @Autowired
    MeetingserverMapper meetingserverMapper;
    @Autowired
    MsgserverMapper msgserverMapper;
    @Autowired
    UserMapper userMapper;

    @Override
    public Map<String, Object> enterRoom(Meeting meeting) {
        Map<String,Object> res = new HashMap<>();
        if(meeting==null || meeting.getUid()==null || meeting.getId()==null || meeting.getCode()==null) {
            res.put("code",ErrorCode.UNABLE_TO_PARSE_SUBMITTED_DATA);
            return res;
        }
        Meeting searched = meetingService.searchMeetingById(meeting);
        if(searched==null || !searched.getCode().equals(meeting.getCode())) {
            res.put("code",ErrorCode.NO_MEETING);
            return res;
        }
        Date date = new Date(System.currentTimeMillis());
        if(date.before(searched.getStart())) {
            res.put("code", ErrorCode.MEETING_IS_NOT_START);
            res.put("errResult",searched);
            return res;
        }
        if(searched.getRealend()!=null){
            res.put("code", ErrorCode.MEETING_IS_ENDED);
            res.put("errResult",searched);
            return res;
        }
        Boolean isAdmin = meeting.getUid().equals(searched.getUid())?true:false;
        String username = userMapper.selectByPrimaryKey(meeting.getUid()).getName();
        res.put("meeting",searched);
        Map<String,String> map = new HashMap<>();
        map.put("uid",meeting.getUid().toString());
        map.put("mid",searched.getId().toString());
        map.put("isAdmin",isAdmin.toString());
        map.put("name",username);
        String token=null;
        if(searched.getEnd().after(date))
            token = JwtUtil.genToken(map,searched.getEnd());
        else {
            date.setTime(date.getTime()+JwtUtil.EXPIRE_TIME);
            token = JwtUtil.genToken(map,date);
        }
        res.put("token",token);
        Msgserver msgserver = msgserverMapper.selectByPrimaryKey(meetingserverMapper.selectByMid(searched.getId()).getSid());
        res.put("msgserver",msgserver);
        Live live = liveMapper.selectByPrimaryKey(meeting.getId());
        if(live != null) {
            Liveserver liveserver = liveserverMapper.selectByPrimaryKey(live.getSid());

            User user = userMapper.selectByPrimaryKey(live.getUid());
            Map<String,Object> map1 = new HashMap<>();
            map1.put("user",user);

            StringBuffer buffer = new StringBuffer();
            buffer.append("rtmp://").append(liveserver.getDownload())
                    .append("/live").append("/").append(live.getUuid());
            String download = buffer.toString();
            map1.put("download_addr",download);

            res.put("live",map1);
        }
        return res;
    }

    @Override
    public int closeRoom(Meeting meeting) {
        if(meeting==null || meeting.getUid()==null || meeting.getId()==null) {
            return ErrorCode.UNABLE_TO_PARSE_SUBMITTED_DATA;
        }
        Meeting searched = meetingService.searchMeetingById(meeting);
        if(searched==null || !searched.getUid().equals(meeting.getUid())) {
            return ErrorCode.PERMISSION_ERROR;
        }
        Date date = new Date(System.currentTimeMillis());
        if(searched.getStart().after(date))
            return ErrorCode.MEETING_IS_NOT_START;
        int res = meetingService.overMeeting(meeting);
        return res;
    }
}
