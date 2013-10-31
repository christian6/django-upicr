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
		opacity : 0.8,
		success : function (response) {
			if (response == 'Si') {
				if (valid_form_cotizacion() == true) {
					listdetsuministro();
					savecotiza($("#nros").val());
					$("#mpro").modal('show');
				}else{
					return false;
				}	
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
function valid_form_cotizacion () {
	if ($("#fec").val() == '') {
		msgError(null,'No se ha ingresado fecha requerida',true);
		return false;
	}else if ($("#nros").val() == '') {
		msgError(null,'Esto parece ser grave, el número de suministro no existe.',true);
		return false;
	}else{
		return true;
	}
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
function savecotiza (nro) {
	var prm = {
		'nro' : nro,
		'dni' : $("#tdni").val(),
		'fec' : $("#fec").val(),
		'obs' : $("#obs").val()
	}
	$.ajax({
		data : prm,
		url : '/ws/logistica/save/cotizacion/',
		type : 'GET',
		dataType : 'html',
		beforeSend : function (obj) {
			$(".full-screen").removeClass('hide');
		},
		success : function  (response) {
			if (response == 'success') {
				$(".full-screen").addClass('hide');
				return true;
			}else{
				msgError(null,'Al parecer no se a podido guardar la Cotización.',false);
				$(".full-screen").addClass('hide');
				return false;
			}
		},
		error : function (obj,que,otr) {
			msgError(null,'Tienes un Error',false);
			$(".full-screen").addClass('hide');
			return false;
		}
	});
}
function finish () {
	$("#mpro").modal("hide");
	$.msgBox({
		title : 'Confirmar?',
		content : 'Ya has terminado de Cotizar a los Proveedores?',
		type : 'confirm',
		opacity : 0.8,
		buttons : [{value:'Si'},{value:'No'}],
		success : function (response) {
			if (response == 'Si') {
				// Cambiar de estado a la orden de suministro
				$.ajax({
					url : '/ws/logistica/finally/cotiza/suministro/',
					type : 'GET',
					data : { 'nro' : $("#nros").val()},
					dataType : 'html',
					success : function (response) {
						if (response == 'success') {
							location.href='';
						}else
							msgError(null,'Se ha producido un error al finalizar con la cotización',true);
					},
					error : function (obj,que,otr) {
						msgError(null,null,true);
					}
				});
			}
		}
	});
}
function generar_cotizacion_proveedor () {
	var mat = "";
	$('input:checkbox').each(function () {
		var item = this;
		if (item.checked) {
			mat += "'"+item.value+"',";
		}
	});
	mat = "("+mat.substring(0,(mat.length-1))+")";
	//alert(mat);
	var nro = $("#nros").val();
	var prm = {
		'nro' : nro,
		'ruc' : $("#pro").val(),
		'mat' : mat
	}
	$.ajax({
		data : prm,
		url : '/ws/logistica/save/cotizacion/proveedor/',
		type : 'GET',
		dataType : 'html',
		success : function (response) {
			if (response == 'success') {
				//document.getElementById().checked = true;
				$('#mpro').modal('hide');
				$.msgBox({
					title : 'Información',
					content : 'Se a guardado la cotización para el proveedor.',
					type : 'info',
					opacity : 0.8,
					autoClose : true
				});
				setTimeout(function() {
					$("#mpro").modal("show");
				}, 1800);
			}
		},
		error : function (obj,que,otr) {
			msgError(null,null,true);
		}
	});
}