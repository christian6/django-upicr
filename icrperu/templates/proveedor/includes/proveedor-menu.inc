<nav class="navbar navbar-fixed-top navbar-inverse bs-docs-nav" role="banner">
	<div class="navbar-header">
		<button type="button" data-toggle="collapse" data-target=".bs-navbar-collapse" class="navbar-toggle">
			<span class="sr-only">Toogle navigation</span>
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
			<span class="icon-bar"></span>
		</button>
    
    <div class="navbar-brand">
      <a href="{% url 'vw_home_supplier' %}"><img id="icrlogo" src="/media/resource/images/icrlogo.png" ></a>
      <a href="{% url 'vw_home_supplier' %}">
        Proveedores
      </a>  
    </div>
	</div>
	<!-- Collect the nav links, forms, and other content for toggling -->
  <nav class="collapse navbar-collapse bs-navbar-collapse" role="navigation">
    <ul class="nav navbar-nav">
      <li class="active"><a href="{% url 'vw_home_supplier' %}"><span class="glyphicon  glyphicon-home"></span></a></li>
      <!--<li><a href="#">Link</a></li>-->
      <!-- Suminstro -->
      <li class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">Solicitud de Cotización <b class="caret"></b></a>
        <ul class="dropdown-menu">
          <li><a href="{% url 'vw_list_cotizacion_supplier' %}">Cotización</a></li>
        </ul>
      </li>
      <!-- Cotizacion -->
      <li class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">Orden de Compra <b class="caret"></b></a>
        <ul class="dropdown-menu">
          <li><a href="{% url 'vw_list_Order_buy' %}">Lista de Orden de Compra</a></li>
        </ul>
      </li>
    </ul>
    <ul class="nav navbar-nav navbar-right">
      <li class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown"><span class="glyphicon glyphicon-user"></span> {{ request.session.rznpro }} <b class="caret"></b></a>
        <ul class="dropdown-menu">
          <li>
            <div class="bs-user-data">
                <h6><strong>
                Ruc : {{ request.session.rucpro }}<br />
                Razón : {{ request.session.rznpro }}<br />
                Tipo : {{ request.session.tippro }}
              </strong>
                </h6>
            </div>
          </li>
          <li><a href="{%url 'vw_logout_supliert' %}"><span class="glyphicon glyphicon-log-out"></span> Cerrar Session</a></li>
        </ul>
      </li>
    </ul>
  </nav><!-- /.navbar-collapse -->
</nav>