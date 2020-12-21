package com.atomu.apiserver.util;

import com.atomu.apiserver.entity.Live;
import com.atomu.apiserver.entity.Liveserver;

public class StreamAddress {

    public static String generateUploadAddress(Liveserver liveserver, Live live) {
        var builder = new StringBuilder();
        builder.append("rtsp://")
                .append(liveserver.getUpload())
                .append("/live")
                .append("/")
                .append(live.getUuid());
        return builder.toString();
    }

    public static String generateDownloadAddress(Liveserver liveserver, Live live) {
        var builder = new StringBuilder();
        builder.append("rtsp://").append(liveserver.getDownload())
                .append("/live").append("/").append(live.getUuid());
        return builder.toString();
    }
}
