function reset_password(){
	notif("apakah anda yakin",function(){
		$.post(".",{'reset_password':1},function(response){
			data = getJSON(response);
			//console.log(data);
			notif("ini password barunya : <bold>"+data.password+"</bold>",function(){
				closeNotif();
			});
		});
		
	},true);
}