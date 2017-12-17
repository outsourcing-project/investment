/**
 * Created by Administrator on 2017/10/8 0008.
 */
$(document).ready(function () {
    //tab2-发布房源
    //基础设施选择
    var SetLis = $("#tab2 .surrounding-facilities").find("li");
    for(var i = 0;i < SetLis.length;i++){
        $(SetLis[i]).click(function () {
            var box = $(this).find('input');
            if(box.attr('checked') === 'checked'){
                box.removeAttr('checked');
            }else{
                box.attr('checked','true');
            }
        });
    }
    //增加卧室
    var roomHeight = $('.bedroom').height();
    $('.addBedroom').click(function () {
        var newBedroom = document.createElement('div');
        newBedroom.className = 'bedroom';
        newBedroom.innerHTML = '<h5>卧室</h5><p><label>面积：</label><input class="area" type="text">&nbsp m³</p><p>房间配置：<label>飘窗 </label><input type="checkbox" name="details">&nbsp&nbsp<label>空调 </label><input type="checkbox" name="details">&nbsp&nbsp<label>床 </label><input type="checkbox" name="details">&nbsp&nbsp<label>书桌 </label><input type="checkbox" name="details">&nbsp&nbsp<label>衣柜 </label><input type="checkbox" name="details">&nbsp&nbsp<label>沙发 </label><input type="checkbox" name="details">&nbsp&nbsp<label>独立卫生间 </label><input type="checkbox" name="details"></p><span class="close">X</span>';
        $('.addBedroom').before(newBedroom);
        // $(".tab_container").css("height",$(".tab_container").height() + roomHeight);
        // $(".tabs").css("height",$(".tab_container").height());
        console.log($('.bedroom'));
    });

    //客厅
    if($('#yes').checked){

    }

    //删除卧室
    $(document).on('click','.house-release .bedroom .close',(function () {
        this.parentNode.parentNode.removeChild(this.parentNode);
        $(".tab_container").css("height",$(".tab_container").height() - roomHeight);
        $(".tabs").css("height",$(".tab_container").height());
    }));

    //上传房产证 图片预览
    var
        fileInput = document.getElementById('test-image-file'),
        preview = document.getElementById('test-image-preview');
    // 监听change事件:
    fileInput.addEventListener('change', function () {
        // 清除背景图片:
        preview.style.backgroundImage = '';
        // 检查文件是否选择:
        if (!fileInput.value) {
            info.innerHTML = '没有选择文件';
            return;
        }
        // 获取File引用:
        var file = fileInput.files[0];
        // 读取文件:
        var reader = new FileReader();
        reader.onload = function(e) {
            var
                data = e.target.result; // 'data:image/jpeg;base64,/9j/4AAQSk...(base64编码)...'
            preview.style.backgroundImage = 'url(' + data + ')';
        };
        // 以DataURL的形式读取文件:
        reader.readAsDataURL(file);
    });
});