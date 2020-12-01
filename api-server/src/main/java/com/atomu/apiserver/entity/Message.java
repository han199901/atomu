package com.atomu.apiserver.entity;

import java.sql.Date;

public class Message {
    private int mid;    //会议id
    private int sender; //发送者id
    private String content; //内容
    private Date date;  //发送时间
}
