$(document).ready(function () {
	showCab();
	$("input[name=fecha]").datepicker({ minDate: "+1D" , maxDate: "+4M" , changeMonth: true, changeYear: true, showAnim: "slide", dateFormat: "yy-mm-dd"});
	$("#fent,#fval").datepicker({ minDate: "0", changeMonth: true, changeYear: true, showAnim: 'slide', dateFormat : 'yy-mm-dd' });
	readytotal();
	tooldocument();
});
function calmodp (obj) {
	if (obj.id != "") {
		var id = obj.id.substring(3);
		var cant = $("#c"+id).html();
		//console.log(cant +" * "+obj.value);
		$("#imp"+id).val((parseFloat(cant) * parseFloat(obj.value)).toFixed(2) );
	}
	importtotal();
}
function readytotal () {
	var imp = document.getElementsByName('import');
	var tot = 0;
	for (var i = 0; i < imp.length; i++) {
		var id = imp[i].id.substring(3);
		var pre = $("#pre"+id).val();
		if (pre != "") {
			var cant = parseFloat($("#c"+id).html());
			var im = ( parseFloat(pre) * cant );
			$("#"+imp[i].id).val(im);
			tot += im;
		}
	}
	var imp = 0.18;
	var igv = 0,total=0;
	igv = (tot * imp);
	total = ( tot + igv);
	$("#tot").html('$ '+tot.toFixed(2));
	$("#igv").html('$ '+igv.toFixed(2));
	$("#total").html('$ '+total.toFixed(2));
}
function importtotal () {
	var count = document.getElementsByName('import');
	var tot = 0;
	for (var i = 0; i < count.length; i++) {
		//console.log(count[i].id)
		if (count[i].value != ''){
			tot += parseFloat(count[i].value);
		}
	}
	var imp = 0.18;
	var igv = 0,total=0;
	igv = (tot * imp);
	total = ( tot + igv);
	$("#tot").html('$ '+tot.toFixed(2));
	$("#igv").html('$ '+igv.toFixed(2));
	$("#total").html('$ '+total.toFixed(2));
}
function showhojatec (id) {
	$("#"+id).click();
}
function updatePrice (obj) {
	if (obj.value != '') {
		var mat = obj.id.substring(3);
		var token = $("input[name=csrfmiddlewaretoken]").val();
		var prm = {
				'csrfmiddlewaretoken' : token,
				nro : $("#nro").val(),
				mat : mat,
				pre : parseFloat(obj.value)
			}
		$.ajax({
			url : '/ws/proveedor/update/price/quote/',
			type : 'POST',
			data : prm,
			success : function (response) {
				var json = JSON.parse(response);
				if (json.status != 'success') {
					msgError('Error','No se pudo escribir el precio.',true);
				}
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	}
}
function updateFecha (fec) {
	if (fec.value != "") {
		var mat = fec.id.substring(1);
		var token = $("input[name=csrfmiddlewaretoken]").val();
		var prm = {
				'csrfmiddlewaretoken' : token,
				nro : $("#nro").val(),
				mat : mat,
				fec : fec.value
			}
		$.ajax({
			url : '/ws/proveedor/update/date/quote/',
			type : 'POST',
			data : prm,
			success : function (response) {
				var json = JSON.parse(response);
				if (json.status != 'success') {
					msgError('Error','No se pudo escribir el Fecha.',true);
				}
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	}
}
function updateMarca (obj) {
	if (obj.value != "") {
		var mat = obj.id.substring(1);
		var token = $("input[name=csrfmiddlewaretoken]").val();
		var prm = {
				'csrfmiddlewaretoken' : token,
				nro : $("#nro").val(),
				mat : mat,
				mar : obj.value
			}
		$.ajax({
			url : '/ws/proveedor/update/mark/quote/',
			type : 'POST',
			data : prm,
			success : function (response) {
				var json = JSON.parse(response);
				if (json.status != 'success') {
					msgError('Error','No se pudo escribir el Fecha.',true);
				}
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	}
}
function filetecnicoup (obj) {
	if (obj.id != '') {
		var inputfile = document.getElementById(obj.id);
		var file = inputfile.files[0];
		if (file != null) {
			var prm = new FormData();
			var token = $("input[name=csrfmiddlewaretoken]").val();
			prm.append('arch',file);
			prm.append('nro',$("#nro").val());
			prm.append('mat', obj.id.substring(1));
			prm.append('csrfmiddlewaretoken', token);
			$.ajax({
				url : '/ws/proveedor/upload/file/quote/',
				type : 'POST',
				data : prm,
				contentType : false,
				processData : false,
				cache : false,
				success : function (response) {
					//console.log(response);
					var json = JSON.parse(response);
					if (json.status != 'success') {
						msgError('Error','No se pudo subir hoja técnica.',true);
					}
				},
				error : function (obj,que,otr) {
					msgError(null,null,null);
				}
			});
		}
	}
}
var cab = false;
function showCab () {
	if (cab) {
		$("#btncab").removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
		cab = false;
		$("#cab").show('blind', 1600);
	}else{
		$("#btncab").addClass('glyphicon-chevron-down').removeClass('glyphicon-chevron-up');
		cab = true;
		$("#cab").hide('blind', 1600);
	}
}
function tooldocument () {
	$("#tot").tooltip({
		title : 'Importe Total',
		placement : 'bottom',
		trigger : 'hover'
	});
	$("#btncab").tooltip({
		title : 'Cabecera de Cotización',
		placement : 'top',
		trigger : 'hover'
	});
	$("#tc a").tooltip({
		title : 'Cargar Hoja Técnica',
		placement : 'left',
		trigger : 'hover'
	});
	$("#btns").tooltip({
		title : 'Enviar Cotización a ICR PERU',
		placement : 'top',
		trigger : 'hover'
	});
	$("#upf").tooltip({
		title : 'Aquí puedes enviarnos algún documento adicional, no es necesario.',
		placement : 'top',
		trigger : 'hover'
	});
}
function savecotcliente () {
	var holder = ['Ingrese contanto', 'Fecha Entrega','Fecha Validez'];
	var i = 0;
	$("#con,#fent,#fval").each(function () {
		var item = this;
		if (item.value == '') {
			item.placeholder= holder[i];
			item.focus();
			return false;
		}
		i++;
	});
	if (i == 3) {
		var prm = new FormData();
		var token = $("input[name=csrfmiddlewaretoken]").val();
		var inputfile = document.getElementById("fop");
		var file = inputfile.files[0];
		var ext = "";
		if (file != null){
			prm.append('arch',file);
			ext = file['name'].split('.');
			ext = ext[(ext.length - 1)];
			prm.append('ext', ext);
		}else{
			prm.append('arch','nothing');
		}
		prm.append('con' , $("#con").val());
		prm.append('fen' , $("#fent").val());
		prm.append('fva' , $("#fval").val());
		prm.append('mon' , $("#mo").val());
		prm.append('nro' , $("#nro").val());
		prm.append('obs' , $("#obs").val());
		prm.append('csrfmiddlewaretoken', token);
		$.ajax({
			url : '/ws/proveedor/saved/cotizacion/customer/',
			type : 'POST',
			data : prm,
			contentType : false,
			processData : false,
			cache : false,
			success : function (response) {
				if (response.status == 'success') {
					msgInfo(null,null,null);
					setTimeout(function() {location.href='/proveedor/list/cotizaciones/';}, 1600);
				}else{
					msgWarning('Alerta!','Su cotización ya esta registrada en el sistema, espere nuestra respuesta, Gracias.',null);
				}
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	}
}
function showadj () {
	$('#fop').click();
}