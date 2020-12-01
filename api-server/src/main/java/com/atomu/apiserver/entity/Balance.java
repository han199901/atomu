package com.atomu.apiserver.entity;

import java.sql.Date;

public class Balance {
    private int id;
    private int uid;
    private Date expire;    //过期时间，null时永久有效
    private int balance;    //剩余分钟数
}
