package com.atomu.apiserver.util;

import java.io.Serializable;

public class R  implements Serializable {

    private int code;
    private Object result;


    public static R setOK(Object result) {
        R r = new R();
        r.setCode(0);
        r.setResult(result);
        return r;
    }


    public static R setOK() {
        return setOK(null);
    }


    public static R setError(int code,Object result) {
        R r = new R();
        r.setCode(code);
        r.setResult(result);
        return r;
    }

    public static R setError() {
        R r = new R();
        r.setCode(1);
        return r;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }


    public Object getResult() {
        return result;
    }

    public void setResult(Object result) {
        this.result = result;
    }
}