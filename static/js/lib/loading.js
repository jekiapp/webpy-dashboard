jQuery.fn.extend({
	loading: function(){
		$(this).css("position","relative");
		var top = $(this).height()/2;
		top -= 32; // ketinggian dari gif
		shade = "<div id='loading' style='background-color:rgba(239,237,224,0.5); position:absolute; height:100%; width:100%; top:0; text-align:center; '><img style='padding-top:"+top+"px;' src='/static/images/loader.gif'/></div>";
		$(this).append(shade);
	}
});