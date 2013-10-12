$(document).ready(function () {
	$("#fec").datepicker({minDate:"0", maxDate:"+6M", changeMonth: true, changeYear: true, showAnim:"slide", dateFormat:"yy-mm-dd"});
});
function showfirst (nro) {
	if (nro!= '') {
		$("#nros").val(nro);
		$("#mcotiza").modal('show');
	}
}
function showlast () {
	$("#mcotiza").modal('hide');
	$.msgBox({
		title : 'Confirmar',
		content : 'Desea Generar Cotizacion con la orden de suministro Nro '+$("#nros").val(),
		type : 'confirm',
		buttons : [{value:'Si'},{value:'No'}],
		opacity : 0.5,
		success : function (response) {
			if (response == 'Si') {
				listdetsuministro();
				$("#mpro").modal('show');
			}
		}
	});
}
function listdetsuministro() {
	var nro = $("#nros").val();
	$.ajax({
		data : {'nro':nro},
		url : '/ws/logistica/list/det/suministro/',
		type : 'GET',
		dataType : 'html',
		success : function (response) {
			//alert(response);
			$("#dsum").html(response);
		},
		error : function (obj,que,otr) {
			msgError(null,null,true);
		}
	});
}
function selectedItem () {
	$('input:radio').each(function () {
		var item = this;
		if (item.checked) {
			var s = true;
			if (item.value == 'f') {
				s = true;
			}else if(item.value == 'c'){
				s = false;
			}
			console.log(s);
			$("[name='mat']").each(function () {
					var chk = this;
					chk.checked = s;
			});
		}
	});
}