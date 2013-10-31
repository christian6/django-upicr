$(document).ready(function () {
	var $user = $("#username");
	var $pass = $("#passwd");
	$user.popover({
		content : 'Campo Usuario Vacio',
		placement : 'right',
		delay: { show: 100, hide: 100 },
		trigger : 'manual'
	});
	$pass.popover({
		content : 'Campo password Vacio',
		placement : 'right',
		delay: { show: 100, hide: 100 },
		trigger : 'manual'
	});
	$("#accept").on('click',function () {
		inlogin();
	});
	$user.on('focus', function () {
		$user.popover('hide');
	});
	$pass.on('focus',function () {
		$pass.popover('hide');
	});
});
function inlogin () {
	//console.log(validLogin());
	if (validLogin()) {
		var prm = {
			'username' : $("#username").val(),
			'passwd' : hex_md5($("#passwd").val())
		}
		$.ajax({
			url : '/proveedor/security/login/',
			type : 'GET',
			data : prm,
			dataType : 'html',
			success : function (response) {
				console.log(response);
				if (response == 'success') {
					location.href='home/';
				}else if(response == 'fail'){
					$("#accept").popover({
						content : 'Usuario o Contraseña Incorrecta',
						placement : 'bottom',
						delay: { show: 100, hide: 2024 },
						trigger : 'manual'
					});
					$("#accept").popover('show');
					$(".popover").css("backgroundColor","rgba(250,188,80,.8)");
					$(".popover-content").css("textAlign","center");
					//$(".popover-content").css("fontWeight","bold");
					setTimeout(function() {
						$("#accept").popover('hide');
					}, 6600);
				}
			},
			error : function (obj,que,otr) {
				msgError(null,null,null);
			}
		});
	}
}
function validLogin () {
	var $sts = false;
	var $usern = $("#username");
	var $passwd = $("#passwd");
	if ($usern.val() == '') {
		$usern.popover('show');
		$(".popover").css("backgroundColor","rgba(169,3,16,.6)");
		$(".popover").css("color","rgba(240,240,240,1)");
		sts = false;
		return sts;
	}else{
		sts = true;
	}
	if ($passwd.val() == '') {
		$passwd.popover('show');
		$(".popover").css("backgroundColor","rgba(169,3,16,.6)");
		$(".popover").css("color","rgba(240,240,240,1)");
		sts = false;
		return sts;
	}else{
		sts = true;
	}
	return sts;
}
function redirect () {
	if( $('#ruc').val().length == 11 ){
		location.href='home/';
	}
}