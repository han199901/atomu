package com.atomu.apiserver.service;

import com.atomu.apiserver.entity.User;

import java.util.Map;

public interface UserService {

    Map<String,Object> login(User user);
    String getToken(Map<String, String> uidAndAuth);
    int register(User user);

    boolean logout(String authorization);
}
