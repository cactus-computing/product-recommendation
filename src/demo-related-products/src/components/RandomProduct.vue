<template>
    <div v-if="random_product" class="random-product lg:container lg:mx-auto flex box-content justify-center p-8">
        <div class="product-image p-4">
                <img :src="random_product.img_url" class="shadow-md object-scale-down h-64 w-64 rounded-md">
            </div>
        <div class="product-details-box flex flex-col items-start text-left justify-around  p-4 ">   
            <h1 class="text-3xl font-medium"> {{ random_product.name }} </h1> 
            <div class="product-details flex flex-col justify-center items-start">        
                <h4 class="text-xl"> Precio: {{ random_product.price }} </h4>
                <h4> SKU: {{ random_product.sku }} </h4>
            </div>
            <button class="bg-blue-500 hover:bg-blue-600 shadow-md rounded p-2 text-white">
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
