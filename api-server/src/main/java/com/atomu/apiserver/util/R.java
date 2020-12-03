package com.atomu.apiserver.util;

import java.io.Serializable;

public class R  implements Serializable {

    private int code;
    private String msg;
    private Object result;


    public static R setOK(Object result) {
        R r = new R();
        r.setCode(1);
        r.setMsg("操作成功");
        r.setResult(result);
        return r;
    }


    public static R setOK() {
        return setOK(null);
    }


    public static R setError(int code,String msg,Object result) {
        R r = new R();
        r.setCode(code);
        r.setMsg(msg);
        r.setResult(result);
        return r;
    }

    public static R setError() {
        R r = new R();
        r.setCode(0);
        r.setMsg("操作异常");
        return r;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public Object getResult() {
        return result;
    }

    public void setResult(Object result) {
        this.result = result;
    }
}