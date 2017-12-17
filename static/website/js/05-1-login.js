/**
 * Created by Administrator on 2017/8/8 0008.
 */
window.onload = function () {
    getCookie();
};
function setCookie(){ //设置cookie
    var loginCode = $("#login_code").val(); //获取用户名信息
    console.log(loginCode);
    var pwd = $("#login_password").val(); //获取登陆密码信息
    console.log(pwd);
    var checked = document.getElementById("auto-login").checked; //获取“是否记住密码”复选框

    if(checked){ //判断是否选中了“记住密码”复选框
        $.cookie("login_code",loginCode);//调用jquery.cookie.js中的方法设置cookie中的用户名
        $.cookie("pwd",$.base64.encode(pwd));//调用jquery.cookie.js中的方法设置cookie中的登陆密码，并使用base64（jquery.base64.js）进行加密
    }else{
        $.cookie("pwd", null);
    }
}
function getCookie(){ //获取cookie
    var loginCode = $.cookie("login_code"); //获取cookie中的用户名
    var pwd =  $.cookie("pwd"); //获取cookie中的登陆密码
    if(pwd){//密码存在的话把“记住用户名和密码”复选框勾选住
        $("[name='checkbox']").attr("checked","true");
    }
    if(loginCode){//用户名存在的话把用户名填充到用户名文本框
        $("#login_code").val(loginCode);
    }
    if(pwd){//密码存在的话把密码填充到密码文本框
        $("#login_password").val($.base64.decode(pwd));
    }
}
function login(){
    var userName = $('#login_code').val();
    if(userName == ''){
        alert("请输入用户名。");
        $('#login_code').select();
        return;
    }
    var userPass = $('#login_password').val();
    if(userPass == ''){
        alert("请输入密码。");
        $('#login_password').select();
        return;
    }



    //判断是否选中复选框，如果选中，添加cookie
    var checked = document.getElementById("auto-login").checked; //获取“是否记住密码”复选框
    if(checked) {
        //添加cookie
        setCookie();
        // alert("记住密码登录。");
        // window.location = "http://www.baidu.com";
    }
    // else{
    //     alert("不记密码登录。");
    //     window.location = "http://www.baidu.com";
    // }
}