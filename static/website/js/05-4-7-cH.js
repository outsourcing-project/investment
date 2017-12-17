/**
 * Created by Administrator on 2017/10/9 0009.
 */
$(document).ready(function () {
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