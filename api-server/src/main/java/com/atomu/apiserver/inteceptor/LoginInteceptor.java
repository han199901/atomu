package com.atomu.apiserver.inteceptor;

import com.atomu.apiserver.util.ErrorCode;
import com.atomu.apiserver.util.JwtUtil;
import com.atomu.apiserver.util.R;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@Component
public class LoginInteceptor implements HandlerInterceptor {

    @Autowired
    private ObjectMapper objectMapper;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String token = request.getHeader("Authorization");
        if (token != null) {
            String uid = JwtUtil.verify(token);
            if (uid!=null) {
                request.setAttribute("Uid",uid);
                return true;
            }
        }
        R r = R.setError(ErrorCode.TOKEN_INVALID, null);
        String json = objectMapper.writeValueAsString(r);//要返回的数据
        response.addHeader("content-type", "application/json;charset=utf-8");
        response.getWriter().write(json);
        return false;
    }
}
