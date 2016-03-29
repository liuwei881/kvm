/*
 * 发送ajax异步请求
 * url 域内地址 不可跨域
 * data: json
 * type: post/get	default=post
 * issync:1/0	default=1 
 */ 
function sendReq(url,data,type,successFun,failedFun){
	if(!type){
		type = 'post';
	}
	if(successFun == 'undefined' || successFun == undefined || !successFun)
	    successFun == '';
	if(failedFun == 'undefined' || failedFun == undefined || !failedFun)
	    successFun == '';
	$.ajax({
		type: type,
	   	url: url,
	   	data: data,
	   	success: function(rs){

	   	if(rs.status==200){
	   		eval(successFun);
		   	showAjaxReturnInfo('success',rs.msg,1);
//		   	当页面实现json渲染后可开启下方部分进行局部刷新
//		   	var el = $(".portlet-body");
//            if (url) {
//                Metronic.blockUI({
//                    target: el,
//                    animate: true,
//                    overlayColor: 'none'
//                });
//                $.ajax({
//                    type: "GET",
//                    cache: false,
//                    url: url,
//                    dataType: "html",
//                    success: function(res) {
//                        Metronic.unblockUI(el);
//                        el.html(res);
//                    }
//                });
//            }
		}else{
			eval(failedFun);
			showAjaxReturnInfo('failed',rs.msg);
		}
	   },
	   error(rs){
	   		eval(failedFun);

	   }
	});
}

function showAjaxReturnInfo(type,msg,is_reload){
	var addclass 	= 'mainShowAjaxInfoSuccess';
	if(type == 'failed'){
		addclass 	= 'mainShowAjaxInfoFailed';
		if(msg == '' || msg == undefined){
			msg = '请求失败，请稍后重试';
		}
	}
	var showObj = $('#mainShowAjaxInfoBase');
	showObj.addClass(addclass).text(msg).fadeIn(200,function(){
			setTimeout(function(){
				showObj.fadeOut(300,function(){
					showObj.removeClass(addclass).text('');
					if(is_reload==1){
						location.reload();
					}
				});
			},500);
	});

}