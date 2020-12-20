package com.atomu.apiserver.entity;

public class Liveserver {
    private Integer id;

    private String upload;

    private String download;

    private Integer hls;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getUpload() {
        return upload;
    }

    public void setUpload(String upload) {
        this.upload = upload == null ? null : upload.trim();
    }

    public String getDownload() {
        return download;
    }

    public void setDownload(String download) {
        this.download = download == null ? null : download.trim();
    }

    public Integer getHls() {
        return hls;
    }

    public void setHls(Integer hls) {
        this.hls = hls;
    }
}