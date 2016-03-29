
var mirror_name=[
    ["win2008","windows_standard","windows_datacenter"],  //操作系统
    ["centos6","centos6lnmp","ruby-base","data-zi","centos7","ubuntu"]
    ];

function getostype(){
    var sltProvince=document.forms["theForm"].elements["system"];
    var sltMirror=document.forms["theForm"].elements["mirror_name"];
    var provinceOs=mirror_name[sltProvince.selectedIndex-1];

    sltMirror.length=1;
 
    for(var i=0;i<provinceOs.length;i++){
    sltMirror[i+1]=new Option(provinceOs[i],provinceOs[i]);
    }
}

$(function() {
            $("#hostForm").validate({
                debug: true,
                errorClass: "alert-danger", //默认为错误的样式类为：error
                focusInvalid: true, //当为false时，验证无效时，没有焦点响应
                onkeyup: false,
                submitHandler: function(form){   //表单提交句柄,为一回调函数，带一个参数：form
                    sendReq('/webkvm/addHost/',$('#hostForm').serialize(),'get');
                                             },
                                     });
              })