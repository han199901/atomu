package com.atomu.apiserver.entity;

import java.sql.Date;

public class Meeting {
    private int id;
    private int uid;        //会议拥有者
    private int code;        //会议码
    private Date start;     //预订开始时间
    private Date end;       //预订结束时间
    private Date realEnd;   //实际结束时间 null时表示会议未结束
}
