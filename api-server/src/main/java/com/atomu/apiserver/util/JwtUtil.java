package com.atomu.apiserver.util;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTCreator;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;

import java.util.*;

public class JwtUtil {
    //一小时过期
    private static final long EXPIRE_TIME = 60*60*1000;
    //TOKEN 私钥
    private static final String TOKEN_SECRET = "405c1e6d-05be-447a-8a81-ca58190185ca";
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
