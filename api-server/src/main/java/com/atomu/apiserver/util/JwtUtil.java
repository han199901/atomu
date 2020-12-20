package com.atomu.apiserver.util;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTCreator;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Controller;

import java.util.*;

@Component
public class JwtUtil {
    //一小时过期
    public static long EXPIRE_TIME;
    //TOKEN 私钥
    private static String TOKEN_SECRET;
    //MSG-SERVER 私钥
    private static String MSG_TOKEN_SECRET;

    @Value("${token.expire-time}")
    public void setExpireTime(long expireTime) {
        EXPIRE_TIME = expireTime;
    }
    @Value("${token.api-server.secret}")
    public void setTokenSecret(String secret) {
        TOKEN_SECRET = secret;
    }
    @Value("${token.msg-server.secret}")
    public void setMsgTokenSecret(String secret) {
        MSG_TOKEN_SECRET = secret;
    }

    public static String genToken(String uid) {
        Algorithm algorithm = Algorithm.HMAC256(TOKEN_SECRET);
        Date date = new Date(System.currentTimeMillis() + EXPIRE_TIME);
        Map<String, Object> header = new HashMap<>();
        header.put("typ","JWT");
        header.put("alg","HS256");
        return JWT.create()
                .withHeader(header)
                .withClaim("uid",uid)
                .withExpiresAt(date)
                .sign(algorithm);
    }
    public static String genToken(Map<String, String> map) {
        Algorithm algorithm = Algorithm.HMAC256(TOKEN_SECRET);
        Date date = new Date(System.currentTimeMillis() + EXPIRE_TIME);
        Map<String, Object> header = new HashMap<>();
        header.put("typ","JWT");
        header.put("alg","HS256");
        JWTCreator.Builder token = JWT.create().withHeader(header);
        for(String key : map.keySet()) {
            token.withClaim(key,map.get(key));
        }
        return  token.withExpiresAt(date)
                .sign(algorithm);
    }

    /**
     *  for msg server
     * @param map
     * @param date
     * @return
     */
    public static String genToken(Map<String, String> map,Date date) {
        Algorithm algorithm = Algorithm.HMAC256(MSG_TOKEN_SECRET);
        Map<String, Object> header = new HashMap<>();
        header.put("typ","JWT");
        header.put("alg","HS256");
        JWTCreator.Builder token = JWT.create().withHeader(header);
        for(String key : map.keySet()) {
            token.withClaim(key,map.get(key));
        }
        return  token.withExpiresAt(date)
                .sign(algorithm);
    }
    public static String verify(String authorization) {
        try {
            Algorithm algorithm = Algorithm.HMAC256(TOKEN_SECRET);
            JWTVerifier verifier = JWT.require(algorithm).build();
            String type = authorization.substring(0,7);
            String token = authorization.substring(7);
            if(!type.equals("Bearer "))
                return null;
            DecodedJWT jwt = verifier.verify(token);
            return jwt.getClaim("uid").asString();
        }
        catch (Exception exception) {
            return null;
        }
    }
    public static String decode(String authorization){
        try {
            Algorithm algorithm = Algorithm.HMAC256(TOKEN_SECRET);
            JWTVerifier verifier = JWT.require(algorithm).build();
            String type = authorization.substring(0,7);
            String token = authorization.substring(7);
            if(!type.equals("Bearer "))
                return null;
            DecodedJWT jwt = verifier.verify(token);
            return jwt.getClaim("uid").asString();
        }
        catch (Exception exception) {
            return null;
        }
    }
    public static String genAuth() {
        return UUID.randomUUID().toString();
    }
}
