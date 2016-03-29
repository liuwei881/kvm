$(function() {
    $("#userForm").validate({
        debug: true,
        errorClass: "alert-danger", //默认为错误的样式类为：error
        focusInvalid: true, //当为false时，验证无效时，没有焦点响应
        onkeyup: false,
        submitHandler: function(form){   //表单提交句柄,为一回调函数，带一个参数：form
            sendReq('/users/add/',$('#userForm').serialize(),'post',"$('#myModal-add').modal('hide')");
        },
        rules: {
            username: {
                required: true,
                minlength: 2
            },
            password: {
                required: true,
                minlength: 1
            },
            confirm_password: {
                required: true,
                minlength: 1,
                equalTo: "#password"
            },
            email: {
                email: true
            }
        },
        messages: {
            username: {
                required: '用户名不能为空',
                minlength: 6
            },
            password: {
                required: "请输入密码",
                minlength: 6
            },
            confirm_password: {
                required: "请再次输入密码",
                minlength: "密码不能小于6个字符",
                equalTo: "两次输入密码不一致"
            },
            email: {
                email: "请输入正确的邮箱地址",
            }
        }
    });
    $("#userFormEdit").validate({
        debug: true,
        errorClass: "alert-danger", //默认为错误的样式类为：error
        focusInvalid: true, //当为false时，验证无效时，没有焦点响应
        onkeyup: false,
        submitHandler: function(form){   //表单提交句柄,为一回调函数，带一个参数：form
            sendReq('/users/edit/',$('#userFormEdit').serialize(),'post',"$('#myModal-edit').modal('hide')");
        },
        rules: {
            id:{
                required:true
            },
            password: {
                minlength: 1
            },
            repassword: {
                minlength: 1,
                equalTo: "#passwordEdit"
            },
            email: {
                email: true
            }
        },
        messages: {
            id :{
                required:'无法获取UID请刷新页面重试'
            },
            password: {
                minlength: "密码不能小于6个字符"
            },
            repassword: {
                minlength: "密码不能小于6个字符",
                equalTo: "两次输入密码不一致"
            },
            email: {
                email: "请输入正确的邮箱地址",
            }
        }
    });
    $('#saveUserProInfo').click('click',function(){
        sendReq('/users/editUserProInfo/'+ $('#userProFormEdit').find('#user_id').val()+'/',$('#userProFormEdit').serialize(),'post',"$('#myModal-editPro').modal('hide')");
    });
});
function editUser(id){
    $.get('/users/getUserInfo/'+id,'',function(r){
        if(r.status==200){
            var editForm = $('#myModal-edit');
            editForm.find('form')[0].reset();
            editForm.find('#username').val(r.data.username);
            editForm.find('#email').val(r.data.email);
            if(r.data.is_active==true)
                editForm.find('#is_active').val(1);
            else
                editForm.find('#is_active').val(0);
            editForm.find('#userid').val(r.data.id);
            $('#myModal-edit').modal();
        }
    },'json');
}
function showUserProInfo(id){
    $.post('/users/getUserProInfo/'+id+'/','',function(r){
        if(r.status==200){
            var editForm = $('#myModal-editPro');
            editForm.find('form')[0].reset();
            editForm.find('#username').text(r.data.username);
            editForm.find('#user_id').val(r.data.user_id);
            editForm.find('#proHtml').html(r.data.html);
            $('#myModal-editPro').modal();
        }
    },'json');
}