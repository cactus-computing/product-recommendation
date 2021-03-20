
function createCookie(name,value,days) {
	// crea cookie con nombre, valor y dias en que expirará
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}
var timestamp = Date.now();
createCookie("ClickRelatedProduct"+"_"+timestamp,"{{cjs - Related Product name clicked}}",5)
/*
crea una cookie por cada producto relacionado clickeado
el nombre del producto clickeado viene de un evento en GTM que guarda el nombre en la variable: {{cjs - Related Product name clicked}}
function() {
return google_tag_manager["GTM-T3G5JVZ"].dataLayer.get("gtm.element").parentElement.parentElement.querySelector(".product-info .containerNombreYMarca .product-name a").innerText.toLowerCase()
}*/