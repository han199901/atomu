~~~java
    // code 0 is success
    int INVALID_NAME_OR_PASSWORD = 1;
    int USER_NAME_EXIST = 2;
    int UNKNOWN_USER = 3;
    int USER_NAME_OR_PASSWORD_ERROR = 4;
    int TOKEN_INVALID = 5;
    int PERMISSION_ERROR = 6;
    int ERROR = 10;
~~~

### /api/login

- http://help.hanblog.fun/api/login/login

  ~~~json
  Method: POST
  {"name": "用户名","password": "密码"}
  
  成功返回：
  {
      "code": 0,
      "result": {
          "uid": "1",
          "auth": "c6b0af83-da58-44cb-b6a7-6726a7cf045f"
      }
  }
  
  失败返回：
  {
      "code": 4,
      "result": null
  }
  
  
  ~~~

- http://help.hanblog.fun/api/login/token

  ~~~json
  Method: POST
  {"uid": "uid","auth": "auth"}
  
  成功返回：
  {
      "code": 0,
      "result": {
          "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIxIiwiZXhwIjoxNjA3MDAwMTgwfQ.QMzGxXvny_boD2Jc3zvHEpLuqukxZj-A1pZrR2o4peM"
      }
  }
  失败返回：
  {
      "code": 3,
      "result": null
  }
  
  
  ~~~

- http://help.hanblog.fun/api/login/register

  ~~~json
  Method: PUT
  {"name": "用户名","password": "密码"}
  
  成功返回：
  {
      "code": 0,
      "result": null
  }
  错误返回：
  {
      "code": 1,	//也可能是 2
      "result": null
  }
  ~~~



### /api/user

- http://help.hanblog.fun/api/user/logout

  ~~~json
  Method: POST
  
  成功返回：
  {
      "code": 0,
      "result": null
  }
  失败返回：
  {
  "code": 5, //也可能是 6
  "result": null
  }
  ~~~

  
