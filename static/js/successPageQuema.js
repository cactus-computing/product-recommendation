function createCookie(name,value,days) {
    // crea cookie con nombre, valor y dias en que expirará
    if (days) {
        const date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        const expires = "; expires="+date.toGMTString();
    }
    else const expires = "";
    document.cookie = name+"="+value+expires+"; path=/";
  }

function setGoogleAnalytics () {
    const script = document.createElement("script");
    const head = document.head;
    script.async = "async";
    script.src = "https://www.googletagmanager.com/gtag/js?id=UA-119655898-1";
    head.appendChild(script);

    const scriptJs = document.createElement("script");
    scriptJs.innerText = 
        "window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config','UA-119655898-1');";
    head.appendChild(scriptJs);
    }

function readCookieStartingWith(name) { 
    //leemos todas las cookies que el nombre empiece con "ClickRelatedProduct" 
    //el output es un arreglo con los nombres
    const productNames = [];
    const nameEQ = name;
    const ca = document.cookie.split(';');
    for(const i=0;i < ca.length;i++) {
        const c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.substring(0,19).indexOf(nameEQ) == 0){ 
            productNames.push(c.substring(c.indexOf("=")+1,c.length));
        }
    }
  return productNames;
}

setGoogleAnalytics();

relatedProductsClicked = readCookieStartingWith("ClickRelatedProduct"); 
//leemos todas las cookies que el nombre empiece con "ClickRelatedProduct"

const itemsBought = document.querySelectorAll('.order_details tbody tr');
// extrae todas las filas de productos comprados
const purchasedProducts = [];
for (const i = 0; i < itemsBought.length; i++) { //iterar por cada linea de producto comprado
  item = itemsBought[i].querySelectorAll('td');
  const productName = item[0].innerText.toLowerCase();
  const productTotal = parseInt(item[1].querySelector('.product-total span').innerText.substring(1).replaceAll(".","").replaceAll('"',""));  
  
  purchasedProducts.push({ 
    productName: productName,
    productTotal: productTotal
  });
  }

relatedProductPurchasedAmount = 0;
for (const i = 0; i < purchasedProducts.length; i++) {
  //para cada producto comprado veremos si es que hay alguna cookie de producto relacionado
  const purchasedProductName = purchasedProducts[i].productName;
  const k = 0;
  for (const j = 0; j < relatedProductsClicked.length; j++) {
    //para cada producto relacionado clickeado
    const clickedProductName = relatedProductsClicked[j];
    if (purchasedProductName.indexOf(clickedProductName) != -1) {
      // si es que alguno de los productos que compro, fue clickeado antes, entonces lo marco
      const k = k+1;
    }
  }
  if (k>0) {
    //si el producto esta marcado, entonces sumo el total al monto de productos relacionados
    relatedProductPurchasedAmount = relatedProductPurchasedAmount + purchasedProducts[i].productTotal
  }
}

window.addEventListener('load', function() {
  if (relatedProductPurchasedAmount > 0) {
    gtag('event', 'Related Product Sales', {
        'event_category': 'Related Product Sales',
        'event_label': '',
        'value': relatedProductPurchasedAmount
      });
  }   
});

//creamos cookie para leerla en GTM y enviarla a Google Analytics
//mic
//drop