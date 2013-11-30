$(document).ready(function () {
	$("#fec").datepicker({ minDate : "0", maxDate : "+8M", changeMonth:true, changeYear:true, showAnim: 'slide',dateFormat:'yy-mm-dd'})
	list_tmp_compra();
});
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
function list_tmp_compra () {
	var dni = $("#dni").val();
	if (dni != '') {
		//console.log(dni);
		$.ajax({
			url : '/ws/logistica/list/tmp/compra/',
			type : 'GET',
			data : { 'dni':dni },
			success : function (response) {
				//console.log(response);
				if (response.status == 'success'){
					var tbody = document.getElementById("dtbl");
					tbody.innerHTML = '';
					for (var i = 0; i < response.list.length; i++) {
						var tr = document.createElement('tr'), id = document.createElement('td'),	nom = document.createElement('td'),
								med = document.createElement('td'),und = document.createElement('td'), cant = document.createElement('td'),
								pre = document.createElement('td'), edit = document.createElement('td'),del = document.createElement('td'),
								bed = document.createElement('button'),bde = document.createElement('button'),ied = document.createElement('span'),
								ide = document.createElement('span'),item = document.createElement('td');

						item.innerHTML = i+1;
						id.innerHTML = response.list[i].materialesid;
						nom.innerHTML = response.list[i].matnom;
						med.innerHTML = response.list[i].matmed;
						und.innerHTML = response.list[i].matund;
						cant.innerHTML = response.list[i].cantidad;
						pre.innerHTML = response.list[i].precio;

						id.setAttribute("id",response.list[i].materialesid);
						id.setAttribute("name","lmat");
						item.setAttribute('class','text-center');
						und.setAttribute('class','text-center');
						cant.setAttribute('class','text-center');
						cant.setAttribute('id','c'+response.list[i].materialesid);
						pre.setAttribute('class','text-center');
						pre.setAttribute('id','p'+response.list[i].materialesid);

						ied.setAttribute('class','glyphicon glyphicon-edit');
						ide.setAttribute('class','glyphicon glyphicon-remove');
						bed.setAttribute('class','btn btn-xs tblack');
						bde.setAttribute('class','btn btn-xs tblack');
						bed.setAttribute('onClick','editmattmp("'+response.list[i].materialesid+'",'+response.list[i].cantidad+','+response.list[i].precio+');');
						bde.setAttribute('onClick','delmattmp("'+response.list[i].materialesid+'");');
						bed.appendChild(ied);
						bde.appendChild(ide);

						edit.setAttribute('class', 'text-center');
						del.setAttribute('class', 'text-center');
						edit.appendChild(bed);
						del.appendChild(bde);

						tr.appendChild(item);tr.appendChild(id);tr.appendChild(nom);tr.appendChild(med);tr.appendChild(und);tr.appendChild(cant);tr.appendChild(pre);
						tr.appendChild(edit);tr.appendChild(del);
						tbody.appendChild(tr);
					};
					var tr = document.createElement("tr");
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
function deletetmp () {
	$.msgBox({
		title : 'Comfirmar?',
		content : 'Realmente desea eliminar temporal de Orden de Compra?',
		type : 'confirm',
		opacity : 0.8,
		buttons : [{value:'Si'},{value:'No'}],
		success : function (response) {
			if (response == 'Si') {
				var dni = $("#dni").val();
				if (dni != '') {
					$.ajax({
						url : '/ws/logistica/delete/tmp/det/buy/',
						type : 'GET',
						data : { 'dni':dni },
						success : function (response) {
							if (response.status == 'success') {
								list_tmp_compra();
							}else{
								msgWarning(null,'No se ha podido realizar la consulta',true);
							}
						},
						error : function (obj,que,otr) {
							msgError(null,null,null);
						}
					});
				}else{
					msgWarning(null,'No se ha podido realizar la consulta',true);
				}
			}
		}
	});
}
function addmatmtmp () {
	var mid = $("#matid").html();
	if (mid != '') {
		var cant =  $("#cant").val();
		var pre = $("#pre").val();
		if (cant != '' && pre != '') {
			var prm = {
				'mat':mid,
				'cant':cant,
				'pre' : parseFloat(pre),
				'dni':$("#dni").val()
			}
			//console.log(prm);
			$.ajax({
				url : '/ws/logistica/add/tmp/detils/buy/',
				type : 'GET',
				data : prm,
				success : function (response) {
					if (response.status == 'success') {
						list_tmp_compra();
					}else{
						msgWarning(null,'No hemos agregado el materiale, posiblemente ya se encuentre en tu lista.',true);
					}
				},
				error : function (obj,que,otr) {
					msgError(null,null,null);
				}
			});
		}else{
			msgWarning(null,'El campo cantidad o precio se encuentra vacio.',true);
			return;
		}
	}else{
		msgError(null,'No se a encontrado al material.',true);
		return;
	}
}
function editmattmp (mat,cant,pre) {
	$.msgBox({
		title : 'Editar Cantidad',
		content : '<span><em>Cantidad</em>'+
							'<input style="width : 10em;" id="cante" class="form-control input-xs" type="number" min="1" value="'+cant+'" max="9999"></span>'+
							'<span class="help-block"><em>Precio</em>'+
							'<input style="width : 10em;" id="pree" class="form-control input-xs" type="number" min="1" value="'+pre+'" max="9999"></span>',
		opacity : 0.8,
		type : 'confirm',
		buttons : [{value:'Editar'},{value:'Cancelar'}],
		success : function (response) {
			if (response == 'Editar') {
				var prm = {
					'cant' : $("#cante").val(),
					'pre' : $("#pree").val(),
					'dni' : $("#dni").val(),
					'mat' : mat
				}
				$.ajax({
					url : '/ws/logistica/edit/mat/tmp/buy/',
					type : 'GET',
					data : prm,
					success : function (response) {
						//console.log(response);
						if (response.status == 'success') {
							list_tmp_compra();
						}else{
							msgWarning(null,'Al parecer hay un error de transacción',true);
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
					url : '/ws/logistica/delete/mat/tmp/compra/',
					type : 'GET',
					data : {'mat':mat,'dni':$("#dni").val()},
					success : function (response) {
						//console.log(response);
						if (response.status == 'success') {
							list_tmp_compra();
						}else{
							msgWarning(null,'Al parecer hay un error de transacción',true);
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
function showCotiza () {
	$("#mbuy").modal("show");
}
function savedOrderbuy () {
	$("#mbuy").modal("hide");
	if ($("#lug").val() != '' && $("#fec").val()) {
		$.msgBox({
			title : 'Generar Orden de Compra',
			content : 'Seguro(a) que desea generar la Orden de Compra?',
			type : "confirm",
			opacity : 0.8,
			buttons : [{value:'Si'},{value:'No'}],
			success : function (response) {
				if (response == 'Si') {
					var obj = new Object();
					obj['mat'] = new Array();
					$("[name=lmat]").each(function () {
						var item = this;
						var	id = item.id,
								$c = $("#c"+id),
								$p = $("#p"+id),
								cant = parseFloat($c.html()),
								pre = parseFloat($p.html());
						obj.mat.push(new Array(id,cant,pre));
					});
					var prm = {
						'pro' : $("#pro").val(),
						'lug' : $("#lug").val(),
						'doc' : $("#doc").val(),
						'pag' : $("#pag").val(),
						'mo' : $("#mo").val(),
						'fec' : $("#fec").val(),
						'cont' : $("#cont").val(),
						'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
						'lmat' : JSON.stringify(obj)
					}
					$.ajax({
						url : '/ws/logistica/saved/order/buy/single/',
						type : 'POST',
						data : prm,
						success : function (response) {
							//console.log(response);
							if (response.status == 'success') {
								msgInfo("Orden de Compra","<em>Orden de Compra generada:<em><br>Nro : "+response.nro,false);
								list_tmp_compra();
							}
						},
						error : function (obj,que,otr) {
							msgError(null,null,null);
						}
					});
				}
			}
		});
	}else{
		msgWarning(null,'Algún campo se encuentra vacia.',null);
		setTimeout(function() { $("#mbuy").modal("show"); }, 1800);
	}
}
function showfileupload () {
	$("#mreadxls").modal('show');
}
function showopenupfile () {
	$("#upfile").click();
}
function uploadFileBuy () {
	var inputfile = document.getElementById("upfile");
	var file = inputfile.files[0];
	if (file != null) {
		var prm = new FormData();
		var token = $("input[name=csrfmiddlewaretoken]").val();
		prm.append('archivo',file);
		prm.append('csrfmiddlewaretoken', token);
		$.ajax({
			url : '/ws/logistica/upload/ready/buy/tmp/',
			type : 'POST',
			data : prm,
			contentType : false,
			processData : false,
			cache : false,
			beforeSend : function (obj) {
				$("#progressfile").removeClass('hide');
			},
			success : function (response) {
				//console.log(response);
				if (response.status == 'success') {
					$(".progress").removeClass('progress-striped');
					$(".progress-bar").removeClass('progress-bar-warning').addClass('progress-bar-success');
					$('#proinfo').html('Se ha terminado correctamente.');
					list_tmp_compra();
					setTimeout(function() { 
						$("#mreadxls").modal('hide');
						$("#proinfo").html('Espere por favor, estamos trabajando.');
						$(".progress").addClass('progress-striped');
						$(".progress-bar").removeClass('progress-bar-success').addClass('progress-bar-warning');
						$("#progressfile").addClass('hide');
						}, 600);
				}else if (response.status == 'fail') {
					msgError('Error','Archivo sin formato.',true);
				}
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	}else{
		$('#mreadxls').modal('hide');
		msgWarning(null,'No se a cargado ningún archivo, carge uno para continuar.',null);
		setTimeout(function() { $("#mreadxls").modal('show'); }, 2600);
	}
}