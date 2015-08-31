// Apprise 1.5 by Daniel Raftery
// http://thrivingkings.com/apprise
//
// Button text added by Adam Bezulski
//

$(document).keydown(function(e){
		
	
		if(e.keyCode == 27){ 
			closeNotif();
			closeApprise();
		}
	
});
jQuery.fn.doesExist = function(){return this.length>0;}

function set_overlay(args,n){
	
	
	$('body').append('<div class="appriseOverlay" id="aOverlay'+n+'"></div>');
	$('#aOverlay').append('<div class="appriseOuter" id="aOuter'+n+'"></div>');
	$('#aOuter'+n+'').append('<div id="aInner'+n+'" class="appriseInner"></div>');
	
	if(args.index){
		current_index = $("#aOverlay").css("z-index");
		
		$('#aOverlay'+n+'').css("z-index",current_index+args.index);
		$('#aOuter'+n).css("z-index",current_index+args.index+1);
	}
	
	
	// ini untuk website radiaranai
	if($("#wrapper").doesExist()){
		var margin = $("body").width() - $("#wrapper").width();
		$("#wrapper").css({left:(margin/2)});
	}
	
    /* important part */
	var top = $(document).scrollTop();
	var width = $(window).width();
	$("body div:first").css({position:"fixed",top:top*(-1),width:width});
	
}

function apprise(args, callback){
	//cek session dulu
	
	$.post("/",{ajax:"yes"},function(data){
		if(data=="session_end"){
			document.location="/"; 
			return;
		}
	});
	
	if(!args['textOk'])
		args['textOk'] = 'Simpan';
	args['textCancel'] = 'Batal';
	
	n = "";
	if(args.index){
		n += args.index;
	}
	
	
	set_overlay(args,n);
	
	if(args.onClose){
		$('#aOverlay'+n).on("remove", function () {
			args.onClose();
		});
	}
	
	post_data = {};
	if(args.post_data){
		post_data = args.post_data;
	}
	appriseLoading("#aOuter");
	$('#aInner'+n).load(args.url,post_data,function(){
		closeLoading();
		if(args.value){
			val = args.value;
			$.each(val,function(index,value){
				$("#"+index).val(value);
			});
		}
		
		$("#apprise_title").html(args.title);
		
		$('#aInner'+n).append("<div class='close' onclick='closeApprise("+n+")' title='Close'></div>");
		
		$('#aInner'+n+'').append('<div class="aButtons"></div>');
		if(!args.closeOnly){ 
			$('.aButtons').append('<button value="ok"  >'+args['textOk']+'</button>'); 
			$('.aButtons').append('<button value="cancel" >'+args['textCancel']+'</button>');
		}else{
			//$('.aButtons').append('<button value="cancel" >Close</button>');
		}
		$('.aButtons > button').click(function(){
			if(callback){
				var wButton = $(this).attr("value");
				if(wButton=='ok'){ 
					appriseLoading('#aInner'+n);
					
					callback();
				}else if(wButton=='cancel'){ 
					
					closeApprise();
				}
			}
		});
		
		
	});
	
	
}

function preview(args, callback){
	
	args['textOk'] = 'Ok';
	args['textCancel'] = 'Batal';
	
	n = "";
	if(args.index){
		n += args.index;
	}
	
	set_overlay(args,n);
	
	$('#aInner'+n).html($("#"+args.content).html());

	if(args.value){
		val = args.value;
		$.each(val,function(index,value){
			$("#"+index).val(value);
		});
	}
	
	$("#apprise_title").html(args.title);
	
	$('#aInner'+n).append("<div class='close' onclick='closeApprise("+n+")' title='Close'></div>");
	
	$('#aInner'+n+'').append('<div class="aButtons"></div>');
	if(!args.closeOnly){ 
		$('.aButtons').append('<button value="ok"  >'+args['textOk']+'</button>'); 
		$('.aButtons').append('<button value="cancel" >'+args['textCancel']+'</button>');
	}else{
		//$('.aButtons').append('<button value="cancel" >Close</button>');
	}
	$('.aButtons > button').click(function(e){
		if(callback){
			var wButton = $(this).attr("value");
			if(wButton=='ok'){ 
				appriseLoading('#aInner'+n);
				
				callback(e);
			}else if(wButton=='cancel'){ 
				
				closeApprise();
			}
		}else{
			closeApprise();
		}
	});
	
}

function appriseLoading(selector){
	$(selector).append("<div class='loader_overlay'><div class='apprise_loader'></div></div>");
}


function closeLoading(){
	$(".loader_overlay").remove();
}


function setPos(n){
	
}


function notif(title,callback,confirm){
	
	var aHeight = $(document).height();
	var aWidth = $(document).width();
	
	var top = $(document).scrollTop();
	var width = $("body div:first").width();
	var margin = $("body").width() - width;
	$("body div:first").css({
		position:"fixed",
		top:top*(-1),width:width,
		left:(margin/2)
	});
	
	if(!$(".notifInner").doesExist()){
		$('body').append('<div class="notifOverlay" id="aNotifOverlay"></div>');
		//$('.notifOverlay').css('height', aHeight).css('width', aWidth).fadeIn(100);
		$('.notifOverlay').append('<div class="notifOuter"></div>');
		$('.notifOuter').append('<div class="notifInner"></div>');
		
		var aniSpeed = 400; 
		$('.notifOuter').show();//.animate({top:"100px"}, aniSpeed);
	}else{
		$('.notifInner').empty();
	}
	
	
	
	$('.notifInner').append('<div style="font-size:15px;">'+title+'</div>');
	$('.notifInner').append('<div class="aNotifButtons" "></div>');
	$('.aNotifButtons').append('<button id="btn_ok_notif" style="width:70px; float:left;" value="ok"  >OK</button>');
	if(confirm){
		$('.aNotifButtons').append('<button style="width:70px; float:right;" value="cancel" >Batal</button>');
	}else{
		margin = ($('.aNotifButtons').width() - $('#btn_ok_notif').width())/2;
		$('#btn_ok_notif').css({marginLeft:margin});
	}
	$("#btn_ok_notif").focus();
	
	
	$('.aNotifButtons > button').click(function(){
		var wButton = $(this).attr("value");
		if(wButton=='ok'){ 	
			if(callback){				
				appriseLoading('.notifInner');
				callback();
			}else{
				closeNotif();
			}
		}else{
			closeNotif();
		}
	});

    
    
}


function closeNotif(){
	$('.notifOverlay').remove();
	$('.notifOuter').remove();
	var top = $("body div:first").css("top").replace(/[^-\d\.]/g, '');
	
	top *= -1;
	
	$("body div:first").css({position:"",margin:"",top:""});
	$(document).scrollTop(top);
}


function closeApprise(n){
	b="";
	if(n){
		b = n;
	}
	$('#aOverlay'+b).remove();
	$('#aOuter'+b).remove();
	
	var top = $("body div:first").css("top").replace(/[^-\d\.]/g, '');
	
	top *= -1;
	
	$("body div:first").css({position:"",margin:"",top:""});
	$(document).scrollTop(top);
}
