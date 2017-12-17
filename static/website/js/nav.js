/**
 * Created by Administrator on 2017/7/9 0009.
 */
$('.nav_items>li').click(function () {
   $(this).addClass('active').siblings("li").removeClass("active");
});

