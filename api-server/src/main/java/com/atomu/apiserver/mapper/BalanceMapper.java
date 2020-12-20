package com.atomu.apiserver.mapper;

import com.atomu.apiserver.entity.Balance;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface BalanceMapper {
    int deleteByPrimaryKey(Integer id);

    int insert(Balance record);

    int insertSelective(Balance record);

    Balance selectByPrimaryKey(Integer id);

    int updateByPrimaryKeySelective(Balance record);

    int updateByPrimaryKey(Balance record);
}