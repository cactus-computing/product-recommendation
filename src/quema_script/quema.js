window.onload = addCactusRecommendation;
const CODE_STATUS = 'local' // options: local, dev, prod
const COMPANY = "quema";

const HOST_DICT = {
    local: "http://localhost:8000",
    dev: "https://dev.cactusco.cl",
    prod: "https://cactusco.cl"
}

const formatter = new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
  })

function addCactusRecommendation () {
    /* Create Div and add content */
    const recommenderSection = document.createElement("div");
    const link = document.createElement("link");
    const head = document.head;
    
    link.type = "text/css";
    link.rel = "stylesheet";
    link.href = HOST_DICT[CODE_STATUS] + "/static/css/" + COMPANY + ".css";
    //link.href = "/Users/rodrigooyarzun/Documents/Proyectos/Cactus/CactusCo/static/css/quema.css";
    head.appendChild(link);

    /*Create --> <script type="text/javascript" src="js/lightslider.js"></script>*/
    const scriptSlider = document.createElement("script");
    
    scriptSlider.type = "text/javascript";
    scriptSlider.src = "slider.js";
    head.appendChild(scriptSlider);

    recommenderSection.className = "cross-sell-slider";
    recommenderSection.id = "cross-sell-slider"
    const targetDiv = document.querySelector("#main .elementor-inner");
    //var targetDiv = document.querySelector("#main .elementor-inner .elementor-section-wrap");
    products = [];

    const titleDiv = document.createElement("div");
    titleDiv.className = "cross-sell-title";
    const sectionTitle = document.createElement("h2");
    sectionTitle.innerText = "Productos Relacionados";
    titleDiv.appendChild(sectionTitle)
    recommenderSection.appendChild(titleDiv)

    const slideBoxDiv = document.createElement("div");
    slideBoxDiv.className = "cross-sell-slide-box";
    slideBoxDiv.id = "cross-sell-slide-box";
    recommenderSection.appendChild(slideBoxDiv);

        const arrowLeft = document.createElement("button");
        arrowLeft.className = "ctrl-btn pro-prev";
        arrowLeft.innerText = "<";
        slideBoxDiv.appendChild(arrowLeft);

        const productsDiv = document.createElement("div");
        productsDiv.className = "cross-sell-slide";
        productsDiv.id = "cross-sell-slide";
        slideBoxDiv.appendChild(productsDiv);

        const arrowRight = document.createElement("button");
        arrowRight.className = "ctrl-btn pro-next";
        arrowRight.innerText = ">";
        slideBoxDiv.appendChild(arrowRight);

    const productName = document.querySelector(".elementor-widget-container h1").innerText;
    console.log(productName)

    const host = "https://cactusco.cl";
    const localhost = "http://localhost:8000";
    // fetch data from API
    fetch(
        host + "/api/cross_selling?name=" + productName+ "&company="+COMPANY+"&top-k=10"
    ).then( function(res) {
        return res.json();
    }).then( function(data) {
        console.log(data["data"][0])
        data["data"].forEach( function(prod) {
            const productDiv = document.createElement("div");
            productDiv.id = prod['sku']
            productDiv.className = "cross-sell-product";
                const productImageLink = document.createElement("a")
                productImageLink.href = prod['permalink']
                 
                const productImage = document.createElement("img");
                productImage.src = prod['href']
                productImage.className = "product-image";
                productImageLink.appendChild(productImage)
                productDiv.appendChild(productImageLink);

                const productNameDiv = document.createElement("div");
                productNameDiv.className = "product-name-box";

                    const productTitleLink = document.createElement("a")
                    productTitleLink.href = prod['permalink']
                    
                    const productTitle = document.createElement("h2");
                    productTitle.innerText = prod['name']
                    productTitle.className = "product-name";
                    productTitleLink.appendChild(productTitle)
                    productNameDiv.appendChild(productTitleLink);
                    
                    productDiv.appendChild(productNameDiv)
                
                    const productPriceDiv = document.createElement("div");
                productPriceDiv.className = "product-price-box";
                    
                    const productPrice = document.createElement("span");
                    productPrice.innerText = formatter.format(prod['price']);
                    productPrice.className = "product-price";
                    productPriceDiv.appendChild(productPrice);

                    productDiv.appendChild(productPriceDiv)

            productsDiv.appendChild(productDiv)
        });
    });
    

    const cactusContainer = document.createElement("div");
    cactusContainer.id = "cactusContainer"
    cactusContainer.class = "cactusRecommendation"

    cactusContainer.appendChild(recommenderSection)

    // añade el elemento creado y su contenido al DOM
    targetDiv.insertBefore(cactusContainer, targetDiv.lastChild);
    //targetDiv.appendChild(cactusContainer);
}