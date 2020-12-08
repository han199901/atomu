package com.atomu.apiserver.util;


import org.springframework.util.DigestUtils;

import java.util.Date;
import java.util.UUID;

public class CommonUtil {
    public static String Password2Md5(String password) {
        return DigestUtils.md5DigestAsHex(password.getBytes());
    }
    public static String genUUID() {
        return UUID.randomUUID().toString();
    }
    public static String genUUIDSimple() {
        return UUID.randomUUID().toString().replaceAll("-","");
    }
    /***
     *
     * @param startDateOne 第一个时间段的开始时间
     * @param endDateOne 第一个时间段的结束时间
     * @param startDateTwo 第二个时间段的开始时间
     * @param endDateTwo 第二个时间段的结束时间
     * @return
     */
    public static Boolean IsInterSection(Date startDateOne,Date endDateOne,Date startDateTwo,Date endDateTwo)
    {
        Date maxStartDate = startDateOne;
        if(maxStartDate.before(startDateTwo))
        {
            maxStartDate = startDateTwo;
        }

        Date minEndDate = endDateOne;
        if(endDateTwo.before(minEndDate))
        {
            minEndDate = endDateTwo;
        }
        if(maxStartDate.before(minEndDate) || (maxStartDate.getTime() == minEndDate.getTime()))
        {
            return true;
        }
        else {
            return  false;
        }
    }
}
