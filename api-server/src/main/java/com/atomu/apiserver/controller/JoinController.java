package com.atomu.apiserver.controller;

import com.atomu.apiserver.entity.Meeting;
import com.atomu.apiserver.service.JoinService;
import com.atomu.apiserver.util.ErrorCode;
import com.atomu.apiserver.util.R;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class JoinController {
    @Autowired
    JoinService joinService;

    @GetMapping("/join/{address}")
    public String join() {
        return "/meeting.html";
    }


    @GetMapping("/search/{address}")
    @ResponseBody
    public R search(@PathVariable String address) {
        String[] t = address.split(":");
        if (t[0] != null && t[1] != null) {
            int mid;
            try {
                mid = Integer.parseInt(t[0]);
            } catch (NumberFormatException e) {
                return R.setError();
            }
            Meeting searched = joinService.getMeetingInfo(mid,t[1]);
            if(searched == null)
                return R.setError(ErrorCode.NO_MEETING,null);
            else
                return R.setOK(searched);
        }
        else
            return R.setError();
    }
}
