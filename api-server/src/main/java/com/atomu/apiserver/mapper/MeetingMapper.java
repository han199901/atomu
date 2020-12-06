package com.atomu.apiserver.mapper;

import com.atomu.apiserver.entity.Meeting;
import org.apache.ibatis.annotations.Mapper;

import java.util.Date;
import java.util.List;

@Mapper
public interface MeetingMapper {
    int deleteByPrimaryKey(Integer id);

    int insert(Meeting record);

    int insertSelective(Meeting record);

    Meeting selectByPrimaryKey(Integer id);

    int updateByPrimaryKeySelective(Meeting record);

    int updateByPrimaryKey(Meeting record);

    int deleteByCode(Meeting record);

    Meeting selectByCode(Meeting meeting);

    List<Meeting> selectByUid(int uid);

    int updateByCode(Meeting meeting);
}