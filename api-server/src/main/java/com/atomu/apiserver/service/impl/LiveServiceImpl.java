package com.atomu.apiserver.service.impl;

import com.atomu.apiserver.entity.Live;
import com.atomu.apiserver.entity.Liveserver;
import com.atomu.apiserver.entity.Meeting;
import com.atomu.apiserver.mapper.*;
import com.atomu.apiserver.service.LiveService;
import com.atomu.apiserver.service.MeetingService;
import com.atomu.apiserver.util.CommonUtil;
import com.atomu.apiserver.util.ErrorCode;
import com.atomu.apiserver.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Service
public class LiveServiceImpl implements LiveService {

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
    public Map<String, Object> startLive(Meeting meeting) {
        Map<String,Object> res = new HashMap<>();
        if(meeting==null || meeting.getUid()==null || meeting.getId()==null || meeting.getCode()==null) {
            res.put("code", ErrorCode.UNABLE_TO_PARSE_SUBMITTED_DATA);
            return res;
        }
        Meeting searched = meetingService.searchMeetingById(meeting);
        if(searched==null || !searched.getCode().equals(meeting.getCode())) {
            res.put("code",ErrorCode.NO_MEETING);
            return res;
        }
        searched.setCode(null);
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
        Map<String, String> claim = new HashMap<>();
        claim.put("mid",meeting.getId().toString());
        claim.put("uid",meeting.getUid().toString());
        Date expired = new Date(date.getTime()+(5*60*1000));
        String token = JwtUtil.genToken(claim,expired);
        res.put("token",token);


        Live live = liveMapper.selectByPrimaryKey(meeting.getId());
        int count = liveserverMapper.countAll();
        if(live == null){
            live = new Live();
            live.setMid(meeting.getId());
            live.setSid(meeting.getId()%count+1);
            live.setUid(meeting.getUid());
            live.setUuid(CommonUtil.genUUIDSimple());
            live.setUpsecret(CommonUtil.genUUIDSimple());
            liveMapper.insert(live);
        }
        else {
            live.setUid(meeting.getUid());
            live.setUuid(CommonUtil.genUUIDSimple());
            live.setUpsecret(CommonUtil.genUUIDSimple());
            liveMapper.updateByPrimaryKey(live);
        }
        Liveserver liveserver = liveserverMapper.selectByPrimaryKey(live.getSid());
        StringBuffer buffer = new StringBuffer();
        buffer.append("rtmp://")
                .append(liveserver.getUpload())
                .append("/live")
                .append("/")
                .append(live.getUuid());
        res.put("upload_addr",buffer.toString());
        return res;
    }

    @Override
    public Map<String, Object> endLive(Live live) {
        Map<String,Object> res = new HashMap<>();
        if(live==null || live.getMid() == null || live.getUid()==null){
            res.put("code", ErrorCode.UNABLE_TO_PARSE_SUBMITTED_DATA);
            return res;
        }
        Live searchedLive = liveMapper.selectByPrimaryKey(live.getMid());
        if(searchedLive == null) {
            res.put("code",ErrorCode.NO_LIVE);
            return res;
        }
        if(live.getUid() != searchedLive.getUid()){
            res.put("code",ErrorCode.NO_LIVE);
            return res;
        }
        liveMapper.deleteByPrimaryKey(live.getMid());
        return res;
    }
}
