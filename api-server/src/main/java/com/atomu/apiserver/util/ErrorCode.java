package com.atomu.apiserver.util;

public interface ErrorCode {
    // code 0 is success
    int INVALID_NAME_OR_PASSWORD = 1;
    int USER_NAME_EXIST = 2;
    int UNKNOWN_USER = 3;
    int USER_NAME_OR_PASSWORD_ERROR = 4;
    int NOT_LOGIN = 5;
    int TOKEN_EXPIRED = 6;
}