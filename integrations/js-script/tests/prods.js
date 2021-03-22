window.onload = addCactusRecommendation;

function addCactusRecommendation () {
    /* Create Div and add content */
    var recommenderSection = document.createElement("div");
    var mainDiv = document.getElementById("elementor-inner");
    products = [];
    var recommederSection = null
    var productSKU = document.getElementsByClassName("sku")[0].innerText
    console.log(productSKU)
    // fetch data from API
    fetch("http://localhost:8000/api/cross_selling?sku=" + productSKU+ "&company=quema").then( (res) => {
        return res.json();
    }).then( (data) => {
        console.log(data["data"][0])
        data["data"].forEach( (prod) => {
            var productDiv = document.createElement("div");
            productDiv.id = prod['sku']

            var productTitle = document.createElement("h2");
            productTitle.innerText = prod['name']
            productDiv.appendChild(productTitle);

            var productImage = document.createElement("img");
            productImage.src = prod['href']
            productDiv.appendChild(productImage);

            var productPrice = document.createElement("span");
            productPrice.innerText = prod['price']
            productDiv.appendChild(productPrice);

            recommenderSection.appendChild(productDiv)
        });
    });
    

    var cactusContainer = document.createElement("div");
    cactusContainer.id = "cactusContainer"
    cactusContainer.class = "cactusRecommendation"
    cactusContainer.appendChild(recommenderSection)

    // añade el elemento creado y su contenido al DOM
    document.body.insertBefore(cactusContainer, mainDiv);
}