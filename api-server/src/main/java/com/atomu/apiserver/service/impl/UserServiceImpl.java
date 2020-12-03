package com.atomu.apiserver.service.impl;

import com.atomu.apiserver.entity.User;
import com.atomu.apiserver.mapper.UserMapper;
import com.atomu.apiserver.service.UserService;
import com.atomu.apiserver.util.CommonUtil;
import com.atomu.apiserver.util.ErrorCode;
import com.atomu.apiserver.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
public class UserServiceImpl implements UserService {
    @Autowired
    UserMapper userMapper;
    @Autowired
    RedisTemplate redisTemplate;


    public Map<String,Object> login(User user) {
        if(user==null || user.getName() == null || user.getPassword() == null || user.getName().equals("") || user.getPassword().equals("")) {
            return null;
        }
        else {
            Map<String,Object> map = new HashMap<>();
            User searchUser = userMapper.selectByName(user.getName());
            if(searchUser==null)
                return null;
            else if(CommonUtil.Password2Md5(user.getPassword()).equals(searchUser.getPassword())) {
                user = searchUser;
                map.put("userObject",searchUser);
                String auth = JwtUtil.genAuth();
                Map<String,String> result = new HashMap<>();
                redisTemplate.opsForValue().set(user.getId().toString(),auth);
                result.put("uid",user.getId().toString());
                result.put("auth", auth);
                map.put("result",result);
                return map;
            }
            else
                return null;
        }
    }

    @Override
    public String getToken(Map<String, String> uidAndAuth) {
        String uid = uidAndAuth.get("uid");
        String auth = uidAndAuth.get("auth");
        if(uid==null || auth ==null)
            return null;
        Map<String,String> res = new HashMap<>();
        String searchAuth = (String) redisTemplate.opsForValue().get(uid);
        if(searchAuth == null || !searchAuth.equals(auth))
            return null;
        String token = JwtUtil.genToken(uid);
        return token;
    }

    public int register(User user) {
        if(user==null || user.getName() == null || user.getPassword() == null || user.getName().equals("") || user.getPassword().equals("")) {
            return ErrorCode.INVALID_NAME_OR_PASSWORD;
        }
        String username = user.getName();
        String password = CommonUtil.Password2Md5(user.getPassword());
        if(userMapper.selectByName(username)!=null)
            return ErrorCode.USER_NAME_EXIST;
        user.setPassword(password);
        userMapper.insert(user);
        return 0;
    }
}
