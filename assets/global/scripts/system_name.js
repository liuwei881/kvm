
var mirror_name=[
    ["win2008","windows_standard","windows_datacenter"],  //����ϵͳ
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
                errorClass: "alert-danger", //Ĭ��Ϊ�������ʽ��Ϊ��error
                focusInvalid: true, //��Ϊfalseʱ����֤��Чʱ��û�н�����Ӧ
                onkeyup: false,
                submitHandler: function(form){   //���ύ���,Ϊһ�ص���������һ��������form
                    sendReq('/webkvm/addHost/',$('#hostForm').serialize(),'get');
                                             },
                                     });
              })