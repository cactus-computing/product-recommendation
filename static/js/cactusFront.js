window.onload = processProduct;

const cactusScript = document.getElementById('CactusScript');
const COMPANY = cactusScript.src.match(/(\?|\&)([^=]+)\=([^&]+)/)[3]

const CODE_STATUS = 'local' // options: local, dev, prod

const HOST_DICT = {
    local: "http://localhost:8000",
    dev: "https://dev.cactusco.cl",
    prod: "https://cactusco.cl"
}

const CLIENT_METADATA = {
    'quema': {
        'target-div': "#main .elementor-inner",
        'product-name-selector': ".elementor-widget-container h1",
        'insert-before': "lastChild"
    },
    'makerschile': {
        'target-div': "#content .ast-container .woo-variation-gallery-product",
        'product-name-selector': ".entry-title",
        'insert-before': "lastChild"
    },
}


function processProduct () {
  
  const productName = document.querySelector(CLIENT_METADATA[COMPANY]['product-name-selector']).innerText;
  const recommenderSection = document.createElement("div");

  importStyles();
  
  crossSellDiv = createCactusCarousel("Productos Complementarios", "cross-sell", recommenderSection);
  upSellDiv = createCactusCarousel("Productos Similares", "up-sell", recommenderSection);

  getPredictions(crossSellDiv, type="cross_selling", productName, k=30).then( function (success){ 
    if(success){
      createCactusContainer(recommenderSection);
      productScroll(type='cross-sell');
    }
  });

  getPredictions(upSellDiv, type="up_selling", productName, k=30).then( function (success){ 
    if(success){
      createCactusContainer(recommenderSection);
      productScroll(type='up-sell');
    }
  });
}


function importStyles () {
  /* Create Div and add content */
  
  const link = document.createElement("link");
  const head = document.head;
  
  link.type = "text/css";
  link.rel = "stylesheet";
  link.href = HOST_DICT[CODE_STATUS] + "/static/css/" + COMPANY + ".css";


  head.appendChild(link);
}

function createCactusCarousel(title, type, recommenderSection){
  recommenderSection.className = `${type} slider`;
    recommenderSection.id = `${type}-slider`;
    
    products = [];

    const titleDiv = document.createElement("div");
    titleDiv.className =  `${type} title`;
    const sectionTitle = document.createElement("h2");
    sectionTitle.innerText = title;
    titleDiv.appendChild(sectionTitle)
    recommenderSection.appendChild(titleDiv)

    const slideBoxDiv = document.createElement("div");
    slideBoxDiv.className =  `${type} slide-box`;
    slideBoxDiv.id = `${type}-slide-box`;
    recommenderSection.appendChild(slideBoxDiv);

    const arrowLeft = document.createElement("button");
    arrowLeft.className = `${type} ctrl-btn pro-prev`;
    arrowLeft.innerText = "<";
    slideBoxDiv.appendChild(arrowLeft);

    const productsDiv = document.createElement("div");
    productsDiv.className = `${type} slide`;
    productsDiv.id = `${type}-slide`;
    slideBoxDiv.appendChild(productsDiv);

    const arrowRight = document.createElement("button");
    arrowRight.className = `${type} ctrl-btn pro-next`;
    arrowRight.innerText = ">";
    slideBoxDiv.appendChild(arrowRight);
    return productsDiv
}

const getPredictions = async function (productsDiv, type, productName, k) {
  const response = await fetch(
    `${HOST_DICT[CODE_STATUS]}/api/${type}?name=${productName}&company=${COMPANY}&top-k=${k}`
  )
  const data = await response.json();
  let success = false
  if (data["empty"] === false){
    success = true
    createProductHtml(data["data"], productsDiv);
  }
  return success;
}

function createCactusContainer(recommenderSection){
  
  const targetDiv = document.querySelector(CLIENT_METADATA[COMPANY]['target-div']);
  const cactusContainer = document.createElement("div");
  cactusContainer.id = "cactusContainer"
  cactusContainer.class = "cactusRecommendation"

  cactusContainer.appendChild(recommenderSection)
  targetDiv.insertBefore(cactusContainer, targetDiv[CLIENT_METADATA[COMPANY]['insert-before']]); 
  
}

function createProductHtml (data, productsDiv) {
  data.forEach( function(prod) {
    const productDiv = document.createElement("div");
    productDiv.id = prod['sku']
    productDiv.className = "product";
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
        productPrice.innerText = prod['price'];
        productPrice.className = "product-price";
        productPriceDiv.appendChild(productPrice);

        productDiv.appendChild(productPriceDiv)

    productsDiv.appendChild(productDiv)
  });
}

function createHtmlElement () {

}

//-----------------------slider------------------------//

function productScroll(type) {

    let slider = document.getElementById(`${type}-slide-box`);
    let next = document.getElementsByClassName(`${type} pro-next`);
    let prev = document.getElementsByClassName(`${type} pro-prev`);
    let slide = document.getElementById(`${type}-slide`);
    let item = document.getElementById(`${type}-slide`);

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