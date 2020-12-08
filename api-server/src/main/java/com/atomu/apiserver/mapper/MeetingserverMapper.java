package com.atomu.apiserver.mapper;

import com.atomu.apiserver.entity.Meetingserver;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface MeetingserverMapper {
    int deleteByPrimaryKey(Integer id);


    int insert(Meetingserver record);

    int insertSelective(Meetingserver record);

    Meetingserver selectByPrimaryKey(Integer id);

    Meetingserver selectByMid (Integer mid);

    int updateByPrimaryKeySelective(Meetingserver record);

    int updateByPrimaryKey(Meetingserver record);
}