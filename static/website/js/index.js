/**
 * Created by Administrator on 2017/9/17 0017.
 */
$(document).ready(function() {
    //    <!-- Swiper JS -->
    //    banner autoplay
    var swiper = new Swiper('.swiper-container', {
        pagination: '.swiper-pagination',
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
        paginationClickable: true,
        spaceBetween: 1000,
        centeredSlides: true,
        autoplay: 4000,
        autoplayDisableOnInteraction: false,
        effect: 'fade',
        loop: true
    });

    // 房源推荐切换
    //Default Action
    $(".tab-content").hide(); //Hide all content
    $("ul.tabs li:first").addClass("active").show(); //Activate first tab
    $(".tab-content:first").show(); //Show first tab content

//On Click Event
    $("ul.tabs li").click(function() {
        $("ul.tabs li").removeClass("active"); //Remove any "active" class
        $(this).addClass("active"); //Add "active" class to selected tab
        $(".tab-content").hide(); //Hide all tab content
        var activeTab = $(this).find("a").attr("href"); //Find the rel attribute value to identify the active tab + content
        $(activeTab).fadeIn(); //Fade in the active content
        return false;
    });

});



