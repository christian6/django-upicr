$(document).ready(function () {
	var prms = getVarsUrl();
	if (prms.list == 't') {
		$('#tabpro a[href="#list"]').tab('show') // Select tab by name
	}else{
		$('#tabpro a[href="#upkeep"]').tab('show') // Select tab by name
	}
});
function getVarsUrl(){
    var url= location.search.replace("?", "");
    var arrUrl = url.split("&");
    var urlObj={};
    for(var i=0; i<arrUrl.length; i++){
        var x= arrUrl[i].split("=");
        urlObj[x[0]]=x[1]
    }
    return urlObj;
}
function changePais () {
	$.ajax({
		url : '/ws/logistica/search/departamento/',
		type : 'GET',
		data : { 'pais' : $("#cbopa").val() },
		dataType : 'json',
		success : function (response) {
			if (response.status == 'success') {
				var dep = document.getElementById("cbodep");
				dep.innerHTML ='';
				for (var i = 0; i < response.ldet.length; i++) {
					var opt = document.createElement('option');
					opt.text = response.ldet[i].deparnom;
					opt.value = response.ldet[i].departamentoid;
					try
					{
					  // for IE earlier than version 8
					  dep.appendChild(opt);
					}
					catch (e)
					{
						dep.appendChild(opt);
					}
				}
			}
		},
		error : function (obj,que,otr) {
			msgError(null,null,null);
		}
	});
}
function changeDepartamento () {
	$.ajax({
		url : '/ws/logistica/search/provincia/',
		type : 'GET',
		data : { 'pais' : $("#cbopa").val(), 'dep' : $("#cbodep").val() },
		dataType : 'json',
		success : function (response) {
			if (response.status == 'success') {
				var pro = document.getElementById("cbopro");
				pro.innerHTML ='';
				for (var i = 0; i < response.ldet.length; i++) {
					var opt = document.createElement('option');
					opt.text = response.ldet[i].provnom;
					opt.value = response.ldet[i].provinciaid;
					try
					{
					  // for IE earlier than version 8
					  //pro.add(opt,pro.options[null]);
					  pro.appendChild(opt);
					}
					catch (e)
					{
						pro.appendChild(opt);
						//pro.appendChild(opt,null);
					}
				}
			}
		},
		error : function (obj,que,otr) {
			msgError(null,null,null);
		}
	});
}
function changeProvincia () {
	$.ajax({
		url : '/ws/logistica/search/distrito/',
		type : 'GET',
		data : { 'pais' : $("#cbopa").val(), 'dep' : $("#cbodep").val(), 'pro' : $("#cbopro").val() },
		dataType : 'json',
		success : function (response) {
			if (response.status == 'success') {
				var dist = document.getElementById("cbodist");
				dist.innerHTML ='';
				for (var i = 0; i < response.ldet.length; i++) {
					var opt = document.createElement('option');
					opt.text = response.ldet[i].distnom;
					opt.value = response.ldet[i].distritoid;
					try
					{
					  // for IE earlier than version 8
					  //dist.add(opt,dist.options[null]);
					  dist.appendChild(opt);
					}
					catch (e)
					{
						dist.appendChild(opt);
						//dist.appendChild(opt,null);
					}
				}
			}
		},
		error : function (obj,que,otr) {
			msgError(null,null,null);
		}
	});
}
function cleaninput () {
	$("input").each(function () {
		var item = this;
		item.value = '';
	});
}
function singleNumber (e) {
	var charCode = (e.which) ? e.which : event.keyCode;
	if( charCode > 31 && (charCode < 48 || charCode > 57) )
		return false;
	else
		return true;

}
function editpro (ruc,rs,dir,pa,de,pr,di,ti,te,or,ml) {
	$("#ruc").val(ruc);
	$("#rz").val(rs);
	$("#dir").val(dir);
	$("#tel").val(te);
	$("#mail").val(ml);
	triggerChange('cboori',or);
	triggerChange('cbopa',pa);
	setTimeout(function() {
		triggerChange('cbodep',de);
	}, 2500);
	setTimeout(function() {
		triggerChange('cbopro',pr);
	}, 5000);
	setTimeout(function() {
		triggerChange('cbodist',di);
	}, 7500);
	$('#tabpro a[href="#upkeep"]').tab('show') // Select tab by name
}
function delpro (ruc,rs) {
	$.msgBox({
		title : 'Eliminar Proveedor!',
		content : 'Realmente desea eliminar al Proveedor '+rs,
		type : 'confirm',
		opacity : 0.8,
		buttons : [{value:'Si'},{value:'No'}],
		success : function (response) {
			if (response == 'Si') {
				$.ajax({
					url : '/ws/logistica/delete/supplier/',
					type : 'GET',
					data : { 'ruc' : ruc },
					dataType : 'json',
					success : function (response) {
						console.log(response);
						if (response.status == 'success') {
							location.href='?list=t';
						}
					},
					error : function (obj,que,otr) {
						msgError(null,null,null);
					}
				});
			}
		}
	});
}
function triggerChange (select,val) {
	var obj = document.getElementById(select);
	var A= obj.options, L= A.length;
	if (L > 0) {
		for (var i = 0; i < L; i++) {
			if (A[i].value == val) {
				obj.selectedIndex = i;
				$("#"+select).trigger('change');
				i = L;
				return true;
			}
		}
	}else{
		console.log(select+'  '+val);
		setTimeout(function() {
			triggerChange(select,val);	
		}, 2000);
		
	}
}
function save () {
	if (validSave()) {
		var prm = {
			'ruc' : $("#ruc").val(),
			'rs' : $("#rz").val(),
			'dir' : $("#dir").val(),
			'tel' : $("#tel").val(),
			'pais' : $("#cbopa").val(),
			'dep' : $("#cbodep").val(),
			'pro' : $("#cbopro").val(),
			'dist' : $("#cbodist").val(),
			'tipo' : $("#cbotipo").val(),
			'ori' : $("#cboori").val(),
			'mail' : $("#mail").val()
		}
		$.ajax({
			url : '/ws/logistica/save/supplier/',
			type : 'GET',
			data : prm,
			dataType : 'json',
			success : function (response) {
				//console.log(response);
				if (response.status == 'success') {
					location.href='?list=t';
				}
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		})
	}
}
function validSave () {
	var sts = false;
	$("input").each(function () {
		var item = this;
		if (item.value == ''){
			item.focus();
			item.placeholder = 'Este campo esta vacio';
			sts = false;
			return false;
		}else{
			sts = true;
		}
		console.log(item.id);
		if (item.id == 'ruc' && item.value.length < 11) {
			alert('El RUC ingresado no es correcto!');
			sts = false;
			return false;
		}
	});
	return sts;
}