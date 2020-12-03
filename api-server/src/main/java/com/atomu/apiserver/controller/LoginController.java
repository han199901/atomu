package com.atomu.apiserver.controller;

import com.atomu.apiserver.entity.User;
import com.atomu.apiserver.service.UserService;
import com.atomu.apiserver.util.ErrorCode;
import com.atomu.apiserver.util.JwtUtil;
import com.atomu.apiserver.util.R;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.repository.query.Param;
import org.springframework.lang.NonNull;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/login")
public class LoginController {

    @Autowired
    UserService userService;
    @Autowired
    RedisTemplate redisTemplate;

    @PostMapping("/login")
    public R login(@RequestBody User user) {
        if (user.getName() == null || user.getPassword() == null) {
            return R.setError(ErrorCode.USER_NAME_OR_PASSWORD_ERROR, "用户名或密码不正确", null);
        }
        user = userService.isCorrect(user);
        if(user!=null) {
            Map<String, String> result = new HashMap<>();
            String auth = JwtUtil.genAuth();
            redisTemplate.opsForValue().set(user.getId().toString(),auth);
            result.put("uid",user.getId().toString());
            result.put("auth", auth);
            return R.setOK(result);
        }
        else {
            return R.setError(ErrorCode.USER_NAME_OR_PASSWORD_ERROR, "用户名或密码不正确", null);
        }
    }
    @GetMapping("/token/{uid}/{auth}")
    public R getToken(@NonNull @PathVariable("uid") Integer uid, @NonNull @PathVariable("auth") String auth) {
        Map<String,String> res = new HashMap<>();
        String searchAuth = (String) redisTemplate.opsForValue().get(uid.toString());
        if(searchAuth == null || !searchAuth.equals(auth))
            return R.setError();
        String token = JwtUtil.genToken(uid);
        res.put("token",token);
        return R.setOK(res);
    }
    @PutMapping("/register")
    public R register(@RequestBody User user) {
        if(userService.addUser(user.getName(),user.getPassword()))
            return R.setOK();
        return R.setError();
    }


}
