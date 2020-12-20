package com.atomu.apiserver.controller;

import com.atomu.apiserver.entity.Meeting;
import com.atomu.apiserver.service.MeetingService;
import com.atomu.apiserver.util.ErrorCode;
import com.atomu.apiserver.util.R;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.List;

@RestController
@RequestMapping("/api/meeting")
public class MeetingController {

    @Autowired
    MeetingService meetingService;

    @Value("${meeting.max-created-num}")
    Integer max_created_num;

    @PostMapping("/create")
    public R createMeeting(@RequestBody Meeting meeting, @RequestAttribute("Uid") String Uid) {
        int uid = Integer.parseInt(Uid);
        meeting.setUid(uid);
        Meeting result = meetingService.createMeeting(meeting);
        if(result == null)
            return R.setError(ErrorCode.UNABLE_TO_PARSE_SUBMITTED_DATA,null);
        else {
            if (result.getId() == -1) {
                return R.setError(ErrorCode.QUANTITY_EXCEEDS_LIMIT, null);
            }
            if(result.getId() == -2)
                return R.setError(ErrorCode.INVALID_TIME,null);
        }
        return R.setOK(result);
    }

    @PostMapping("/cancel")
    public R cancelMeeting(@RequestBody Meeting meeting , @RequestAttribute("Uid") String Uid) {
        int uid = Integer.parseInt(Uid);
        meeting.setUid(uid);
        int code = meetingService.cancelMeeting(meeting);
        if(code == 0)
            return R.setOK();
        else
            return R.setError(code,null);
    }


    @PostMapping("/list")
    public R listMeeting(HttpServletRequest request) {
        Meeting meeting = new Meeting();
        meeting.setUid(Integer.parseInt((String) request.getAttribute("Uid")));
        List<Meeting> meetingArrayList = meetingService.listMeeting(meeting);
        if(meetingArrayList.size()==0)
            return R.setOK(null);
        else
            return R.setOK(meetingArrayList);
    }

    @PostMapping("/over")
    public R overMeeting(@RequestBody Meeting meeting) {
        int code = meetingService.overMeeting(meeting);
        if(code == 0)
            return R.setOK();
        else
            return R.setError(code,null);

    }


}


