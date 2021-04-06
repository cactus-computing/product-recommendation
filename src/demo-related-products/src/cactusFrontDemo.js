window.onload = processProduct;

const cactusScriptUrl = document.getElementById('CactusScript').src;
const queryString = cactusScriptUrl.substring(cactusScriptUrl.indexOf('?'));
const urlParams = new URLSearchParams(queryString);

const company = urlParams.get('client');
const codeStatus = urlParams.get('environment'); // options: local, dev, prod

const HOST_DICT = {
    local: 'http://localhost:8000',
    dev: 'https://dev.cactusco.cl',
    prod: 'https://cactusco.cl',
};

function importStyles() {
    const link = document.createElement('link');
    const head = document.head;

    link.type = 'text/css';
    link.rel = 'stylesheet';
    link.href = `${HOST_DICT[codeStatus]}/static/css/${company}.css`;

    head.appendChild(link);
}

function createCactusContainer() {
    const targetDiv = document.querySelector('#demo');
    const cactusContainer = document.createElement('div');
    cactusContainer.id = 'cactusContainer';
    cactusContainer.class = 'cactusRecommendation';
    targetDiv.insertBefore(cactusContainer, targetDiv.nextSibling);
    return cactusContainer;
}

function processProduct() {
    const productName = document.querySelector('.product-details-box h1').innerText.trim();
    const upSellSection = document.createElement('div');
    const crossSellSection = document.createElement('div');

    importStyles();

    const crossSellDiv = createCactusCarousel('Productos Relacionados', 'cross-sell', crossSellSection);
    const upSellDiv = createCactusCarousel('Productos Similares', 'up-sell', upSellSection);

    const cactusContainer = createCactusContainer();

    getPredictions(crossSellDiv, type='cross_selling', productName, k = 30).then((success) => {
        if (success) {
            cactusContainer.appendChild(crossSellSection);
            productScroll(type='cross-sell');
        }
    });

    getPredictions(upSellDiv, type = 'up_selling', productName, k = 30).then((success) => {
        if (success) {
            cactusContainer.appendChild(upSellSection);
            productScroll(type='up-sell');
        }
    });
}

function createCactusCarousel(title, type, recommenderSection) {
    recommenderSection.className = `${type} slider`;
    recommenderSection.id = `${type}-slider`;

    products = [];

    const titleDiv = document.createElement('div');
    titleDiv.className = `${type} title`;
    const sectionTitle = document.createElement('h2');
    sectionTitle.innerText = title;
    titleDiv.appendChild(sectionTitle);
    recommenderSection.appendChild(titleDiv);

    const slideBoxDiv = document.createElement('div');
    slideBoxDiv.className = `${type} slide-box`;
    slideBoxDiv.id = `${type}-slide-box`;
    recommenderSection.appendChild(slideBoxDiv);

    const arrowLeft = document.createElement('button');
    arrowLeft.className = `${type} ctrl-btn pro-prev`;
    arrowLeft.innerText = '<';
    slideBoxDiv.appendChild(arrowLeft);

    const productsDiv = document.createElement('div');
    productsDiv.className = `${type} slide`;
    productsDiv.id = `${type}-slide`;
    slideBoxDiv.appendChild(productsDiv);

    const arrowRight = document.createElement('button');
    arrowRight.className = `${type} ctrl-btn pro-next`;
    arrowRight.innerText = '>';
    slideBoxDiv.appendChild(arrowRight);
    return productsDiv;
}

const getPredictions = async function (productsDiv, type, productName, k) {
    const response = await fetch(
        `${HOST_DICT[codeStatus]}/api/${type}?name=${productName}&company=${company
        }&top-k=${k}`,
    );
    const data = await response.json();
    let success = false;
    if (data['empty'] === false) {
        success = true;
        createProductHtml(data['data'], productsDiv);
    }
    return success;
};

function createProductHtml(data, productsDiv) {
    data.forEach((prod) => {
        const productDiv = document.createElement('div');
        productDiv.id = prod.sku;
        productDiv.className = 'product';
        const productImageLink = document.createElement('a');
        productImageLink.href = prod.permalink;

        const productImage = document.createElement('img');
        productImage.src = prod.href;
        productImage.className = 'product-image';

        productImageLink.appendChild(productImage);
        productDiv.appendChild(productImageLink);

        const productNameDiv = document.createElement('div');
        productNameDiv.className = 'product-name-box';

        const productTitleLink = document.createElement('a');
        productTitleLink.href = prod.permalink;

        const productTitle = document.createElement('h2');
        productTitle.innerText = prod.name;
        productTitle.className = 'product-name';

        productTitleLink.appendChild(productTitle);
        productNameDiv.appendChild(productTitleLink);

        productDiv.appendChild(productNameDiv);

        const productPriceDiv = document.createElement('div');
        productPriceDiv.className = 'product-price-box';

        const productPrice = document.createElement('span');
        productPrice.innerText = prod.price;
        productPrice.className = 'product-price';
        productPriceDiv.appendChild(productPrice);

        productDiv.appendChild(productPriceDiv);

        productsDiv.appendChild(productDiv);
    });
}

// -----------------------slider------------------------//

function productScroll(type) {
    const slider = document.getElementById(`${type}-slide-box`);
    const next = document.getElementsByClassName(`${type} pro-next`);
    const prev = document.getElementsByClassName(`${type} pro-prev`);
    const slide = document.getElementById(`${type}-slide`);
    const item = document.getElementById(`${type}-slide`);

    for (let i = 0; i < next.length; i += 1) {
        // refer elements by class name

        let position = 0; // slider postion
        const width = 210; // product box + margin width
        const visibleProductsWanted = 3;
        prev[i].addEventListener('click', () => {
        // click previos button
            if (position > 0) {
                // avoid slide left beyond the first item
                position -= 1;
                slide.scroll({ left: slide.scrollLeft -= visibleProductsWanted * width });
            }
        });

        next[i].addEventListener('click', () => {
            if (position >= 0 && position < hiddenItems()) {
                // avoid slide right beyond the last item
                position += 1;
                slide.scroll({ left: slide.scrollLeft += visibleProductsWanted * width });
            }
        });
    }

    function hiddenItems() {
        // get hidden items
        const items = getCount(item, false);
        const visibleItems = slider.offsetWidth / 210;
        return items - Math.ceil(visibleItems);
    }
}

function getCount(parent, getChildrensChildren) {
    // count no of items
    let relevantChildren = 0;
    const children = parent.childNodes.length;
    for (let i = 0; i < children; i += 1) {
        if (parent.childNodes[i].nodeType !== 3) {
            if (getChildrensChildren)
                relevantChildren += getCount(parent.childNodes[i], true);
            relevantChildren++;
        }
    }
    return relevantChildren;
}

// ----------------------- end slider------------------------//
