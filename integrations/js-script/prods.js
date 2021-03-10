document.body.onload = addCactusRecommendation;

products = [
    {
        sku: 3494551,
        price: 2590,
        name: "Rodillo chiporro",
        href: "https://sodimac.scene7.com/is/image/SodimacCL/3494551?fmt=jpg&fit=constrain,1&wid=420&hei=420"
    },
    {
        sku: 1954210,
        price: 9990,
        name: "Pistola de silicona",
        href: "https://sodimac.scene7.com/is/image/SodimacCL/1954210?fmt=jpg&fit=constrain,1&wid=420&hei=420"
    },
    {
        sku: 8700575,
        price: 129990,
        name: "Taladro",
        href: "https://sodimac.scene7.com/is/image/SodimacCL/8700575?fmt=jpg&fit=constrain,1&wid=420&hei=420"
    },
]

function addCactusRecommendation () {
    // crea un nuevo div
    // y añade contenido
    var recommenderSection = document.createElement("div");
    var mainDiv = document.getElementById("main");
    
    products.forEach((prod) => {
        var productDiv = document.createElement("div");
        productDiv.id = prod.sku

        var productTitle = document.createElement("h2");
        productTitle.innerText = prod.name
        productDiv.appendChild(productTitle);

        var productImage = document.createElement("img");
        productImage.src = prod.href
        productDiv.appendChild(productImage);

        var productPrice = document.createElement("span");
        productPrice.innerText = prod.price
        productDiv.appendChild(productPrice);

        recommenderSection.appendChild(productDiv)
    });

    var cactusContainer = document.createElement("div");
    cactusContainer.id = "cactusContainer"
    cactusContainer.class = "cactusRecommendation"
    cactusContainer.appendChild(recommenderSection)

    // añade el elemento creado y su contenido al DOM
    document.body.insertBefore(cactusContainer, mainDiv);
}