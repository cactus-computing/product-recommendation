<template>
    <div v-if="random_product" class="random-product lg:container lg:mx-auto flex box-content justify-center p-8 flex-wrap">
        <div class="product-image">
                <img :src="random_product.img_url" class="shadow-lg object-scale-down h-64 w-64 rounded-md border-gray-900">
            </div>
        <div class="product-details-box flex flex-col items-start text-left justify-around  p-3">   
            <h1 :productName="random_product.name" class="text-3xl font-medium"> {{ random_product.name }} </h1> 
            <div class="product-details flex flex-col justify-center items-start pb-3">        
                <h4 class="text-xl pt-1"> Precio: {{ random_product.formatted_price }} </h4>
                <h4 v-if="random_product.stock_quantity" class="text-green-500 pt-1"> Hay existencias </h4>
                <h4 v-else class="text-red-500 pt-1"> Sin stock </h4>
            </div>
            <button @click="getRandomProduct" class="bg-blue-500 hover:bg-blue-600 shadow-md rounded text-white p-2">
                    Ver otro Producto
            </button>
        </div>
    </div>
</template>

<script>
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const client = urlParams.get('client')

    const type = 'random_product';
    export default {
        data() {
            return {
                random_product: null,
            }
        },
        mounted() {
            fetch(`http://dev.cactusco.cl/api/${type}?company=${client}`)
                .then(response => response.json())
                .then(data => this.random_product = data.selected_product);
        },
        methods: {
            getRandomProduct: function() {
                window.location.reload(true);
            }
        }
    }
</script>

<style>
#app {
    font-family: montserrat;
}
/*    #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
    }

    .random-product {
        display: flex;
        align-items: center;
        position:relative;
        justify-content: center;
    }

    .random-product img {
        height: 300px;
        width: 300px;
        object-fit: cover;
        box-sizing: border-box;
        border-radius: 10px;
        border-color: #ebebeb;
        border: 1px solid;
    }

    .product-details-box {
        margin-left: 30px;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: flex-start;
        text-align: left;
    }
*/
</style>
