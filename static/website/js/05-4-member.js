/**
 * Created by Administrator on 2017/7/18 0018.
 */
    //列表切换
    $(document).ready(function() {

        // 确认修改
        document.querySelector(".modify").onclick = function () {
            document.querySelector(".modify-success span").innerHTML = getNowFormatDate();
            document.querySelector(".modify-success").style.display = "block";
        };

        function getNowFormatDate() {
            var date = new Date();
            var seperator1 = "-";
            var seperator2 = ":";
            var month = date.getMonth() + 1;
            var strDate = date.getDate();
            if (month >= 1 && month <= 9) {
                month = "0" + month;
            }
            if (strDate >= 0 && strDate <= 9) {
                strDate = "0" + strDate;
            }
            var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
                + " " + date.getHours() + seperator2 + date.getMinutes()
                + seperator2 + date.getSeconds();
            return currentdate;
        }

        //tab3-房源管理

        //  评价房源
        $(function () {
            var wjx_none = "☆";
            var wjx_sel = "★";
            //需求1：鼠标放上去  当前的li和之前所有的li内容全部变为实心五角星，其他空心，离开变为空心
            //需求2：鼠标点击哪个li，当前的li和之前的所有li变为实心，其他变为空心

            //需求1：鼠标放上去  当前的li和之前所有的li内容全部变为实心五角星，其他空心，离开变为空心
            $(".comment li").on("mouseenter",function () {
                //当前的li和之前所有的li内容全部变为实心五角星，其他空心
                $(this).text(wjx_sel).prevAll(".comment li").text(wjx_sel).end().nextAll(".comment li").text(wjx_none);
            });

            $(".comment li").on("mouseleave",function () {
                //bug：如果没有点击过li,那么会出现无法清除的现象
                if($("li.current").length === 0){
                    $(".comment li").text(wjx_none);
                }else {
                    $("li.current").text(wjx_sel).prevAll(".comment li").text(wjx_sel).end().nextAll(".comment li").text(wjx_none);
                }
                //当鼠标移开时， 哪个li有current的类名，该li及其前面的全部变为实心五角星，其他空心
            });

            //需求2：鼠标点击哪个li，当前的li和之前的所有li变为实心，其他变为空心
            $(".comment li").on("click",function () {
                //点击哪个li ，给哪个加一个类名。其他所有li的类名清空
//                $(this).text(wjx_sel).prevAll().text(wjx_sel).end().nextAll().text(wjx_none);
                $(this).attr("class","current").siblings(".comment li").removeAttr("class");
            })

        });



    });