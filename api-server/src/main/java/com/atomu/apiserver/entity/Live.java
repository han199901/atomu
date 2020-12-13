package com.atomu.apiserver.entity;

public class Live {
    private Integer mid;

    private Integer uid;

    private Integer sid;

    private String uuid;

    private String upsecret;

    public Integer getMid() {
        return mid;
    }

    public void setMid(Integer mid) {
        this.mid = mid;
    }

    public Integer getUid() {
        return uid;
    }

    public void setUid(Integer uid) {
        this.uid = uid;
    }

    public Integer getSid() {
        return sid;
    }

    public void setSid(Integer sid) {
        this.sid = sid;
    }

    public String getUuid() {
        return uuid;
    }

    public void setUuid(String uuid) {
        this.uuid = uuid == null ? null : uuid.trim();
    }

    public String getUpsecret() {
        return upsecret;
    }

    public void setUpsecret(String upsecret) {
        this.upsecret = upsecret == null ? null : upsecret.trim();
    }
}