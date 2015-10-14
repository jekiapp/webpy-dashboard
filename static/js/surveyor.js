
function blacklist(obj,id){
	notif("Apakah yakin memblacklist surveyor ini?<br/>Semua data pemilih dari surveyor ini akan dihapus",
	function(){
		$.post(base_url+"blacklist/",{id:id},function(resp){
			console.log(resp);
			closeNotif();
			location.reload();
		});
	},true);
}
function aktif(obj,id){
	notif("Apakah yakin mengaktifkan kembali surveyor ini?",
	function(){
		$.post(base_url+"aktif/",{id:id},function(resp){
			console.log(resp);
			closeNotif();
			location.reload();
		});
	},true);
}