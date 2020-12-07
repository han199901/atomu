package com.atomu.apiserver.mapper;

import com.atomu.apiserver.entity.Meeting;
import org.apache.ibatis.annotations.Mapper;

import java.util.Date;
import java.util.List;

@Mapper
public interface MeetingMapper {

    int deleteByPrimaryKey(Meeting record);
    int insert(Meeting record);

    int insertSelective(Meeting record);

    Meeting selectByPrimaryKey(Meeting record);

    int updateByPrimaryKeySelective(Meeting record);

    int updateByPrimaryKey(Meeting record);

    int deleteByCode(Meeting record);

    Meeting selectByCode(Meeting record);

    List<Meeting> selectByUid(Meeting record);

    int updateByCode(Meeting record);
}