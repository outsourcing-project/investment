/**
 * Created by Administrator on 2017/9/29 0029.
 */
$(document).ready(function () {
    // tab9 系统消息
    $(".systInfoTitle").click(function () {
        if($(this).find("svg use").attr("xlink:href") === "#icon-open"){
            $(this).find("svg use").attr("xlink:href","#icon-close");
        }else{
            $(this).find("svg use").attr("xlink:href","#icon-open");
        }

        $(this).parent().find(".systInfo").toggle();

        $(".systemInformation").height("auto");
        $(".tab_container").css("height","auto");

    });
});
