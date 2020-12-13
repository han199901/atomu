package com.atomu.apiserver.controller;

import com.atomu.apiserver.entity.Live;
import com.atomu.apiserver.entity.Meeting;
import com.atomu.apiserver.service.LiveService;
import com.atomu.apiserver.util.R;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/live")
public class LiveController {

    @Autowired
    LiveService liveService;


    @PostMapping("/start")
    public R start(@RequestBody Meeting meeting, @RequestAttribute("Uid") String Uid) {
        int uid = Integer.parseInt(Uid);
        meeting.setUid(uid);
        Map<String, Object> res = liveService.startLive(meeting);
        if (res.get("code")!=null)
            return R.setError((int)res.get("code"),res.get("errResult"));
        return R.setOK(res);
    }

    @PostMapping("/end")
    public R end(@RequestBody Live live, @RequestAttribute("Uid") String Uid) {
        int uid = Integer.parseInt(Uid);
        live.setUid(uid);
        Map<String, Object> res = liveService.endLive(live);
        if (res.get("code")!=null)
            return R.setError((int)res.get("code"),res.get("errResult"));
        return R.setOK();
    }
}
