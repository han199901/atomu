package com.atomu.apiserver.controller;

import com.atomu.apiserver.entity.Meeting;
import com.atomu.apiserver.service.MeetingService;
import com.atomu.apiserver.service.RoomService;
import com.atomu.apiserver.util.ErrorCode;
import com.atomu.apiserver.util.R;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;


@RestController
@RequestMapping("/api/room")
public class RoomController {

    @Autowired
    RoomService roomService;

    @PostMapping("/enter")
    public R enter(@RequestBody Meeting meeting, @RequestAttribute("Uid") String Uid) {
        int uid = Integer.parseInt(Uid);
        meeting.setUid(uid);
        Map<String, Object> res = roomService.enterRoom(meeting);
        if (res.get("code")!=null)
            return R.setError((int)res.get("code"),res.get("errResult"));
        return R.setOK(res);
    }

}
