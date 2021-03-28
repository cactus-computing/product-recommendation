function setGoogleAnalytics() {
    const script = document.createElement('script');
    const head = document.head;
    script.async = "async";
    script.src = "https://www.googletagmanager.com/gtag/js?id=UA-159111495-1";
    head.appendChild(script);

    let scriptJs = document.createElement("script");
    scriptJs.innerText = 
        "window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config','UA-159111495-1');";
    head.appendChild(scriptJs);
}

function readCookieStartingWith(name) { 
    //leemos todas las cookies que el nombre empiece con "ClickRelatedProduct" 
    //el output es un arreglo con los nombres
    let productNames = [];
    let nameEQ = name;
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i += 1) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1,c.length);
        if (c.substring(0,19).indexOf(nameEQ) == 0){ 
            productNames.push(c.substring(c.indexOf("=")+1,c.length));
        }
    }
  return productNames;
}

setGoogleAnalytics();

const relatedProductsClicked = readCookieStartingWith("ClickRelatedProduct"); 
//leemos todas las cookies que el nombre empiece con "ClickRelatedProduct"

const itemsBought = document.querySelectorAll('.order_details tbody tr');
// extrae todas las filas de productos comprados
const purchasedProducts = [];
for (let i = 0; i < itemsBought.length; i++) { //iterar por cada linea de producto comprado
    const item = itemsBought[i].querySelectorAll('td');
    const productName = item[0].innerText.toLowerCase();
    const productTotal = parseInt(item[1].querySelector('.product-total span').innerText.substring(1).replaceAll(".","").replaceAll('"',""));
    purchasedProducts.push({ 
        productName: productName,
        productTotal: productTotal
    });
}

relatedProductPurchasedAmount = 0;
for (let i = 0; i < purchasedProducts.length; i++) {
  //para cada producto comprado veremos si es que hay alguna cookie de producto relacionado
  const purchasedProductName = purchasedProducts[i].productName;
  let k = 0;
  for (let j = 0; j < relatedProductsClicked.length; j++) {
    //para cada producto relacionado clickeado
    const clickedProductName = relatedProductsClicked[j];
    if (purchasedProductName.indexOf(clickedProductName) != -1) {
      // si es que alguno de los productos que compro, fue clickeado antes, entonces lo marco
            k += 1;
    }
  }
  if (k > 0) {
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