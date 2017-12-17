/**
 * Created by Administrator on 2017/8/8 0008.
 */
$(document).ready(function () {

    //验证手机合法性
    $(".phoneNum").blur(function () {
        //手机合法性验证
        var reg1 = /^(13[0-9]|15[0|3|6|7|8|9]|18[8|9])\d{8}$/;
        var phoneNum = $(this).val();
        console.log(phoneNum);
        if(reg1.test(phoneNum)){
            //3、符合个给一个样式，不符合给另一个样式
            $(this).css('color','green');
            $(".verification-code button").removeClass("disable").addClass("able").removeAttr("disabled");
        }else{
            $(this).css('color','red');
            $(".phone-wrong").html("请输入正确的手机号").addClass("wrong");
            console.log($(".phone-wrong"));
            $(".verification-code button").removeClass("able").addClass("disable").attr("disabled","disabled");
        }
    });
    $(".phoneNum").focus(function () {
        $(this).css("color","black");
        $(".phone-wrong").html("").removeClass("wrong");
    });

    //验证码 正确验证
    $(".verification-code input").blur(function () {
        // console.log($(this));
        var verCode = 1234;
        if(verCode === $(this).val()){
            $(this).css("color","green");
        }else{
            $(this).css("color","red");
            $(".vCodeWrong").html("验证码错误").addClass("wrong");
        }
    });
    $(".verification-code input").focus(function () {
        $(this).css("color","black");
        $(".vCodeWrong").html("").removeClass("wrong");
    });


    //邮箱合格验证
    $(".mailbox").blur(function () {
        var reg2 = /^[_a-z 0-9]+@([_a-z 0-9]+\.)+[a-z 0-9]{2,3}$/;
        var mailbox = $(this).val();
        if(reg2.test(mailbox)){
            $(this).css("color","green");
        }else {
            $(".mailWrong").html("邮箱格式不正确").addClass("wrong");
        }
    });
    $(".mailbox").focus(function () {
        $(this).css("color","black");
        $("mailWrong").html("").removeClass("wrong");
    });

    

    //两次密码比对验证
    //第二次输入密码后，进行比对
    $(".code2").blur(function () {
        var code1 = $(".code1").val();
        var code2 = $(".code2").val();
        if(code1 !== code2){
            $(".codeWrong").html("两次密码不一样").addClass("wrong");
        }
    });

    //重新输入
    $(".code1").focus(function () {
        codeWrongHide();
    });
    $(".code2").focus(function () {
        codeWrongHide();
    });
    function codeWrongHide() {
        $(".codeWrong").html("").removeClass("wrong");
    }

    
    //提交注册
    $(".reg-submit input").click(function () {
        //手机空
        var phone = $(".phoneNum").val();
        if(phone === ""){
            alert("请输入手机号");
        }

        //验证空
        var vCode = $(".verification-code input").val();
        if(vCode === ""){
            alert("请输入验证码");
        }

        //邮箱空
        var mail = $(".mailbox").val();
        if(mail === ""){
            alert("请输入邮箱");
        }

        //密码空
        var code1 = $(".code1").val();
        var code2 = $(".code2").val();
        if(code1 === "" || code2 === ""){
            alert("请输入密码");
        }
    });
    




});