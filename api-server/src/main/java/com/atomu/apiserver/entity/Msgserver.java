package com.atomu.apiserver.entity;

public class Msgserver {
    private Integer id;

    private String ip;

    private String ip6;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip == null ? null : ip.trim();
    }

    public String getIp6() {
        return ip6;
    }

    public void setIp6(String ip6) {
        this.ip6 = ip6 == null ? null : ip6.trim();
    }
}