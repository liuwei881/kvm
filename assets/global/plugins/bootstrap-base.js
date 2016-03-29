/*!
 * extend bootstrap by ZhangYunling v1.0.1
 * 
 * extend some method we used often
 * 
 * Copyright 2014, ZhangYunling
 *  
 * Date: 2014-11-30
 */

var extendBoot = (function($){
	//这里定义一下一些基本的信息。
	var loadingImg = "http://www.zhangyunling.com/images/loading.gif";
	
	function Mesbox(options){
		/*
			//options中包含的一些信息
			//title表示title的名称
			//id，表示生成的div的id名称
			//type，表示弹出框的类型，
				分为：alert，单纯提示信息
					confirm，选择
					ajax，会有ajax的请求类型的
					
			//getContent，可以是一个回调函数，返回的内容会被显示。
				或者一段需要显示的文本，表示生成的的内容部分的结构
				
			//applyName，确认按钮的名称
			//applyFn，点击确认按钮时，会触发的功能函数
			//cancelName，取消按钮的名称
			//confirmType，confirm点击确认之后，接下来的动作，
				如果取值为ajax，则确认之后，触发applyFn函数，
				applyFn函数内是继续type = "ajax"的模态框方法
				
			//ajaxOptions，如果type=ajax时，ajax的请求，按照该对象的内容处理
				{
					url:请求地址
					type:ajax请求类型，get或者post
					data:参数
					dataType:返回类型，默认为json类型
					success:成功之后的回调
					showResultType:回调成功之后，信息的显示模式
					//取值暂时只有"alert"，回调成功之后，以alert的形式展示信息
					//如果不设置该值，那么需要自己在success函数内部，自行处理
				}
		*/
		if(options.id && $(options.id).size() != 0){
			alert("您的在调用Mbox时，设置了重复id="+options.id+"，请确修改！");
			return false;
		}
		
		options.doc = options.doc || document;
		options.title = options.title || "信息提示";
		options.type = options.type || "alert";
		
		options.loaddingDiv = "<div style = 'padding-top:10px;padding-bottom:10px;text-align:center;'><img src = '"+loadingImg+"' /></div>";
		options.applyName = options.applyName || "Apply";
		options.cancelName = options.cancelName || "Close";
		
		//缓存一下使用function生成的文本的结构，如果使用相同的function生成的话，
		//直接读取缓存，降低时间
		options.contentsCache = {
			num:0,
		};
		this.options = options;

		this.doc = $(options.doc);

		this.createBox();
		
		//更换title的显示
		this.initTitle(options.title);
		
		//更新content部分
		this.initContent(options);
		
		//初始化footer部分的显示
		this.initfooter(options);
		//事件的绑定处理
		this.btnFn(options);
	}
	
	Mesbox.prototype.createBox = function(){
		if(this.Mbox){
			return "";
		}
		var options = this.options,
			doc = this.doc,
			html = '<div class="modal fade" id = "'+(options.id || "")+'">'+
				'<div class="modal-dialog">'+
					'<div class="modal-content">'+
						'<div class="modal-header">'+
							'<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>'+
							'<h4 class="modal-title">'+options.title+'</h4>'+
						'</div>'+
						'<div class="modal-body"></div>'+
						'<div class="modal-footer">'+
							'<button type="button" class="btn btn-primary applyMbox"></button>'+
							'<button type="button" class="btn btn-default closeMbox" style = "margin-left:20px;" data-dismiss="modal"></button>'+
						'</div>'+
					'</div>'+
				'</div>'+
			'</div>';
			
		this.Mbox = $(html);
		
		var Mbox = this.Mbox;
		
		$(document.body).append(Mbox);
		
		if(!options.container){
			options.header = Mbox.find(".modal-header");
			options.titler = Mbox.find(".modal-title");
			options.container = Mbox.find(".modal-body");
			options.footer = Mbox.find(".modal-footer");
			options.apply = Mbox.find(".applyMbox");
			options.close = Mbox.find(".closeMbox");
		}
	};
	
	Mesbox.prototype.showMbox = function(){
		this.Mbox.modal({show:true,backdrop:"static"});
	};
	
	Mesbox.prototype.hideMbox = function(){
		this.Mbox.modal('hide');
	}
	
	Mesbox.prototype.reDefineMbox = function(option){
		/**
			*option的值，和Mesbox时的类型相同
			如果这时有option的输入，则后面的输入使用option，
			如果没有，则使用this.options
		*/
		
		//$.extend(this.options,option);
		
		var options = this.options;
		option = option || options || "";

		if(!option){
			//如果为空，则提示错误
			this.reDefineMbox({
				type:"alert",
				getContent:"您调用reDefineMbox方法时，出现错误，请确认"
			});
			return false;
		}
		//更换title的显示
		this.initTitle(option.title);
		
		//更新content部分
		this.initContent(option);
		
		//初始化footer部分的显示
		this.initfooter(option);
		//事件的绑定处理
		this.btnFn(option);
			
		//显示模态框
		this.showMbox();
	}
	
	Mesbox.prototype.initTitle = function(title){
		//初始化title
		title = title || "";
		var options = this.options;
		
		if(title){
			options.titler.html(title);
		}
	}
	
	Mesbox.prototype.initContent = function(option){
		//初始化内容的模块显示部分
		option = option || {};
		var options = this.options,
			contentsCache = null,
			getContent = option.getContent || options.getContent,
			content = "",
			mboxNum = 0;
			
		if(typeof getContent == "function"){
			//如果有getContent，并且为function，则使用function返回的作为html结构
			contentsCache = options.contentsCache;
			if(getContent.mboxNum){
				mboxNum = getContent.mboxNum;
				content = contentsCache[mboxNum];
			}
			if(!content){
				content = getContent.call(this.Mbox);
				if(mboxNum){
					contentsCache[mboxNum] = content;
				}else{
					mboxNum = "C"+contentsCache.num;
					contentsCache.num++;
					contentsCache[mboxNum] = content;
					getContent.mboxNum = mboxNum;
				}
			}
			options.container.html(content);	
		}else{
			options.container.html(getContent);
		}
	}
	
	Mesbox.prototype.initfooter = function(option){
		//初始化footer部分，并且该部分的提交的点击事件
		option = option || {};
		var options = this.options,
			type = option.type || options.type,
			Mbox = this.Mbox,
			apply = options.apply,
			cancel = options.close,
			applyName = option.applyName || options.applyName,
			cancelName = option.cancelName || options.cancelName;
			
		options.footer.show();
		cancel.text(cancelName).removeClass("btn-primary");
		apply.text(applyName).show();
		
		if(type == "alert"){
			//只有当显示为alert显示时，才会更改
			apply.hide();
			cancel.text("确认").addClass("btn-primary");
		}
	};
	
	Mesbox.prototype.btnFn = function(option){
		//给确认按钮添加点击事件
		option = option || {};
		var options = this.options,
			type = option.type || options.type;

		switch(type){
			case "alert":this.alertFn(option);break;
			case "confirm":this.confirmFn(option);break;
			case "ajax":this.ajaxFn(option);break;
			default:break;
		}
	}
	
	Mesbox.prototype.alertFn = function(option){
		//调用类似alert的模态框
		option = option || this.options || {};
		var options = this.options,
			cancel = options.close,
			that = this,
			applyFn = option.applyFn
			that = this;

		cancel.off("click");
		cancel.on("click",function(){
			if(typeof applyFn == "function"){
				applyFn.call(that.Mbox);
			}
			that.hideMbox();
		});
	};
	
	Mesbox.prototype.confirmFn = function(option){
		//调用类似confirm的模态框
		option = option || this.option || {};
		var options = this.options,
			apply = options.apply,
			that = this,
			applyFn = option.applyFn,
			confirmType = option.confirmType || "";
			
		apply.off("click");
		apply.on("click",function(){
			if(typeof applyFn == "function"){
				applyFn.call(that.Mbox);
			}
			if(confirmType != "ajax"){
				//如果这个confirm之后，跟的不是ajax请求，就隐藏该模态框
				//如果接下来是ajax请求，则直接进行ajax的请求
				that.hideMbox();
			}
		});
	}
	
	Mesbox.prototype.ajaxFn = function(option){
		var options = this.options,
			ajaxOptions = option.ajaxOptions || options.ajaxOptions || {};
			
		this.ajax(this,ajaxOptions);
	}
	
	Mesbox.prototype.ajax = function(obj,option){
		var that = this;
		
		if(!(option.url || "")){
			this.reDefineMbox({
				title:"信息错误",
				type:"alert",
				getContent:"您的ajax请求的url为空！"
			});
			return false;
		}
		
		//如果可以提交，则转成正在提交的图标
		var showResultType = option.showResultType || "";
		
		this.loading();
		option.dataType = option.dataType || "json";
		$.ajax({
			url: option.url,
			type: option.type || "POST",
			data: option.data,
			dataType: option.dataType,
			success: function(json){
				var needCallBack = true;
				if(option.dataType == "json"){
					json = typeof json == "string"?$.parseJSON(json):json;
					if(showResultType == "alert" && json.msg){
						needCallBack = false;
						that.reDefineMbox({
							title:"操作结果",
							type:"alert",
							getContent:json.msg,
							applyFn:function(){
								if(typeof option.success == "function"){
									option.success.call(obj,json);
								}
							}
						});
					}
				}
				
				if(needCallBack && typeof option.success == "function"){
					option.success.call(obj,json);
				}
			},
			error: function() {
				that.reDefineMbox({
					title:"提交失败",
					type:"alert",
					getContent:"由于网络的原因，您刚才的操作没有成功。"
				});
			}
		});
	};
	
	Mesbox.prototype.loading = function(){
		var options = this.options;
		options.footer.hide();
		options.container.html(options.loaddingDiv);
	}
	
	return {
		Mesbox:Mesbox
	}
})(jQuery);