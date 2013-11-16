$(document).ready(function () {
	
});
function showkey (nro) {
	$("#nro").val(nro);
	$("#keyc").modal('show');
}
function valid () {
	if ($("#key").val() == '') {
		$("#keyc").modal('hide');
		msgWarning('Alerta','Campo Key Vacio!',true);
		$("#key").focus();
		setTimeout(function() {$("#keyc").modal('show');}, 1400);
		return;
	}else{
		var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
		var prm = {
			'csrfmiddlewaretoken' : csrfToken,
			nro : $("#nro").val(),
			key : $("#key").val()
		}
		$.ajax({
			url : '/ws/proveedor/consulting/key/valid/',
			type : 'POST',
			data : prm,
			dataType : 'json',
			success : function (response) {
				$("#keyc").modal('hide');
				var obj = JSON.parse(response);
				if (obj.status == 'success') {
					location.href='/proveedor/view/cotizacion/'+obj.ncot+'/';
				}else if(obj.status == 'error'){
					msgWarning('Warning','El Key que se ha ingresado es incorrecto.',true);
				}
				setTimeout(function() {$("#keyc").modal('show');}, 2200);
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	}
}