package com.atomu.apiserver.service;

import com.atomu.apiserver.entity.User;
import com.atomu.apiserver.mapper.UserMapper;
import com.atomu.apiserver.util.CommonUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserService {
    @Autowired
    UserMapper userMapper;

    public User isCorrect(User user) {
        User sUser = userMapper.selectByName(user.getName());
        if(CommonUtil.Password2Md5(user.getPassword()).equals(sUser.getPassword()))
            return  sUser;
        else return null;
    }
    public boolean addUser(String username, String password) {
        if(userMapper.selectByName(username)!=null)
            return false;
        User user = new User();
        user.setName(username);
        password = CommonUtil.Password2Md5(password);
        user.setPassword(password);
        userMapper.insert(user);
        return true;
    }
}
