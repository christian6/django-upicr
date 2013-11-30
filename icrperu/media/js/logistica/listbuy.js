$(document).ready(function () {
	$("#fi,#ff").datepicker({ changeMonth : true, changeYear : true, showAnim : 'slide', dateFormat : 'yy-mm-dd' });
});
var changeRadio = function () {
	$("[name=rbtn]").each(function () {
		var item = this;
		if (item.checked) {
			if (item.value == 'n') {
				$("#nro").removeAttr('disabled');
				$("#fi,#ff").attr('disabled',true);
			}else if(item.value == 'f'){
				$("#fi,#ff").removeAttr('disabled',true);
				$("#nro").attr('disabled',true);
			}
		};
	});
}
var searchOrderBuy = function () {
	var obj = new Object();
	$("[name=rbtn]").each(function () {
		var item = this;
		if (item.checked) {
			if (item.value == 'n') {
				obj['tipo'] = 'nro';
				obj['nro'] = $("#nro").val();
			}else{
				if ($("#fi").val() != '' && $("#ff").val() == '') {
					obj['tipo'] = 'one';
					obj['fi'] = $("#fi").val();
				}else if($("#fi").val() != '' && $("#ff").val() != ''){
					obj['tipo'] = 'multi';
					obj['fi'] = $("#fi").val();
					obj['ff'] = $("#ff").val();
				}
			}
		}
	});
	if (obj != null) {
		$.ajax({
			url : '/ws/logistica/consulting/order/buy/',
			type : 'GET',
			data : obj,
			dataType : 'json',
			success : function (response) {
				console.log(response);
				if (response.status == 'success') {
					makingTable(response);
				}else{
					msgWarning(null,'Hay algún error con la consulta',null);
				}
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	}
}
var makingTable = function (json) {
	if (json != null) {
		var tb = document.getElementById('tbo');
		tb.innerHTML = '';
		for (var i = 0; i < json.lbuy.length; i++) {
			var tr = document.createElement('tr'),item = document.createElement('td'),nro = document.createElement('td'),rs = document.createElement('td'),
					doc = document.createElement('td'),mo = document.createElement('td'),tbt = document.createElement('td');
			var a = document.createElement('a'),ico = document.createElement('span');
			item.setAttribute('class','text-center');
			tbt.setAttribute('class','text-center');
			item.innerHTML = i+1;
			nro.innerHTML = json.lbuy[i].nrocompra;
			rs.innerHTML = json.lbuy[i].razonsocial;
			doc.innerHTML = json.lbuy[i].docnom;
			mo.innerHTML = json.lbuy[i].nomdes;
			ico.setAttribute('class','glyphicon glyphicon-export');
			a.setAttribute('class','tblack');
			a.appendChild(ico);
			tbt.appendChild(a);
			tr.appendChild(item);
			tr.appendChild(nro);
			tr.appendChild(rs);
			tr.appendChild(doc);
			tr.appendChild(mo);
			tr.appendChild(tbt);
			tb.appendChild(tr);
		};
	}
}