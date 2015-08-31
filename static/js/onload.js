$(document).ready(function(){

	$("#pikame").PikaChoose({
		transition:[0],
		autoPlay:true,
	});
	
	$(".menu").hover(
	function(){
		submenu = $(this).children(".submenu")[0];
		$(submenu).show();
	},
	function(){
		submenu = $(this).children(".submenu")[0];
		$(submenu).hide();
	});
	
});