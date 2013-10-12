$(function () {
	$("#fi,#ff").datepicker({ minDate: "-12M" , maxDate: "0" , changeMonth: true, changeYear: true, showAnim: "slide", dateFormat: "yy/mm/dd"});
});
function radiosearch (obj) {
	if (obj.checked) {
		if (obj.value == 'n') {
			document.getElementById("nros").disabled = false;
			document.getElementById("fi").disabled = true;
			document.getElementById("ff").disabled = true;
		}else if(obj.value == 'f'){
			document.getElementById("nros").disabled = true;
			document.getElementById("fi").disabled = false;
			document.getElementById("ff").disabled = false;
		}
	}
}
function listsuminstro () {
	/* valid list*/
	var $nros = $("#nros");
	var $fi = $("#fi");
	var $ff = $("#ff");
	var data = {}
	$(":radio").each(function () {
		var item = this;
		if (item.checked) {
			if (item.value == 'n') {
				if($nros.val()!=''){
					data = { 'type':'nro','nro':$nros.val() }
				}else{
					$.msgBox({
						title : 'Error',
						content : 'El campo nro se encuetran vacio.',
						type : 'warning',
						autoClose : true,
						opacity : 0.6
					});
					return;
				}
			}else if(item.value == 'f'){
				if ($fi.val() != '' && $ff.val() != '') {
					data = { 'type':'ff','fi':$fi.val(),'ff':$ff.val() }
				}else if($ff.val() == '' && $fi.val() != ''){
					data = { 'type':'fi','fi':$fi.val() }
				}else{
					$.msgBox({
						title : 'Error',
						content : 'Los campos de fecha se encuetran vacios.',
						type : 'info',
						autoClose : true,
						opacity : 0.6
					});
					return;
				}
			}
		}
	});
	//alert(data['type'] +' ');
	if( Object.keys(data).length > 0){
		$.ajax({
			data : data,
			url : '/ws/logistica/list/suministro/',
			type : 'GET',
			dataType : 'html',
			success : function (response) {
				response = response.split('|');
				if (response[1] == 'success') {
					$("#tbld").html(response[0]);
				}else{
					alert("error");
				}
			},
			error : function (obj,que,otr) {
				alert('tienes un error');
			}
		});
	}
}
function getdetail (nros) {
	$.ajax({
		data : {'nro':nros},
		url : '/ws/logistica/listdet/suministro/',
		type : 'GET',
		dataType : 'html',
		success : function (response) {
			//alert(response);
			$("#nro").html(nros);
			$("#dtbls").html(response);
			$("#mds").modal('show');
		},
		error : function (obj,que,otr) {
			msgError(null,null,true);
		}
	});
}
function aprobarSuministro () {
	var nro = $.trim($('#nro').html());
	$("#mds").modal('hide');
	$.msgBox({
		title : 'Confirmar',
		content : 'Realmente desea aprobar la orden de Suministro Nro '+nro,
		type : 'confirm',
		buttons : [{value:'Si'},{value:'No'}],
		opacity : 0.9,
		success : function (response) {
			if (response == 'Si') {
				var prm = { 'nro':nro }
				$.ajax({
					data : prm,
					url : '/ws/logistica/update/approved/suministro/',
					type : 'GET',
					dataType : 'html',
					beforeSend : function (obj) {
						$(".full-screen").removeClass("hide");
					},
					success : function (response) {
						//alert(response);
						listsuminstro();
						$(".full-screen").addClass("hide");
					},
					error : function (obj,que,otr) {
						msgError(null,null,null);
					}
				});
			}
		}
	});
}
function anularSuministro () {
	var nro = $.trim($('#nro').html());
	$("#mds").modal('hide');
	$.msgBox({
		title : 'Anular Suministro',
		content : 'Realmente desea anular la orden de Suministro Nro '+nro+'?',
		type : 'confirm',
		buttons : [{value:'Si'},{value:'No'}],
		opacity : 0.8,
		success : function (response) {
			if (response == 'Si') {
				var prm = { 'nro':nro }
				$.ajax({
					data : prm,
					url : '/ws/logistica/update/annulled/suministro/',
					type : 'GET',
					dataType : 'html',
					beforeSend : function (obj) {
						$(".full-screen").removeClass("hide");
					},
					success : function (response) {
						listsuminstro();
						$(".full-screen").addClass("hide");
					},
					error : function (obj,que,otr) {
						msgError(null,null,true);
					}
				});
			}
		}
	});
}
var obs = false;
function showobs () {
	if (obs) {
		$("#aobs").addClass("hide");
		obs = false;
	}else if(!obs){
		$("#aobs").removeClass("hide");
		obs = true;
	}
}