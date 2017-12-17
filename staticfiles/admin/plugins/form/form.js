function form_validation(classname){
    can_submit = true;
    var classstr = "." + classname;
    $('.prompt').hide();
    $(classstr).each(function(){
        if (!$(this).val()){
            var message = "<p class='prompt' style='color:red'>请填写" + $(this).prev().text() + "</p>";
            $(this).after(message);
            can_submit = false;
        }else {
            $(this).next().hide();
        }
    })
    return can_submit;
}