package com.atomu.apiserver.entity;

import java.util.Date;

public class Meeting {
    @Override
    public String toString() {
        return "Meeting{" +
                "id=" + id +
                ", uid=" + uid +
                ", code='" + code + '\'' +
                ", start=" + start +
                ", end=" + end +
                ", realend=" + realend +
                '}';
    }

    private Integer id;

    private Integer uid;

    private String code;

    private Date start;

    private Date end;

    private Date realend;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getUid() {
        return uid;
    }

    public void setUid(Integer uid) {
        this.uid = uid;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code == null ? null : code.trim();
    }

    public Date getStart() {
        return start;
    }

    public void setStart(Date start) {
        this.start = start;
    }

    public Date getEnd() {
        return end;
    }

    public void setEnd(Date end) {
        this.end = end;
    }

    public Date getRealend() {
        return realend;
    }

    public void setRealend(Date realend) {
        this.realend = realend;
    }
}