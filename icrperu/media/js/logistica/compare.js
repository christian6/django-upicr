$(document).ready(function () {
		loaddata();
		$("#fec").datepicker({ minDate : "0", maxDate : "+6M", changeMonth : true, changeYear : true, showAnim: "slide", dateFormat : "yy-mm-dd" })
});
function loaddata () {
		var prm = {
			'nro' : $("#nro").val()
		}
		$.ajax({
			url : '/ws/logistica/compare/supplier/cotizacion/',
			type : 'GET',
			data : prm,
			dataType : 'html',
			success : function (response) {
				$("#det").html(response);
				typeMoneda();
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
}
function typeMoneda () {
	$("input[name=supplier]").each(function () {
		var item = this;
		$.ajax({
			url : '/ws/logistica/consulting/money/supplier/',
			type : 'GET',
			data : { 'nro' : $("#nro").val(), 'ruc' : item.value },
			dataType : 'json',
			success : function (response) {
				var obj = JSON.parse(response);
				if (obj.status == 'success') {
					$("#m"+item.value).html(obj.money);
				}else{
					$("#m"+item.value).html(obj.status);
				}
				importPrice();
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	});
}
function importPrice () {
	$("input[name=supplier]").each(function () {
		var ruc = this;
		var impruc = 0;
		$("input[name=mat]").each(function () {
			var mat = this;
			var cant = $("#c"+mat.value).html();
			var pre = $("#op"+ruc.value+mat.value).html();
			impruc += (parseFloat(cant) * parseFloat(pre));
		});	
		$("#t"+ruc.value).html(impruc.toFixed(2));
	});
}
function updatePrice (ruc) {
	var impruc = 0;
	$("input[name=mat]").each(function () {
		var mat = this;
		var cant = $("#c"+mat.value).html();
		var pre = $("#"+ruc+mat.value).val();
		impruc += (parseFloat(cant) * parseFloat(pre));
	});	
	$("#tm"+ruc).html(impruc.toFixed(2));
}
function selectCheck () {
	$("input[type=radio]").each(function () {
		var item = this;
		if (item.checked) {
			var val = false;
			if (item.value == 'f') val = true; else val = false;
			$("input[name=mat]").each(function () {
				var mat = this;
				mat.checked = val;
			});
		}
	});
}
function showCompra (ruc) {
	$.msgBox({
		title : 'Elegir Precio',
		content : 'Con que precio se va ha trabajar?',
		type : 'confirm',
		buttons : [{value:'Original'},{value:'Modificado'},{value:'Cancelar'}],
		opacity : 0.8,
		success : function (response) {
			if (response == 'Original') {
				showmodal(ruc,'op');
			}else if(response == 'Modificado'){
				showmodal(ruc,'');
			}
		}
	});
	
}
function showmodal (ruc,tp) {
	$("#toc").html('Realizar Orden Compra a '+$("#"+ruc).val());
	$("#cruc").html('RUC '+ruc);
	$("#rucc").val(ruc);
	showdetComp($("#nro").val(),ruc,tp);
	$("#mco").modal("show");
}
function showdetComp (nro,ruc,tp) {
	var mats = "";
	$("input[name=mat]").each(function (){
		var item = this;
		if (item.checked) {
			mats += "'" + item.value + "',";
		}
	});
	if (mats.length > 0) {
		$.ajax({
			url : '/ws/logistica/consulting/mat/buy/',
			type : 'GET',
			data : { 'mat' :  mats.substring(0,mats.length - 1), 'nro' : nro, 'ruc' : ruc },
			dataType : 'html',
			success : function (response) {
				var obj = JSON.parse(response);
				if (obj.status == 'success') {
					$("#cont").val(obj.contacto);
					$("#tm").html($("#m"+ruc).html());
					var tbody = document.getElementById("dcom");
					tbody.innerHTML = "";
					for (var i = 0; i < obj.mat.length; i++) {
						var tr = document.createElement("tr");
						var item = document.createElement("td");
						var id = document.createElement("td");
						var nom = document.createElement("td");
						var med = document.createElement("td");
						var und = document.createElement("td");
						var cant = document.createElement("td");
						var pre = document.createElement("td");
						var imp = document.createElement("td");

						id.setAttribute("name","ocmat");
						id.setAttribute("id","oc"+obj.mat[i].materialesid);

						cant.setAttribute("class","text-right");
						cant.setAttribute("id","coc"+obj.mat[i].materialesid);

						pre.setAttribute("class","text-right");
						pre.setAttribute("id","poc"+obj.mat[i].materialesid);

						imp.setAttribute("class","text-right");
						imp.setAttribute("id","ioc"+obj.mat[i].materialesid);

						item.innerHTML = i+1;
						id.innerHTML = obj.mat[i].materialesid;
						nom.innerHTML = obj.mat[i].matnom;
						med.innerHTML = obj.mat[i].matmed;
						und.innerHTML = obj.mat[i].matund;
						var c=0,p=0;
						c = parseFloat($("#c"+obj.mat[i].materialesid).html());
						if (tp != '') { p = parseFloat($("#"+tp+ruc+obj.mat[i].materialesid).html()); }else{ p = parseFloat($("#"+tp+ruc+obj.mat[i].materialesid).val());}
						cant.innerHTML = c;
						pre.innerHTML = p;
						imp.innerHTML = (c * p);

						tr.appendChild(item);
						tr.appendChild(id);
						tr.appendChild(nom);
						tr.appendChild(med);
						tr.appendChild(und);
						tr.appendChild(cant);
						tr.appendChild(pre);
						tr.appendChild(imp);
						tbody.appendChild(tr);
					}
				}
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	}
}
function cambioMoney () {
	var $mo = $("#mo option:selected");
	var tm = $("#tm").html();
	//if ($mo.text() != tm) {
		var tc = 0;
		$.ajax({
			url : '/ws/logistica/consulting/type/change/money/',
			type : 'GET',
			data : {},
			success : function (response) {
				if (response.status == 'success') {
					tc = response.tc[0].tcompra;

					if (tc != 0) {
						if ($mo.text() == 'DOLARES AMERICANOS') {
							changeD('D',tc);
						}else if($mo.text() == 'NUEVO SOLES'){
							changeD('S',tc);
						}
					}else{
	
					}
				}
			},
			error : function  (obj,que,otr) {
				msgError(null,null,null);
			}
		});

	//}else{
	//}
}
function changeD (money,tcc) {
	$("[name=ocmat]").each(function () {
		var item = this;
		var id = item.id.substring(2);
		var $c = $("#coc"+id);
		var $p = $("#poc"+id);
		var $imp = $("#ioc"+id);
		var pre = parseFloat($p.html());
		var cant  = parseFloat($c.html());
		if (money == 'D') {
			pre = (pre / tcc);
		}else if(money == 'S'){
			pre = (pre * tcc);
		}
		$p.html(pre.toFixed(2));
		$imp.html((cant * pre).toFixed(2));
	});
}
function saveOrderBuy () {
	if ($("#lug").val() == '') {
		$("#lug").focus();
		return false;
	}
	if ($("#fec").val() == '') {
		$("#fec").focus();
		return false;
	}
	$('#mco').modal('hide');
	$.msgBox({
		title : 'Generar Orden de Compra?',
		content : 'Desea generar Orden de Compra?',
		type : 'confirm',
		opacity : 0.8,
		buttons : [{value:'Si'},{value:'No'}],
		success : function (response) {
			if (response == 'Si') {

			}else if(response == 'No'){
				$("#mco").modal('show');
			}
		}
	});
}
function save() {
	var obj = new Object();
	$("[name=ocmat]").each(function () {
		var item = this;
		var mat = new Array();
		var id = item.id.substring(2);
		ar $c = $("#coc"+id);
		var $p = $("#poc"+id);
		var pre = parseFloat($p.html());
		var cant  = parseFloat($c.html());
		
	});
}