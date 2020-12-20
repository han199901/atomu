package com.atomu.apiserver.mapper;

import com.atomu.apiserver.entity.Liveserver;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface LiveserverMapper {
    int deleteByPrimaryKey(Integer id);

    int insert(Liveserver record);

    int insertSelective(Liveserver record);

    Liveserver selectByPrimaryKey(Integer id);

    int updateByPrimaryKeySelective(Liveserver record);

    int updateByPrimaryKey(Liveserver record);

    int countAll();
}