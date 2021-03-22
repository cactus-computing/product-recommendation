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

function readCookie(name) { 
    //leemos todas las cookies que el nombre empiece con "ClickRelatedProduct" 
    //el output es un arreglo con los nombres
    var productNames = [];
    var nameEQ = name;
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.substring(0,19).indexOf(nameEQ) == 0){ 
            productNames.push(c.substring(c.indexOf("=")+1,c.length));
        }
    }
  return productNames;
}
  
relatedProductsClicked = readCookie("ClickRelatedProduct"); //leemos todas las cookies que el nombre empiece con "ClickRelatedProduct"
//console.log(relatedProductsClicked)

var tbody = document.querySelectorAll('#my-orders-table tbody'); // extrae todas las filas de productos comprados
var purchasedProducts = [];
for (var i = 0; i < tbody.length; i++) { //iterar por cada linea de producto comprado
  td = tbody[i].querySelectorAll('td');
  var productName = td[0].querySelector('.product-name').innerText.toLowerCase();
  var productSKU = td[1].innerText.trim();
  var productPrice = parseInt(td[2].querySelector('.price .this').innerText.substring(1).replaceAll(".",""));
  var productQuantity = parseInt(td[3].querySelector('.nobr').innerText.trim());
  var productTotal = parseInt(td[4].querySelector('.price .this').innerText.substring(1).replaceAll(".",""));  
  
  purchasedProducts.push({ 
    productName: productName,
    productSKU: productSKU,
    productPrice: productPrice,
    productQuantity: productQuantity,
    productTotal: productTotal
  });
  }
//console.log(purchasedProducts)
relatedProductPurchasedAmount = 0;
for (var i = 0; i < purchasedProducts.length; i++) {
  //para cada producto comprado veremos si es que hay alguna cookie de producto relacionado
  //console.log(purchasedProducts[i].productName);
  var purchasedProductName = purchasedProducts[i].productName;
  var k = 0;
  for (var j = 0; j < relatedProductsClicked.length; j++) {
    //para cada producto relacionado clickeado
    var clickedProductName = relatedProductsClicked[j];
    if (purchasedProductName == clickedProductName) {
      // si es que alguno de los productos que compro, fue clickeado antes, entonces lo marco
      var k = k+1;
    }
  }
  if (k>0) {
    //si el producto esta marcado, entonces sumo el total al monto de productos relacionados
    relatedProductPurchasedAmount = relatedProductPurchasedAmount + purchasedProducts[i].productTotal
  }
}

//console.log(relatedProductPurchasedAmount);

createCookie("totalAmountRP",relatedProductPurchasedAmount);
//creamos cookie para leerla en GTM y enviarla a Google Analytics
//mic
//drop