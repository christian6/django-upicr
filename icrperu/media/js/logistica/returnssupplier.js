$(document).ready(function () {
	$("#feci,#fecf").datepicker({ changeMonth: true, changeYear: true, showAnim: 'slide', dateFormat : 'yy-mm-dd'});
	$("input[name=rbtn]").change(function () {
		changeSearch();
	});
	$("#btnch").click(function () {
		checkedDet();
	});
	$("#btnb").click(function () {
		moveContainer(1);
	});
	$(".opensaved").click(function () {
		$("#mod").modal("show");
		requestMaterials();
	});
});
var changeSearch = function () {
	$("input[name=rbtn]").each(function () {
		var item = this;
		if (item.checked) {
			if (item.value == 'n') {
				$("#nro").attr('disabled',false);
				$("#feci,#fecf").attr('disabled',true);
			}else if(item.value == 'f'){
				$("#nro").attr('disabled',true);
				$("#feci,#fecf").attr('disabled',false);
			};
		};
	});
}
var moveContainer = function (number) {
	$("#container"+number).ScrollTo({
		duration : 1000,
		easing : 'linear'
	});
}
var al='',oc='';
var detailNoteEntry = function (nro,a,o) {
	if (nro != '') {
		$.ajax({
			url : '/ws/logistica/list/note/entry/',
			type : 'GET',
			data : { 'nro' : nro },
			dataType : 'json',
			success : function (response) {
				//console.log(response);
				if (response.status == 'success') {
					$(".nni").html(nro);
					constructTable(response);
					al = a;
					oc = o;
				};
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	};
}
var constructTable = function (json) {
	if (json.list.length > 0) {
		var bdet = document.getElementById("tbd");
		bdet.innerHTML = '';
		for (var i = 0; i < json.list.length; i++) {
			var tr = document.createElement('tr'),
					td = document.createElement('td'),id=document.createElement('td'),de=document.createElement('td'),me=document.createElement('td'),
					un=document.createElement('td'),cn=document.createElement('td'),ch=document.createElement('td'),inp=document.createElement('input');
			td.innerHTML = (i+1);
			td.setAttribute('class','text-center');
			tr.appendChild(td);
			id.innerHTML = json.list[i].materialesid;
			id.setAttribute('class','text-center');
			tr.appendChild(id);
			de.innerHTML = json.list[i].matnom;
			de.setAttribute('class','');
			tr.appendChild(de);
			me.innerHTML = json.list[i].matmed;
			me.setAttribute('class','');
			tr.appendChild(me);
			un.innerHTML = json.list[i].matund;
			un.setAttribute('class','text-center');
			tr.appendChild(un);
			cn.innerHTML = json.list[i].cantidad;
			cn.setAttribute('class','text-center');
			tr.appendChild(cn);
			inp.setAttribute('type','checkBox');
			inp.setAttribute('value',json.list[i].materialesid);
			inp.setAttribute('checked',true);
			inp.setAttribute('name','chkfirst');
			ch.appendChild(inp);
			ch.setAttribute('class','text-center');
			tr.appendChild(ch);
			bdet.appendChild(tr);
		};
		moveContainer(2);
	};
}
var statusCheck = false;
var checkedDet = function () {
	$("input[name=chkfirst]").each(function () {
		var item = this;
		item.checked = statusCheck;
	});
	if (statusCheck) {
		$("#btnch .glyphicon").removeClass('glyphicon-check').addClass('glyphicon-unchecked');
		$("#btnch .btn-text").html('Limpiar');
		statusCheck = false;
	}else{		
		$("#btnch .glyphicon").removeClass('glyphicon-unchecked').addClass('glyphicon-check');
		$("#btnch .btn-text").html('Seleccionar');
		statusCheck = true;
	};
}
var saved = function () {
	$("#mod").modal('hide');
	if (validCheckDet()) {
		$.msgBox({
			title : 'Confirmar?',
			content : 'Realmente desea guardar la Devolución a Proveedor?',
			type : 'confirm',
			buttons : [{value:'Si'},{value:'No'}],
			success : function (response) {
				if (response == 'Si') {
					var det = Array(),mat = Array();
					$("input[name=cants]").each(function () {
						var item = this;
						mat.push({'mid':item.id,'cant':item.value});
					});
					det['list'] = mat;
					//console.log(JSON.parse(JSON.stringify(det['list'])));
					var mon = 0;
					if ($("#mon").val() == '') { mon = 0 };
					var prm = {
						'nni' : $('.nni').html(), // codigo nota de ingreso
						'aid' : al, // codigo almacen
						'noc' : oc, // Nro Orden de compra
						'nnc' : $("#nnc").val(), // nro nota de credito
						'mon' : mon, // nro nota de credito
						'obs' : $("#obs").val(), // observacaion
						'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
						'list' : JSON.stringify(det['list']) // materiales
					}
					$.ajax({
						url : '/ws/logistica/saved/returns/supplier/nc/',
						type : 'GET',
						data : prm,
						dataType : 'json',
						success : function (res) {
							if (res.status == 'success') {
								msgInfo(null,null,null);
							};
						},
						error : function (obj,que,otr) {
							msgError(null,null,null);
						}
					});
				};
			}
		});
	}else{
		msgWarning(null,'No se a seleccionado ningún material!',true);
	};
}
var validCheckDet = function  () {
	var count = 0;
	$("input[name=chkfirst]").each(function () {
		var item = this;
		if (item.checked) {
			count++;
		};
	});
	if (count > 0) {
		return true;
	}else{
		return false;
	};
};
var continus = function () {
	$('#mod').modal('hide');
	var count = 0;
	$("input[type=]")
	if (validCheckDet()) {
		$('#mdet').modal('show');	
	}else{
		msgWarning(null,'No han seleccionado materiales!',true);
	};
}
var blacks = function () {
	$('#mdet').modal('hide');
	$('#mod').modal('show');
}
var requestMaterials = function () {
	var cadm = "";
	$("input[name=chkfirst]").each(function () {
		var item = this;
		if (item.checked) {
			cadm += "'"+item.value+"',";
		};
	});
	cadm = cadm.substring(0,(cadm.length - 1));
	console.log(cadm.length);
	if (cadm.length >= 17) {
		$.ajax({
			url : '/ws/logistica/list/selected/note/returns/',
			type : 'GET',
			data : { 'nro' : $('.nni').html(), 'cad' : cadm },
			dataType : 'json',
			success : function (response) {
				if (response.status == 'success') {
					var dbc = document.getElementById('tcan');
					dbc.innerHTML = '';
					if (response.list.length > 0) {
						for (var i = 0; i < response.list.length; i++) {
							var tr = document.createElement('tr'),
									td = document.createElement('td'),id=document.createElement('td'),de=document.createElement('td'),me=document.createElement('td'),
									un=document.createElement('td'),cn=document.createElement('td'),ch=document.createElement('td'),inp=document.createElement('input');
							td.innerHTML = (i+1);
							td.setAttribute('class','text-center');
							tr.appendChild(td);
							id.innerHTML = response.list[i].materialesid;
							id.setAttribute('class','text-center');
							tr.appendChild(id);
							de.innerHTML = response.list[i].matnom;
							de.setAttribute('class','');
							tr.appendChild(de);
							me.innerHTML = response.list[i].matmed;
							me.setAttribute('class','');
							tr.appendChild(me);
							un.innerHTML = response.list[i].matund;
							un.setAttribute('class','text-center');
							tr.appendChild(un);
							//cn.innerHTML = response.list[i].cantidad;
							cn.setAttribute('class','text-center');
							//tr.appendChild(cn);
							inp.setAttribute('type','number');
							inp.setAttribute('value',response.list[i].cantidad);
							inp.setAttribute('min',0);
							inp.setAttribute('max',response.list[i].cantidad);
							inp.setAttribute('id',response.list[i].materialesid);
							inp.setAttribute('class', 'form-control input-xs col-md-2');
							inp.setAttribute('name','cants');
							cn.appendChild(inp);
							//ch.setAttribute('class','text-center');
							tr.appendChild(cn);
							dbc.appendChild(tr);
						};
					};
				};
			}
		});
	}else{
		msgWarning('Alerta!','El codigo de material no es correcto',true);
	};
}