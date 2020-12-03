package com.atomu.apiserver.controller;

import com.atomu.apiserver.entity.User;
import com.atomu.apiserver.service.UserService;
import com.atomu.apiserver.util.ErrorCode;
import com.atomu.apiserver.util.R;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/login")
public class LoginController {

    @Autowired
    UserService userService;


    @PostMapping("/login")
    public R login(@RequestBody User user) {
        Map<String, Object> res = userService.login(user);
        if(res!=null) {
            return R.setOK(res.get("result"));
        }
        else {
            return R.setError(ErrorCode.USER_NAME_OR_PASSWORD_ERROR, null);
        }
    }
    @PostMapping("/token")
    public R getToken(@RequestBody Map<String, String> uidAndAuth) {
        String token = userService.getToken(uidAndAuth);
        Map<String, String> result = null;
        if(token == null)
            return R.setError(ErrorCode.UNKNOWN_USER,null);
        else {
            result = new HashMap<>();
            result.put("token",token);
            return R.setOK(result);
        }
    }
    @PutMapping("/register")
    public R register(@RequestBody User user) {
        int code = userService.register(user);
        if(code==0)
            return R.setOK();
        return R.setError(code,null);
    }


}
