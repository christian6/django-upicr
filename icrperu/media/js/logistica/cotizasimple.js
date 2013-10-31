function searchmeter (e) {
	var txtse = document.getElementById("nommat");
	var evt = e ? e : event;
	var key = window.Event ? evt.which : evt.keyCode;
	if (key == 13) {
		search(txtse.value);
	};
}
function search (val) {
//	console.log(val);
	$.ajax({
		url : '/ws/logistica/consulta/medida/material/',
		type : 'GET',
		data : { 'mat' : val },
		dataType : 'html',
		success : function (response) {
			//console.log(response);
			response = response.split('|');
			if (response[1] == 'success') {
				$("#med").html(response[0]);
			}else{
				msgError(null,'Hay un error al traer los detalle',true);
			}
		},
		error : function (obj,que,otr) {
			msgError(null,null,true);
		}
	});
}
function btnsearch () {
	search($("#nommat").val());
}
function brinddetailt () {
	var nom = $("#nommat").val();
	var med = $("#med").val();
	if (nom != '' && med != '') {
		$.ajax({
			url : '/ws/logistica/consulta/detalle/material/',
			type : 'GET',
			data : { 'mat':nom, 'med':med },
			success : function (response) {
				response = response.split('|');
				if (response[1] == 'success') {
					$("#tdet").html(response[0]);
				}else{
					msgError(null,'Se a producido un error al traer los datos.',true);
				}
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		})
	}else{
		msgError(null,'Nombre o medida se encuentran vacios.',true);
	}
}
function list_tmp_cotiza () {
	var dni = $("#dni").val();
	if (dni != '') {
		console.log(dni);
		$.ajax({
			url : '/ws/logistica/consulta/detalle/tmp/cotiza/',
			type : 'GET',
			data : { 'dni':dni },
			success : function (response) {
				//console.log(response);
				$("#dtbl").html(response);
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	}else{
		msgError(null,'No se ha podido realizar la consulta',true);
	}
}
function deletetmp () {
	$.msgBox({
		title : 'Comfirmar?',
		content : 'Realmente desea eliminar temporal de Cotización?',
		type : 'confirm',
		opacity : 0.8,
		buttons : [{value:'Si'},{value:'No'}],
		success : function (response) {
			if (response == 'Si') {
				var dni = $("#dni").val();
				if (dni != '') {
					$.ajax({
						url : '/ws/logistica/delete/tmp/cotiza/',
						type : 'GET',
						data : { 'dni':dni },
						success : function (response) {
							if (response == 'success') {
								location.href='';
							}else{
								msgError(null,'No se ha podido realizar la consulta',true);
							}
						},
						error : function (obj,que,otr) {
							msgError(null,null,null);
						}
					});
				}else{
					msgError(null,'No se ha podido realizar la consulta',true);
				}
			}
		}
	});
}
function addmatmtmp () {
	var mid = $("#matid").html();
	if (mid != '') {
		var cant =  $("#cant").val();
		if (cant != '') {
			var prm = {
				'mat':mid,
				'cant':cant,
				'dni':$("#dni").val()
			}
			$.ajax({
				url : '/ws/logistica/add/tmp/cotiza/',
				type : 'GET',
				data : prm,
				success : function (response) {
					if (response == 'success') {
						list_tmp_cotiza();
					}else{
						msgWarning(null,'No se ha podido agregar el material.',true);
					}
				},
				error : function (obj,que,otr) {
					msgError(null,null,null);
				}
			});
		}else{
			msgWarning(null,'No se a ingresado una cantidad.',true);
			return;
		}
	}else{
		msgError(null,'No se a encontrado al material.',true);
		return;
	}
}
function editmattmp (mat) {
	$.msgBox({
		title : 'Editar Cantidad',
		content : '<strong>Cantidad</strong><input style="width: 15em;" id="cante" class="form-control input-sm" type="number" min="1" max="9999">',
		opacity : 0.8,
		type : 'confirm',
		buttons : [{value:'Editar'},{value:'Cancelar'}],
		success : function (response) {
			if (response == 'Editar') {
				var prm = {
					'cant' : $("#cante").val(),
					'dni' : $("#dni").val(),
					'mat' : mat
				}
				$.ajax({
					url : '/ws/logistica/edit/mat/tmp/cotiza/',
					type : 'GET',
					data : prm,
					success : function (response) {
						console.log(response);
						if (response == 'success') {
							list_tmp_cotiza();
						}else{
							msgError(null,'Al parecer hay un error de transacción',true);
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
function delmattmp (mat) {
	$.msgBox({
		title : 'Eliminar material',
		content : 'Realmente desea Elimnar?',
		type : 'confirm',
		buttons : [{value:'Si'},{value:'No'}],
		opacity : 0.8,
		success : function (response) {
			if (response == 'Si') {
				$.ajax({
					url : '/ws/logistica/delete/mat/tmp/cotiza/',
					type : 'GET',
					data : {'mat':mat,'dni':$("#dni").val()},
					success : function (response) {
						//console.log(response);
						if (response == 'success') {
							list_tmp_cotiza();
						}else{
							msgError(null,'Al parecer hay un error de transacción',true);
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
///////////////////////////////////////////////////////////////
$(document).ready(function () {
	$("#fec").datepicker({ minDate:"0", maxDate:"+6M", changeMonth:true, showAnim:'blind', dateFormat:"yy-mm-dd" });
	list_tmp_cotiza();
});
function showCotiza () {
	$("#mcot").modal("show");
}
function save_cotiza () {
	$("#mcot").modal("hide");
	$.msgBox({
		title : 'Generar Cotización',
		content : 'Seguro que desea generar Cotización',
		type : 'confirm',
		buttons : [{value:'Si'},{value:'No'}],
		opacity : 0.8,
		success : function (response) {
			if (response == 'Si'){
				var prm = {
					'dni' : $("#dni").val(),
					'fec' : $("#fec").val(),
					'obs' : $("#obs").val()
				}
				$.ajax({
					url : '/ws/logistica/save/cotiza/simple/',
					type : 'GET',
					data : prm,
					dataType : 'html',
					beforeSend : function (obj) {
						$(".full-screen").removeClass("hide");	
					},
					success : function (response) {
						if (response.length == 10) {
							traer_det();
							$("#ncot").html(response);
							$(".full-screen").addClass("hide");
							$("#mdet").modal('show');
						}else{
							msgError(null,'No se a podido realizar ls transacción.',true);
						}
					},
					error : function (obj,que,otr) {
						msgError(null,null,null);
					}
				});
			}else{
				$("#mcot").modal("show");
			}
		}
	});
}
function traer_det () {
	$.ajax({
		url : '/ws/logistica/lista/tmp/material/cotiza/',
		type : 'GET',
		data : { 'dni' : $("#dni").val() },
		dataType : 'html',
		success : function (response) {
			//console.log(response);
			$("#tbld").html(response);
		},
		error : function (ob,que,otr) {
			msgError(null,null,null);
		}
	});
}
function selectedchk () {
	$("[name=rmat]").each(function () {
		var item = this;
		if (item.checked) {
			var status = false;
			if (item.value == 'f') {
				status = true;
			}else if(item.value == 'c'){
				status = false;
			}
			//console.log(status);
			$("[name=mats]").each(function () {
				var chk = this;
				chk.checked = status;
			});
		}
	});
}
function generar_cotizacion_proveedor () {
	$("#mdet").modal('hide');
	$.msgBox({
		title : 'Confirmar',
		content : 'Realmente desea generar cotización para el proveedor?',
		type : 'confirm',
		opacity : 0.8,
		buttons : [{value:'Si'},{value:'No'}],
		success : function (response){
			if (response == 'Si') {
				var mats = "";
				$("[name=mats]").each(function () {
					var item = this;
					if (item.checked) {
						mats+= "'"+item.value+"',";
					}
				});
				mats = "("+mats.substring(0,(mats.length-1))+")";
				var prm = {
					'ruc' : $("#pro").val(),
					'mat' : mats,
					'nco' : $("#ncot").html(),
					'dni' : $("#dni").val()
				}
				$.ajax({
					url : '/ws/logistica/save/proveedor/cotizacion/simple/',
					type : 'GET',
					data : prm,
					dataType : 'html',
					success : function (response) {
						if (response == 'success') {
							$("#mdet").modal('show');
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
function finish_cotiza () {
	$("#mdet").modal('hide');
	$.msgBox({
		title : 'Finalizar Cotización',
		content : 'Desea terminar con la cotizaion?',
		type : 'confirm',
		opacity : 0.8,
		buttons : [{value:'Si'},{value:'No'}],
		success : function (response) {
			if (response == 'Si') {
				$.ajax({
					url : '/ws/logistica/finish/cotizacion/simple/',
					type : 'GET',
					data : { 'dni':$('#dni').val() },
					dataType : 'html',
					success : function (response) {
						if (response == 'success') {
							location.href='';
						}
					},
					error : function (obj,que,otr) {
						msgError(null,null,null);
					}
				});
			}else{
				$("#mdet").modal('show');
			}
		}
	});
}