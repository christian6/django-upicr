$(document).ready(function () {
	$("#fi,#ff").datepicker({ dateMin: '', maxDate : '', changeMonth:true, changeYear:true, showAnim : 'slide', dateFormat : 'yy-mm-dd' });
});
function openCotizacion (ruc,nro) {
	window.open('http://190.41.246.91/web-cotiza/reports/pdfs/solcotpdf.php?ruc='+ruc+'&nro='+nro,'_blank');
}
function searchKeys () {
	var prm = {}
	$("input[name=rbtn]").each(function () {
		var item = this;
		if (item.checked) {
			if (item.value == 'n') {
				prm['type'] = 'nro';
				prm['nro'] = $("#nro").val();
			}else if(item.value == 'f'){
				if ($("#fi").val() != '' && $("#ff").val() == '') {
					prm['type'] = 'one';
					prm['fi'] = $("#fi").val();
				}else if($("#fi").val() != '' && $("#ff").val() != ''){
					prm['type'] = 'plus';
					prm['fi'] = $("#fi").val();
					prm['ff'] = $("#ff").val();
				}
			}
		}
	});
	if (prm != null) {
		$.ajax({
			url : '/ws/logistica/search/key/cotizacion/',
			type : 'GET',
			data : prm,
			dataType : 'json',
			success : function (response) {
				if (response.status == 'success') {
					$("#tb").html('');
					for (var i = 0; i < response.list.length; i++) {
						var tr = document.createElement("tr");
						var item = document.createElement("td"),
							nro = document.createElement("td"),
							ruc = document.createElement("td"),
							rs = document.createElement("td"),
							key = document.createElement("td"),
							fec = document.createElement("td"),
							vw = document.createElement("td"),
							bvw = document.createElement("button"),
							ico = document.createElement("span"),
							bma = document.createElement("button"),
							so = document.createElement("span");

						ico.setAttribute("class","glyphicon glyphicon-eye-open");
						bvw.appendChild(ico);
						bvw.setAttribute("class","btn btn-xs btn-info tblack");
						bvw.setAttribute("onClick","openCotizacion('"+response.list[i].rucproveedor+"','"+response.list[i].nrocotizacion+"');");

						ico.setAttribute("class","glyphicon glyphicon-envelope");
						bvw.appendChild(ico);
						bvw.setAttribute("class","btn btn-xs btn-warning tblack");
						bvw.setAttribute("onClick","confirmMsg('"+response.list[i].nrocotizacion+"','"+response.list[i].razonsocial+"','"+response.list[i].keygen+"');");
						

						item.innerHTML = i+1;
						nro.innerHTML = response.list[i].nrocotizacion;
						ruc.innerHTML = response.list[i].rucproveedor;
						rs.innerHTML = response.list[i].razonsocial;
						key.innerHTML = response.list[i].keygen;
						fec.innerHTML = response.list[i].fecha;
						vw.appendChild(bvw);

						tr.appendChild(item);
						tr.appendChild(nro);
						tr.appendChild(ruc);
						tr.appendChild(rs);
						tr.appendChild(key);
						tr.appendChild(fec);
						tr.appendChild(vw);
						document.getElementById("tb").appendChild(tr);
					}
				}
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	}
}
function changeradio () {
	var sts = false;
	$("input[name=rbtn]").each(function () {
		var item = this;
		if (item.checked) {
			if (item.value == 'n') {
				$("#fi,#ff").attr("disabled",true);
				$("#nro").removeAttr('disabled');
			}else if(item.value == 'f'){
				$("#fi,#ff").removeAttr('disabled');
				$("#nro").attr('disabled',true);
			}
		};
	});
}
function confirmMsg (nro,rs,key) {
	if (nro != '' && rs != '' && key != '') {
		$("#rs").html(rs);
		$("#asunto").val('AutoKey para cotización '+nro);
		$("#texto").val('AutoKey para la cotización Nro <b>'+nro+'</b><br><br> <strong>AutoKey : </strong> '+key+
						'<br><br>Presione <a href="http://190.41.246.91:8000/proveedor/">aquí</a> para ir al sitio web.<br><br><strong> *** Logistica ICR PERU S.A. ***</strong>');
		$.msgBox({
			title : 'Enviar Mensaje',
			content : 'Quieres modificar el mensaje al proveedor?',
			type : 'confirm',
			opacity : 0.8,
			buttons : [{value:'Si'},{value:'No'},{value : 'Enviar'}],
			success : function  (response) {
				if (response == 'Si') {
					$("#mmail").modal('show');
				}else if (response == 'Enviar') {
					alert('Esta opción no se encuetra habilitada.');
				}
			}
		});
	}
}
function sendMsg () {
	if($("#para").val() != ''){
		location.href='http://190.41.246.91:3000/?para='+$("#para").val()+'&asunto='+$("#asunto").val()+'&texto='+$("#texto").val();
	}
}
