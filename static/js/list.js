function page(obj,url){
	p = $(obj).val();
	document.location=url+"p/"+p;
}

function search(url){
	
	txt = $(".search #txt").val();
	document.location = url+"search/"+txt;
	return false;
}

function del(obj,id){
	notif("apakah yakin menghapus data ini?",function(){
		$.get("delete/"+id,function(resp){
			console.log(resp);
			closeNotif();
			location.reload()
		});
	},true);
}

function prev_month(){
	$("#frm_month #nav").val("0");
	$("#frm_month").submit();
}

function next_month(){
	$("#frm_month #nav").val("1");
	$("#frm_month").submit();
}