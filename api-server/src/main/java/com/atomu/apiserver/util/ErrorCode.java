package com.atomu.apiserver.util;

public interface ErrorCode {
    int USER_NAME_NULL = 10001;
    int USER_PASSWORD_NULL = 10002;
    int USER_NAME_EXIST = 10003;
    int USER_NAME_OR_PASSWORD_ERROR = 10004;
    int NOT_LOGIN = 10005;
}