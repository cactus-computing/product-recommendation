window.onload = addCactusRecommendation;
var CODE_STATUS = 'local' // options: local, dev, prod
var COMPANY = "quema";

var HOST_DICT = {
    local: "http://localhost:8000",
    dev: "https://dev.cactusco.cl",
    prod: "https://cactusco.cl"
}

var formatter = new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
  })

function addCactusRecommendation () {
    /* Create Div and add content */
    var recommenderSection = document.createElement("div");
    var link = document.createElement("link");
    var head = document.head;
    
    link.type = "text/css";
    link.rel = "stylesheet";
    link.href = HOST_DICT[CODE_STATUS] + "/static/css/" + COMPANY + ".css";

    head.appendChild(link);

    recommenderSection.className = "cross-sells-carrousel";
    var targetDiv = document.querySelector("#main .elementor-inner");
    //var targetDiv = document.querySelector("#main .elementor-inner .elementor-section-wrap");
    products = [];

    var titleDiv = document.createElement("div");
    titleDiv.className = "section-title";
    var sectionTitle = document.createElement("h2");
    sectionTitle.innerText = "Productos Relacionados";
    titleDiv.appendChild(sectionTitle)
    recommenderSection.appendChild(titleDiv)

    var productsDiv = document.createElement("div");
    productsDiv.className = "section-products";
    recommenderSection.appendChild(productsDiv);

    var productName = document.querySelector(".elementor-widget-container h1").innerText;
    console.log(productName)

    var host = "https://cactusco.cl";
    var localhost = "http://localhost:8000";
    // fetch data from API
    fetch(
        HOST_DICT[CODE_STATUS] + "/api/cross_selling?name=" + productName+ "&company="+COMPANY+"&top-k=5"
    ).then( function(res) {
        return res.json();
    }).then( function(data) {
        console.log(data["data"][0])
        data["data"].forEach( function(prod) {
            var productDiv = document.createElement("div");
            productDiv.id = prod['sku']
            productDiv.className = "cross-sells-product";
                var productImageLink = document.createElement("a")
                productImageLink.href = prod['permalink']
                 
                var productImage = document.createElement("img");
                productImage.src = prod['href']
                productImage.className = "product-image";
                productImageLink.appendChild(productImage)
                productDiv.appendChild(productImageLink);

                var productNameDiv = document.createElement("div");
                productNameDiv.className = "product-name-box";

                    var productTitleLink = document.createElement("a")
                    productTitleLink.href = prod['permalink']
                    
                    var productTitle = document.createElement("h2");
                    productTitle.innerText = prod['name']
                    productTitle.className = "product-name";
                    productTitleLink.appendChild(productTitle)
                    productNameDiv.appendChild(productTitleLink);
                    
                    productDiv.appendChild(productNameDiv)
                
                    var productPriceDiv = document.createElement("div");
                productPriceDiv.className = "product-price-box";
                    
                    var productPrice = document.createElement("span");
                    productPrice.innerText = formatter.format(prod['price']);
                    productPrice.className = "product-price";
                    productPriceDiv.appendChild(productPrice);

                    productDiv.appendChild(productPriceDiv)

            productsDiv.appendChild(productDiv)
        });
    });
    

    var cactusContainer = document.createElement("div");
    cactusContainer.id = "cactusContainer"
    cactusContainer.class = "cactusRecommendation"

    cactusContainer.appendChild(recommenderSection)

    // añade el elemento creado y su contenido al DOM
    targetDiv.insertBefore(cactusContainer, targetDiv.lastChild);
    //targetDiv.appendChild(cactusContainer);
}