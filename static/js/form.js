var dtCh= "/";
var minYear=1900;
var maxYear=2100;

function isInteger(s){
	var i;
    for (i = 0; i < s.length; i++){   
        // Check that current character is number.
        var c = s.charAt(i);
        if (((c < "0") || (c > "9"))) return false;
    }
    // All characters are numbers.
    return true;
}

function stripCharsInBag(s, bag){
	var i;
    var returnString = "";
    // Search through string's characters one by one.
    // If character is not in bag, append to returnString.
    for (i = 0; i < s.length; i++){   
        var c = s.charAt(i);
        if (bag.indexOf(c) == -1) returnString += c;
    }
    return returnString;
}

function daysInFebruary (year){
	// February has 29 days in any year evenly divisible by four,
    // EXCEPT for centurial years which are not also divisible by 400.
    return (((year % 4 == 0) && ( (!(year % 100 == 0)) || (year % 400 == 0))) ? 29 : 28 );
}

function DaysArray(n) {
	for (var i = 1; i <= n; i++) {
		this[i] = 31
		if (i==4 || i==6 || i==9 || i==11) {this[i] = 30}
		if (i==2) {this[i] = 29}
   } 
   return this
}

function isDate(obj){
	var dtStr = $(obj).val()
	if(!dtStr) return true;
	var daysInMonth = DaysArray(12)
	var pos1=dtStr.indexOf(dtCh)
	var pos2=dtStr.indexOf(dtCh,pos1+1)
	var strDay=dtStr.substring(0,pos1)
	var strMonth=dtStr.substring(pos1+1,pos2)
	var strYear=dtStr.substring(pos2+1)
	strYr=strYear
	if (strDay.charAt(0)=="0" && strDay.length>1) strDay=strDay.substring(1)
	if (strMonth.charAt(0)=="0" && strMonth.length>1) strMonth=strMonth.substring(1)
	for (var i = 1; i <= 3; i++) {
		if (strYr.charAt(0)=="0" && strYr.length>1) strYr=strYr.substring(1)
	}
	month=parseInt(strMonth)
	day=parseInt(strDay)
	year=parseInt(strYr)
	if (pos1==-1 || pos2==-1){
		alert("The date format should be : dd/mm/yyyy");
		$(obj).val("");
		return false
	}
	if (strMonth.length<1 || month<1 || month>12){
		alert("Please enter a valid month");
		$(obj).val("");
		return false
	}
	if (strDay.length<1 || day<1 || day>31 || (month==2 && day>daysInFebruary(year)) || day > daysInMonth[month]){
		alert("Please enter a valid day");
		$(obj).val("");
		return false
	}
	if (strYear.length != 4 || year==0 || year<minYear || year>maxYear){
		alert("Please enter a valid 4 digit year between "+minYear+" and "+maxYear);
		$(obj).val("");
		return false
	}
	if (dtStr.indexOf(dtCh,pos2+1)!=-1 || isInteger(stripCharsInBag(dtStr, dtCh))==false){
		alert("Please enter a valid date");
		$(obj).val("");
		return false
	}
	return true
}

var current_focus = 0;

function fokus_out(txt){
	current_focus += 1;
	if(current_focus > 1){
		return;
	}
	
	if(isNaN(Number(txt.value))){
		txt.value = "";
		return;
	}
		
	txt.value = titik(txt.value);
}


function roundVal(val){
	var dec =2;
	var result = Math.round(val*Math.pow(10,dec))/Math.pow(10,dec);
	return result;
}

function fokus(txt){
	current_focus = 0;
	
	val = txt.value;
	
	if(!val){
		return;
	}
	txt.value = hilangTitik(val);
}

function titik(angka){
	
	if(!angka) return "";
	angka = angka.toString();
	if(parseInt(angka)==angka){
		angka = parseInt(angka);
		angka = angka.toString();
	}
	
	angka = angka.replace(/[.]/g,",");
	
	min = false;
	if(angka<0){
		min = true;
		angka = angka.substring(1);
	}
	var p =0;
	var newAngka = new Array();
	
	var a = 0;
	for(var t=angka.length-1;t>-1;t--){
		p++;
		
		if(angka[t]==","){
			p=0;
		}
		if(p==3){
			newAngka[a] = angka[t];
			a++;
			newAngka[a] = ".";
			a++;
			p=0;
			
			continue;
		}
		newAngka[a] = angka[t];
		a++
	}
	
	var re ="";
	var koma = false;
	for(var e=newAngka.length-1;e>-1 ;e--){
		
		if(newAngka[e]==","){
			koma = true;
		}
		if(koma && newAngka[e]=="."){
			continue;
		}
		re += newAngka[e];
	}
	
	if(re[0]=="."){
		re = re.substring(1);
	}
	
	if(min){
		re = "-"+re;
	}
	re = re==0?"":re;
	return re;
	
}

function hilangTitik(val){
	var re = val;
	re = re.replace(/[.]/g,"");
	re = re.replace(/[,]/g,".");
	return roundVal(re);
}



function sendFile(file) {
	
	var foto = $(file).parent().parent().parent();
	var loading = $(foto).children(".loading")[0];
	$(loading).show();
	var progressbar = $(loading).children(".progressbar")[0];
	var cancel = $(loading).children(".cancel")[0];
	$(cancel).show();
	var preview = $(foto).children(".preview")[0];
	var img = $(preview).find("img")[0];
	var del = $(preview).children(".close")[0];
	var fileUpload = $(file).parent(); 
	var foto_name = $(foto).children(".foto_name")[0];
	var id = $($(foto).children(".id")[0]).val();
	
	$(fileUpload).hide();
	
	
	var data = new FormData();
	data.append("file", file.files[0]);
	
	
	$.ajax({
	type: 'post',
	url: image_url+"upload/",
	data: data,
	success: function (data) {
		$(file).replaceWith( file = $(file).clone( true ));
		//console.log(data);
		
		if(data.error){
			notif(data.error);
			return;
		}
		
		$(img).attr("src",data.url);
		$(img).on("load",function(){
			$(foto_name).val(data.foto_name);
			$(loading).hide();
			$(preview).show();
			$(del).show();
		});
	},
	xhr: function(){
		
		var xhr = new window.XMLHttpRequest();
		
        // saat tombol x ditekan untuk cancel
		$(cancel).on("click",function(){
			xhr.abort();
			$(loading).hide();
			$(fileUpload).show();
			$(file).replaceWith( file = $(file).clone( true ) );
		});
        xhr.upload.onprogress = function(evt){
			progress = Math.ceil(evt.loaded/evt.total*100);
			console.log('progress', progress);
			$(progressbar).progressbar({value: progress});
		};
        xhr.upload.onload = function(){ 
			$(progressbar).progressbar({value: false}); 
			$(cancel).hide();
		};
        return xhr;
    } ,
	processData: false,
	contentType: false,
	});
}

function remove_file(obj){
	notif("Foto ini akan dihapus?",function(){
		var foto = $(obj).parent().parent();
		var fileUpload = $(foto).find(".fileUpload")[0];
		var preview = $(foto).children(".preview")[0];
		var foto_name = $(foto).children(".foto_name")[0];
		
		var id = $($(foto).children(".id")[0]).val();
		var img = $(foto).find("img")[0];
		
		file_name = $(foto_name).val();
		$(foto_name).val("");
		$(obj).hide();
		$(fileUpload).show();
		
		$(img).off("load");
		$(img).attr("src","/static/images/broken.png");
		$.post(image_url+"delete/",{remove:1,foto_name:file_name});
		
		
		closeNotif();
	},true);
	
}
