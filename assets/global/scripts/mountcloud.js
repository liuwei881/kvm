$(function() {
    $("#hostForm").validate({
        debug: true,
        errorClass: "alert-danger", //默认为错误的样式类为：error
        focusInvalid: true, //当为false时，验证无效时，没有焦点响应
        onkeyup: false,
        submitHandler: function(form){   //表单提交句柄,为一回调函数，带一个参数：form
        sendReq('/clouddisk/add/',$('#hostForm').serialize(),'get');
        },
        });
    $("#hostForm-create").validate({
        debug: true,
        errorClass: "alert-danger", //默认为错误的样式类为：error
        focusInvalid: true, //当为false时，验证无效时，没有焦点响应
        onkeyup: false,
        submitHandler: function(form){   //表单提交句柄,为一回调函数，带一个参数：form
        sendReq('/clouddisk/mountclouddisk/{{h.id}}/',$('#hostForm-create').serialize(),'get');
        },
        });
})