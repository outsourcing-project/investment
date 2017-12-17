/**
 * Created by Administrator on 2017/8/8 0008.
 */
$(document).ready(function() {

    //初始化 位置列表
    //Default Action
    $(".tab_content").hide(); //Hide all content
    $("ul.tabs li:nth-child(2)").addClass("active").show(); //Activate first tab
    $(".tab_content:first").show(); //Show first tab content

    //初始化 区域范围列表
    //Default Action
    $(".s_tab_content").hide(); //Hide all content
    $("ul.service_tabs li:nth-child(2)").addClass("active").show(); //Activate first tab
    $(".s_tab_content:first").show(); //Show first tab content

    //On Click Event
    $("ul.tabs li").click(function () {
        //【选择位置】
        $("ul.tabs li").removeClass("active"); //Remove any "active" class
        $(this).addClass("active"); //Add "active" class to selected tab
        $(".tab_content").hide(); //Hide all tab content
        var activeTab = $(this).find("a").attr("href"); //Find the rel attribute value to identify the active tab + content
        console.log(activeTab);
        $(activeTab).fadeIn(); //Fade in the active content

        //每次【位置选择】结束，对应的【区域范围】回到初始值
        //Default Action
        $(".s_tab_content").hide(); //Hide all content
        var newContent = $(activeTab).find("ul").find("li:nth-child(2)").find("a").attr("href"); //Show first tab content
        $(newContent).show();
        console.log(newContent);
        $("ul.service_tabs li").removeClass("active");
        $("ul.service_tabs li:nth-child(2)").addClass("active").show(); //Activate first tab



        //【选择位置】 >> 【选择区域】
        //On Click Event
        $("ul.service_tabs li").click(function () {
            $("ul.service_tabs li").removeClass("active"); //Remove any "active" class
            $(this).addClass("active"); //Add "active" class to selected tab
            $(".s_tab_content").hide(); //Hide all tab content
            var activeTab2 = $(this).find("a").attr("href"); //Find the rel attribute value to identify the active tab + content
            console.log(activeTab2);
            $(activeTab2).fadeIn(); //Fade in the active content
            return false;
        });

        return false;
    });

    //初次 【选择位置】 >> 【选择区域】
    $("ul.service_tabs li").click(function () {
        $("ul.service_tabs li").removeClass("active"); //Remove any "active" class
        $(this).addClass("active"); //Add "active" class to selected tab
        $(".s_tab_content").hide(); //Hide all tab content
        var activeTab2 = $(this).find("a").attr("href"); //Find the rel attribute value to identify the active tab + content
        console.log(activeTab2);
        $(activeTab2).fadeIn(); //Fade in the active content
        return false;
    });
});