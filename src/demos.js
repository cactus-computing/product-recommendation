let app = new Vue({
    el: '#app',
    data: {
        company: 'prat',
        company_script: 'http://localhost:8000/static/js/cactusFront.js?client=agustin&environment=prod',
        products: [
            {
                sku: 'ABE000014',
                name: 'ABECEDARIO GOLPE 4 MM',
                img_url: 'https://www.ferreteriaprat.cl/media/catalog/product/cache/1/image/1200x1200/9df78eab33525d08d6e5fb8d27136e95/a/b/abe000014.jpg',
                price: 44710,
                url: 'https://www.ferreteriaprat.cl/abecedario-golpe-4-mm.html',
                stock: true,
            },
            {
                sku: 'PAS118975',
                name: 'Iris Pasta Muro Tr-15 24kg',
                img_url: 'https://www.ferreteriaprat.cl/media/catalog/product/cache/1/small_image/960x960/9df78eab33525d08d6e5fb8d27136e95/P/A/PAS118975_19.jpg',
                price: 10536,
                url: 'https://www.ferreteriaprat.cl/iris-pasta-muro-tr-15-24kg.html',
                stock: true,
            },
        ],
    },
});
