const cactusScriptUrl = document.getElementById('CactusScript').src;
const queryString = cactusScriptUrl.substring(cactusScriptUrl.indexOf('?'));
const urlParams = new URLSearchParams(queryString);

const company = urlParams.get('client');
const codeStatus = urlParams.get('environment'); // options: local, dev, prod

const HOST_DICT = {
    local: 'http://localhost:8000',
    dev: 'https://dev.cactusco.cl',
    prod: 'https://production-cactus.herokuapp.com',
};

const CLIENT_METADATA = {
    quema: {
        'target-div': '#main .elementor-inner .elementor-section-wrap',
        'product-name-selector': '.elementor-widget-container h1',
        'insert-before': 'nextElementSibling',
        'ga-measurement-id': 'UA-119655898-1',
        'product-page-identifier': 'url',
        'product-page-regex': '/producto/',
        'button-target-div': '.elementor-element-48636aa .elementor-widget-wrap .elementor-widget-heading',
        'button-insert-before': 'nextElementSibling',
    },
    makerschile: {
        'target-div': '.woocommerce-tabs.wc-tabs-wrapper',
        'product-name-selector': '.entry-title',
        'insert-before': 'nextElementSibling',
        'ga-measurement-id': 'UA-159111495-1',
        'product-page-identifier': 'url',
        'product-page-regex': '/producto/',
        'button-target-div': '.summary.entry-summary .product_meta',
        'button-insert-before': 'nextElementSibling',
    },
    pippa: {
        'target-div': '.seven.columns.omega',
        'product-name-selector': '.product_name',
        'insert-before': 'nextElementSibling.nextElementSibling',
        'ga-measurement-id': 'UA-105999666-1',
        'product-page-identifier': 'url',
        'product-page-regex': '/products/',
        'button-target-div': '.seven.columns.omega .description.bottom',
        'button-insert-before': 'nextElementSibling',
    },
    prat: {
        'target-div': '.product-essential form',
        'product-name-selector': '.product-name',
        'insert-before': 'nextElementSibling',
        'ga-measurement-id': 'UA-123207746-1',
        'product-page-identifier': 'css',
        'product-page-regex': '.product-view',
        'button-target-div': '.add-to-box-wrap.clearfix .elocker',
        'button-insert-before': 'nextElementSibling',
    },
    protteina: {
        'target-div': '.container.main.content',
        'product-name-selector': '.product_name',
        'insert-before': 'nextElementSibling',
        'ga-measurement-id': 'UA-148747724-1',
        'product-page-identifier': 'url',
        'product-page-regex': '/products/',
        'button-target-div': '.product_name',
        'button-insert-before': 'nextElementSibling',
    },
    construplaza: {
        'target-div': '.product-essential form',
        'product-name-selector': '.product-name',
        'insert-before': 'nextElementSibling',
        'ga-measurement-id': 'UA-128776327-1',
        'product-page-identifier': 'css',
        'product-page-regex': '.product-view',
        'button-target-div': '.add-to-box-wrap.clearfix .product-name',
        'button-insert-before': 'nextElementSibling',
    },
};

function setGoogleAnalytics() {
    const script = document.createElement('script');
    const { head } = document;
    script.async = 'async';
    script.src = `https://www.googletagmanager.com/gtag/js?id=${CLIENT_METADATA[company]['ga-measurement-id']}`;
    head.appendChild(script);

    const scriptJs = document.createElement('script');
    scriptJs.innerText = `window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config','${CLIENT_METADATA[company]['ga-measurement-id']}');`;
    head.appendChild(scriptJs);
}

function importStyles() {
    const link = document.createElement('link');
    const { head } = document;

    link.type = 'text/css';
    link.rel = 'stylesheet';
    link.href = `${HOST_DICT[codeStatus]}/static/css/${company}.css`;

    head.appendChild(link);
}

function createCactusContainer() {
    const targetDiv = document.querySelector(CLIENT_METADATA[company]['target-div']);
    const cactusContainer = document.createElement('div');
    cactusContainer.id = 'cactusContainer';
    cactusContainer.class = 'cactusRecommendation';
    targetDiv.parentElement.insertBefore(cactusContainer, targetDiv[CLIENT_METADATA[company]['insert-before']]);
    return cactusContainer;
}

function createProductHtml(data, productsDiv) {
    data.forEach((prod) => {
        const productDiv = document.createElement('div');
        productDiv.id = prod.sku;
        productDiv.className = 'product';
        const productImageLink = document.createElement('a');
        productImageLink.href = prod.permalink;

        const productImage = document.createElement('img');
        productImage.src = prod.img_url;
        productImage.className = 'product-image';
        productImage.addEventListener('click', () => {
            const productNameClicked = prod.name.toLowerCase();
            const timestamp = Date.now();
            const cookieName = `${'ClickRelatedProduct' + '_'}${timestamp}`;
            createCookie(cookieName, productNameClicked, 5);
            const productName = document.querySelector(CLIENT_METADATA[company]['product-name-selector']).innerText.trim();
            gtag('event', productName, {
                event_category: 'Related Product Click',
                event_label: productNameClicked,
                value: 1,
            });
        });

        productImageLink.appendChild(productImage);
        productDiv.appendChild(productImageLink);

        const productNameDiv = document.createElement('div');
        productNameDiv.className = 'product-name-box';

        const productTitleLink = document.createElement('a');
        productTitleLink.href = prod.permalink;

        const productTitle = document.createElement('h2');
        productTitle.innerText = prod.name;
        productTitle.className = 'product-name';
        productTitle.addEventListener('click', () => {
            const productNameClicked = prod.name.toLowerCase();
            const timestamp = Date.now();
            const cookieName = `${'ClickRelatedProduct' + '_'}${timestamp}`;
            createCookie(cookieName, productNameClicked, 5);
            const productName = document.querySelector(CLIENT_METADATA[company]['product-name-selector']).innerText.trim();
            gtag('event', productName, {
                event_category: 'Related Product Click',
                event_label: productNameClicked,
                value: 1,
            });
        });

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

const getPredictions = async function (productsDiv, type, productName, k) {
    const response = await fetch(
        `${HOST_DICT[codeStatus]}/api/${type}?name=${productName}&company=${company
        }&top-k=${k}`,
    );
    const data = await response.json();
    let success = false;
    if (data.empty === false) {
        success = true;
        createProductHtml(data.data, productsDiv);
    }
    return success;
};

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
            if (getChildrensChildren) relevantChildren += getCount(parent.childNodes[i], true);
            relevantChildren++;
        }
    }
    return relevantChildren;
}

// ----------------------- end slider ------------------------//

function processProduct() {
    const productName = document.querySelector(CLIENT_METADATA[company]['product-name-selector']).innerText.trim();
    const upSellSection = document.createElement('div');
    const crossSellSection = document.createElement('div');

    importStyles();

    const crossSellDiv = createCactusCarousel('Productos Relacionados', 'cross-sell', crossSellSection);
    const upSellDiv = createCactusCarousel('Productos Similares', 'up-sell', upSellSection);

    const cactusContainer = createCactusContainer();

    getPredictions(crossSellDiv, type = 'cross_selling', productName, k = 30).then((success) => {
        if (success) {
            cactusContainer.appendChild(crossSellSection);
            productScroll(type = 'cross-sell');
        }
    });

    getPredictions(upSellDiv, type = 'up_selling', productName, k = 30).then((success) => {
        if (success) {
            cactusContainer.appendChild(upSellSection);
            productScroll(type = 'up-sell');
        }
    });
    createScrollToRpButton();
}

// ----------------------- start button ------------------------//

function createScrollToRpButton() {
    const buttonTargetDiv = document.querySelector(CLIENT_METADATA[company]['button-target-div']);
    const scrollToRpButton = document.createElement('a');
    scrollToRpButton.className = 'scroll-to-rp-button';
    scrollToRpButton.innerText = 'Ver Productos Relacionados';
    scrollToRpButton.addEventListener('click', () => {
        document.getElementById('cactusContainer').scrollIntoView({
            behavior: 'smooth',
        });
        const productName = document.querySelector(CLIENT_METADATA[company]['product-name-selector']).innerText.trim();
        gtag('event', productName, {
            event_category: 'Scroll to RP Button Click',
            value: 1,
        });
    });
    buttonTargetDiv.parentElement.insertBefore(scrollToRpButton, buttonTargetDiv[CLIENT_METADATA[company]['button-insert-before']]);
}

// ----------------------- end button ------------------------//
// ----------------------- start A/B Testing ------------------------//

const AB_TESTING_THRESHOLD = 20;
// b alternative (randomChange=1) is cactus ON
const prefix = company;
const randomNumber = Math.floor(Math.random() * 100);

const changes = {
    1: {
        variants: {
            1: {
                execute() {
                    processProduct();
                },
            },
        },
    },
};
const variants = ['0'];

function createCookie(name, value, days) {
    let expires = '';
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = `; expires=${date.toGMTString()}`;
    }
    document.cookie = `${name}=${value}${expires}; path=/`;
}

function readCookie(name) {
    const nameEQ = `${name}=`;
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i += 1) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function createABtest() {
    let randomChange = 0;
    let abTest = 'Sin Cactus';
    if (randomNumber >= AB_TESTING_THRESHOLD) {
        randomChange = 1;
        abTest = 'Con Cactus';
    }
    window.addEventListener('load', () => {
        gtag('event', abTest, {
            'event_category': 'AB Testing',
            'event_label': '',
            'value': '',
        });
    });
    createCookie(`${prefix}-cookie`, variants[randomChange], 9);
    if (variants[randomChange] !== '0') {
        const newcookie = variants[randomChange].split('.');
        const changeID = newcookie[0];
        const variantID = newcookie[1];

        changes[changeID].variants[variantID].execute();
        sendDimension(changeID, variantID);
    } else {
        sendDimension(0);
    }
}
function sendDimension(changeID, variantID) {
    if (readCookie('_ga')) {
        if (changeID !== 0) {
            dataLayer.push({
                event: 'abTest', eventCategory: 'ab-test', eventAction: `${prefix}-${changeID}-${variantID}`, eventLabel: `${prefix}-${changeID}-${variantID}`, eventNonInteraction: 1,
            });
        } else {
            dataLayer.push({
                event: 'abTest', eventCategory: 'ab-test', eventAction: `${prefix}-0-0`, eventLabel: `${prefix}-0-0`, eventNonInteraction: 1,
            });
        }
    }
}

function processAbTest() {
    for (const j in changes) {
        for (const x in changes[j].variants) {
            variants.push(`${j}.${x}`);
        }
    }
    setGoogleAnalytics();
    if (readCookie(`${prefix}-cookie`)) {
        if (variants.indexOf(readCookie(`${prefix}-cookie`)) !== -1) {
            const currentCookie = readCookie(`${prefix}-cookie`).split('.');
            const currentChangeID = currentCookie[0];
            let currentVariantID = 0;
            if (currentChangeID !== 0) {
                currentVariantID = currentCookie[1];
                changes[currentChangeID].variants[currentVariantID].execute();
            }
            sendDimension(currentChangeID, currentVariantID);
        } else {
            eraseCookie(`${prefix}-cookie`);
            createABtest();
        }
    } else {
        createABtest();
    }
}

function isProductPage() {
    const identifier = CLIENT_METADATA[company]['product-page-identifier'];
    if (identifier === 'css') {
        const productPageDiv = document.querySelector(CLIENT_METADATA[company]['product-page-regex']);
        if (productPageDiv !== null) {
            processAbTest();
        }
        return false;
    }
    if (identifier === 'url') {
        const currentUrl = window.location.href;
        const urlRegex = CLIENT_METADATA[company]['product-page-regex'];
        if (currentUrl.indexOf(urlRegex) !== -1) {
            processAbTest();
        }
        return false;
    }
}

window.onload = isProductPage();
