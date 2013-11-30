$(document).ready(function () {
	$("#tablo a[href='#list']").tab('show');
});
function generarPasswd (ruc,rs,ml) {
	if (ruc.length == 11) {
		$('#ruc').html(ruc);
		$("#rs").html(rs);
		$("#usrn").val(ruc);
		$("#passwd").val(ruc);
		$("#para").val(ml);
		$("#tablo a[href='#login']").tab('show');
	}
}
function vallogin () {
	var sts = false;
	$("#usrn,#passwd").each(function () {
		var item = this;
		console.log(item.id);
		if (item.value == '') {
			sts = false;
			return false;
		}else{
			sts = true;
		}
	});
	console.log(sts);
	return sts;
}
function saved () {
	if (vallogin()) {
		$.ajax({
			url : '/ws/logistica/saved/login/supplier/',
			type : 'GET',
			data : { 'ruc' : $("#ruc").html(),'passwd' : hex_md5($("#passwd").val()) },
			dataType : 'json',
			success : function (response) {
				console.log(response);
				if (response.status == 'success') {
					$("#asunto").val('Cambio de Password');
					$('#texto').val('Se a cambiado la clave para el ingrese al sitio web de ICR PERU, su nueva clave es:<br><br><strong>Clave de acceso : </strong> '+$("#passwd").val()+'<br><br>*** System ICR PERU ***');
					$("#mmail").modal('show');
				}
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	}else{
		msgInfo(null,'Algún campo se encuentra vacio.',null);
	}
}
function send () {
	dataMail($("#ruc").html());
}
function dataMail (ruc) {
	if( ruc.length == 11){
		var sts = false;
		$("input").each(function () {
			var item = this;
			if (item.value == '') {
				item.focus();
				item.placeholder = 'Campo Vacio';
				sts = false;
				return false;
			}else{
				sts = true
			}
		});
		if(sts){
			window.open('http://190.41.246.91:3000/?asunto='+$('#asunto').val()+'&para='+$('#para').val()+'&texto='+$('#texto').val(),'_blank');
		}
	}
}