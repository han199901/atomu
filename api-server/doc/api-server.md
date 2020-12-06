~~~java
    // code 0 is success
    int INVALID_NAME_OR_PASSWORD = 1;
    int USER_NAME_EXIST = 2;
    int UNKNOWN_USER = 3;
    int USER_NAME_OR_PASSWORD_ERROR = 4;
    int TOKEN_INVALID = 5;
    int PERMISSION_ERROR = 6;

    int NO_MEETING = 10;
    int INVALID_TIME = 11;
    int MEETING_IS_ENDED = 13;

    int UNABLE_TO_PARSE_SUBMITTED_DATA=1000;
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


### /api/meeting

- http://help.hanblog.fun/api/meeting/create

  ~~~json
  Method: POST
  {"start": "开始时间", "end":"结束时间"}
  
  成功返回：
  {
      "code": 0,
      "result": {
          "id": null,
          "uid": 1,
          "code": "56f53043-18b2-4fee-963b-7c2f1ae1d2c3",
          "start": "2020-12-06T15:28:52.000+00:00",
          "end": "2020-12-06T15:58:52.000+00:00",
          "realend": null
      }
  }
  
  错误返回：
  {
      "code": 11, //11 时间冲突
      "result": null
  }
  ~~~
  
- http://help.hanblog.fun/api/meeting/cancel

  ~~~json
  Method: POST
  {"code":"会议码"}
  
  成功返回：
  {
      "code": 0,
      "result": null
  }
  错误返回：
  {
      "code": 10,  ////10 无该会议码；
      "result": null
  }
  ~~~
  
- http://help.hanblog.fun/api/meeting/search/{code}

  ~~~json
  Method: GET
  
  成功返回：
  {
      "code": 0,
      "result": {
          "id": 25,
          "uid": 1,
          "code": "63420f03-6d70-4362-ae3e-3bbec1662f4b",
          "start": "2020-12-06T14:28:52.000+00:00",
          "end": "2020-12-06T14:58:52.000+00:00",
          "realend": null
      }
  }
  错误返回：
  {
      "code": 10, //10 无该会议码；
      "result": null
  }
  
  ~~~

- http://help.hanblog.fun/api/meeting/list

  ~~~json
  Method: post
  
  成功返回：
  {
      "code": 0,
      "result": [
          {
              "id": 25,
              "uid": 1,
              "code": "63420f03-6d70-4362-ae3e-3bbec1662f4b",
              "start": "2020-12-06T14:28:52.000+00:00",
              "end": "2020-12-06T14:58:52.000+00:00",
              "realend": null
          },
          {
              "id": 26,
              "uid": 1,
              "code": "7b384a90-efa9-4d2d-bfa6-97e725e3089e",
              "start": "2021-12-06T14:28:52.000+00:00",
              "end": "2021-12-06T14:58:52.000+00:00",
              "realend": null
          }
      ]
  }
  失败返回：
  {
      "code": 10, //10 无该会议码；
      "result": null
  }
  
  ~~~

- http://help.hanblog.fun/api/meeting/over  // live/over

  ~~~json
  Method: post
  {"code":"会议码"}
  
  成功返回：
  {
      "code": 0,
      "result": null
  }
  失败返回：
  {
      "code": 13, // 10 无该会议码； 13 会议已经结束
      "result": null
  }
  
  ~~~

  
