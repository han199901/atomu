package com.atomu.apiserver.util;


import org.springframework.util.DigestUtils;

public class CommonUtil {
    public static String Password2Md5(String password) {
        return DigestUtils.md5DigestAsHex(password.getBytes());
    }
}
