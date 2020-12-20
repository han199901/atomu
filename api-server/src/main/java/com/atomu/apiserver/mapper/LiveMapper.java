package com.atomu.apiserver.mapper;

import com.atomu.apiserver.entity.Live;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface LiveMapper {
    int deleteByPrimaryKey(Integer mid);

    int insert(Live record);

    int insertSelective(Live record);

    Live selectByPrimaryKey(Integer mid);

    int updateByPrimaryKeySelective(Live record);

    int updateByPrimaryKey(Live record);
}