/**
 * Created by Administrator on 2017/10/8 0008.
 */
//tab5-房源发布
//日历
$(document).ready(function () {
    $('#selectDate').datepicker({
        dateFormat: 'yy-mm-dd',
        monthNames: ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月']
    });
});

//基础设施
var SettingLis = $("#tab5 .surrounding-facilities").find("li");
for(var i = 0;i < SettingLis.length;i++){
    $(SettingLis[i]).click(function () {
        var box = $(this).find('input');
        if(box.attr('checked') === 'checked'){
            box.removeAttr('checked');
        }else{
            box.attr('checked','true');
        }
    });
}


//手机验证
var inp = document.getElementById('phoneNum');
inp.onfocus = function () {
    this.select();
};
inp.onblur = function () {
    console.log(11);
    var reg1 = /^(13[0-9]|15[0|3|6|7|8|9]|18[8|9])\d{8}$/;
    if(reg1.test(inp.value)){
        //3、符合个给一个样式，不符合给另一个样式
        inp.style.color = "green";

    }else{
        inp.style.color = "red";
        inp.value = inp.value+"  请输入正确的手机号码";
    }
};