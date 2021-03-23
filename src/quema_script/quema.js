window.onload = addCactusRecommendation;

var formatter = new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
  })

function addCactusRecommendation () {
    /* Create Div and add content */
    var recommenderSection = document.createElement("div");
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

    var productSKU = document.getElementsByClassName("sku")[0].innerText
    console.log(productSKU)
    // fetch data from API
    fetch("https://dev.cactusco.cl/api/cross_selling?sku=" + productSKU+ "&company=quema&top-k=4").then( (res) => {
        return res.json();
    }).then( (data) => {
        console.log(data["data"][0])
        data["data"].forEach( (prod) => {
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
    targetDiv.insertBefore(cactusContainer, targetDiv.nextSibling);
    //targetDiv.appendChild(cactusContainer);
}