package com.atomu.apiserver.service;

import com.atomu.apiserver.entity.User;

import java.util.Map;

public interface UserService {

    public Map<String,Object> login(User user);
    public String getToken(Map<String, String> uidAndAuth);
    public int register(User user);

}
