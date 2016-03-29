$(function() {
            $("#addProForm").validate({
                debug: true,
                errorClass: "alert-danger", //默认为错误的样式类为：error
                focusInvalid: true, //当为false时，验证无效时，没有焦点响应
                onkeyup: false,
                submitHandler: function(form){   //表单提交句柄,为一回调函数，带一个参数：form
                    sendReq('/pro/add/',$('#addProForm').serialize(),'post',"$('#myModal-addPro').modal('hide')");
                },
                rules: {
                    pro_name: {
                        required : true,
                    },
                    c_cpu: {
                        required : true,
                        digits : true,
                        range: [1,100]
                    },
                    c_disk: {
                        required : true,
                        digits : true,
                        range: [1,10]
                    },
                    c_space: {
                        required : true,
                        digits : true,
                        range: [100,10240]
                    }
                },
                messages: {
                    pro_name: {
                        required: '项目名不能为空',
                    },
                    c_cpu: {
                        digits: '请输入1-100范围内的正整数',
                        range: "请输入1-100范围内的正整数"
                    },
                    c_disk: {
                        digits: '请输入1-10范围内的正整数',
                        range: "请输入1-10范围内的正整数"
                    },
                    c_space: {
                        digits: '请输入100-10240范围内的正整数',
                        range: "请输入1-10240范围内的正整数"
                    }
                }
            });
            $("#editProForm").validate({
                debug: true,
                errorClass: "alert-danger", //默认为错误的样式类为：error
                focusInvalid: true, //当为false时，验证无效时，没有焦点响应
                onkeyup: false,
                submitHandler: function(form){   //表单提交句柄,为一回调函数，带一个参数：form
                    sendReq('/pro/edit/',$('#editProForm').serialize(),'post',"$('#myModal-editPro').modal('hide')");
                },
                rules: {
                    c_cpu: {
                        required : true,
                        digits : true,
                        range: [1,200]
                    },
                    c_disk: {
                        required : true,
                        digits : true,
                        range: [1,10]
                    },
                    c_space: {
                        required : true,
                        digits : true,
                        range: [100,10240]
                    }
                },
                messages: {
                    c_cpu: {
                        digits: '请输入1-200范围内的正整数',
                        range: "请输入1-200范围内的正整数"
                    },
                    c_disk: {
                        digits: '请输入1-10范围内的正整数',
                        range: "请输入1-10范围内的正整数"
                    },
                    c_space: {
                        digits: '请输入100-10240范围内的正整数',
                        range: "请输入1-10240范围内的正整数"
                    }
                }
            });
        });
        function editPro(id){
            $.get('/pro/getProInfo/'+id,'',function(r){
                if(r.status==200){
                    var editForm = $('#myModal-editPro');
                    editForm.find('form')[0].reset();
                    editForm.find('#pro_name').val(r.data.pro_name);
                    editForm.find('#pro_desc').val(r.data.pro_desc);
                    editForm.find('#c_cpu').val(r.data.c_cpu);
                    editForm.find('#c_sapce').val(r.data.c_sapce);
                    editForm.find('#c_memory').val(r.data.c_memory);
                    editForm.find('#c_disk').val(r.data.c_disk);
                    editForm.find('#pro_id').val(r.data.id);
                    editForm.find('#admin_id').val(r.data.admin_id);
                    $('#myModal-editPro').modal();
                }
            },'json');
        }
        function editMembers(pro_id){
            $.get('/pro/getProMembersInfo/'+pro_id,'',function(r){
                if(r.status==200){
                    var editForm = $('#myModal-editMember');
                    editForm.find('#choosePos').html(r.data.ht);
                    editForm.find('#pro_name').text(r.data.pro_name);
                    editForm.find('#pro_id').val(r.data.pro_id);
                    $('#myModal-editMember').modal();
                }
            },'json');
        }