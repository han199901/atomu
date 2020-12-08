package com.atomu.apiserver.mapper;

import com.atomu.apiserver.entity.Msgserver;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface MsgserverMapper {
    int deleteByPrimaryKey(Integer id);

    int insert(Msgserver record);

    int insertSelective(Msgserver record);

    Msgserver selectByPrimaryKey(Integer id);

    int updateByPrimaryKeySelective(Msgserver record);

    int updateByPrimaryKey(Msgserver record);

    int countAll();
}