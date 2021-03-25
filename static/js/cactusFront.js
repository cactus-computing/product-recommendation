window.onload = addCactusRecommendation;

const cactusScript = document.getElementById('CactusScript');
const COMPANY = cactusScript.src.match(/(\?|\&)([^=]+)\=([^&]+)/)[3]

const CODE_STATUS = 'dev' // options: local, dev, prod

const HOST_DICT = {
    local: "http://localhost:8000",
    dev: "https://dev.cactusco.cl",
    prod: "https://cactusco.cl"
}

const formatter = new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
  })

const CLIENT_METADATA = {
    'quema': {
        'target-div': "#main .elementor-inner",
        'product-name-selector': ".elementor-widget-container h1"
    },
    'makerschile': {
        'target-div': "#content .ast-container #secondary",
        'product-name-selector': ".entry-title"
    },
}

function addCactusRecommendation () {
    /* Create Div and add content */
    const recommenderSection = document.createElement("div");
    const link = document.createElement("link");
    const head = document.head;
    
    link.type = "text/css";
    link.rel = "stylesheet";
    link.href = HOST_DICT[CODE_STATUS] + "/static/css/" + COMPANY + ".css";

    head.appendChild(link);

    recommenderSection.className = "cross-sell-slider";
    recommenderSection.id = "cross-sell-slider"
    const targetDiv = document.querySelector(CLIENT_METADATA[COMPANY]['target-div']);
    products = [];

    const titleDiv = document.createElement("div");
    titleDiv.className = "cross-sell-title";
    const sectionTitle = document.createElement("h2");
    sectionTitle.innerText = "Productos Complementarios";
    titleDiv.appendChild(sectionTitle)
    recommenderSection.appendChild(titleDiv)


    //------ slider stuff --------//
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
    //------ end slider stuff --------//

    const productName = document.querySelector(CLIENT_METADATA[COMPANY]['product-name-selector']).innerText;
    console.log(productName)
    
    // fetch data from API
    fetch(
        HOST_DICT[CODE_STATUS] + "/api/cross_selling?name=" + productName+ "&company="+COMPANY+"&top-k=20"
    ).then( function(res) {
        return res.json();
    }).then( function(data) {
        let success = false

        if (data["empty"] === false){
            console.log('data is not empty, carrying on')
            success = true
        }

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
        return success;

    }).then(function (success) {
        if (success){
            const cactusContainer = document.createElement("div");
            cactusContainer.id = "cactusContainer"
            cactusContainer.class = "cactusRecommendation"

            cactusContainer.appendChild(recommenderSection)
            targetDiv.insertBefore(cactusContainer, targetDiv.lastChild);
        }
        productScroll();
    });
}

//-----------------------slider------------------------//

function productScroll() {

    let slider = document.getElementById("cross-sell-slide-box");
    let next = document.getElementsByClassName("pro-next");
    let prev = document.getElementsByClassName("pro-prev");
    let slide = document.getElementById("cross-sell-slide");
    let item = document.getElementById("cross-sell-slide");

    for (let i = 0; i < next.length; i++) {
      //refer elements by class name
  
      let position = 0; //slider postion
      let width = 210; // product box + margin width
      let visibleProductsWanted = 3;
      prev[i].addEventListener("click", function() {
        //click previos button
        if (position > 0) {
          //avoid slide left beyond the first item
          position -= 1;
          slide.scroll({ left: slide.scrollLeft -= visibleProductsWanted * width });
        }
      });
  
      next[i].addEventListener("click", function() {
        if (position >= 0 && position < hiddenItems()) {
          //avoid slide right beyond the last item
          position += 1;
          slide.scroll({ left: slide.scrollLeft += visibleProductsWanted * width });
        }
      });
    }
  
    function hiddenItems() {
      //get hidden items
      let items = getCount(item, false);
      let visibleItems = slider.offsetWidth / 210;
      return items - Math.ceil(visibleItems);
    }
  }
  
  function getCount(parent, getChildrensChildren) {
    //count no of items
    let relevantChildren = 0;
    let children = parent.childNodes.length;
    for (let i = 0; i < children; i++) {
      if (parent.childNodes[i].nodeType != 3) {
        if (getChildrensChildren)
          relevantChildren += getCount(parent.childNodes[i], true);
        relevantChildren++;
      }
    }
    return relevantChildren;
  }

//----------------------- end slider------------------------//