/**
 * Created by Administrator on 2017/9/11 0011.
 */
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
    $("ul.service_tabs li:nth-child(1)").addClass("active").show(); //Activate first tab
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
        $("ul.service_tabs li").removeClass("active");
        $("ul.service_tabs li:nth-child(1)").addClass("active").show(); //Activate first tab



        //【选择位置】 >> 【选择区域】
        //On Click Event
        $("ul.service_tabs li").click(function () {
            $("ul.service_tabs li").removeClass("active"); //Remove any "active" class
            $(this).addClass("active"); //Add "active" class to selected tab
            $(".s_tab_content").hide(); //Hide all tab content
            var activeTab2 = $(this).find("a").attr("href"); //Find the rel attribute value to identify the active tab + content
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

    //其他筛选条件
    //价格筛选
    filter1("price");
    //房型筛选
    filter1("structure");
    //租赁方式筛选
    filter2("wayToRent");
    //室友筛选
    $(".wayToRent li:gt(1)").click(function () {
        if($("#sharedRent").hasClass("active")){
            $(".roommate").show();
        }else{
            $(".roommate").hide();
        }
    });

    filter2("roommate");

    function filter1(rowName) {
        var liArr = $("."+rowName+" ul li");
        var choose = false;
        var total = liArr.length - 2;
        var num = 0;

        // console.log(liArr);
        // //选中【不限】时，其他不用高亮
        $(liArr[1]).click(function () {
            $(this).addClass("active");
            for(var i = 2; i < liArr.length;i++){
                $(liArr[i]).removeClass("active");
            }
        });

        // 点击除【不限】之外的选项时高亮，全高亮时改为全部不高亮，【不限】选项高亮
        //为 不限 后面的 选项进行单独绑定点击事件
        for(var i = 2; i < liArr.length;i++) {
            console.log(liArr[i]);
            $(liArr[i]).click(function () {
                //每次点击重置 choose 的值，且
                choose = true;
                num = 0;

                //点击后，高亮显示
                if($(this).hasClass("active")){
                    $(this).removeClass("active");
                }else{
                    $(this).addClass("active");
                }

                //每次点击，都遍历一次确定是否都选中了
                for (var j = 2; j < liArr.length; j++) {
                    if($(liArr[j]).attr("class") === undefined) {
                        choose = false;
                        num++;
                        if(num === total ){
                            choose = true;
                        }
                    }
                }

                //对  choose 进行判断
                if(choose){
                    $("."+rowName+" ul li").removeClass("active");
                    $(liArr[1]).addClass("active");
                }else{
                    $(liArr[1]).removeClass("active");
                }
            });
        }

    }
    function filter2(rowName) {
        $("."+rowName+" ul li").click(function () {
            $(this).parent().find("li").removeClass("active");
            $(this).addClass("active");
        });
    }

});