package com.atomu.apiserver.controller;

import com.atomu.apiserver.service.UserService;
import com.atomu.apiserver.util.ErrorCode;
import com.atomu.apiserver.util.JwtUtil;
import com.atomu.apiserver.util.R;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;

@RestController
@RequestMapping("/api/user")
public class UserController {

    @Autowired
    UserService userService;

    @PostMapping("/logout")
    public R logout(HttpServletRequest request) {
        String auth = request.getHeader("Authorization");
        if(userService.logout(auth))
            return R.setOK();
        return R.setError(ErrorCode.PERMISSION_ERROR,null);

    }
}
