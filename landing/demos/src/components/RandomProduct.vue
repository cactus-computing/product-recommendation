<template>
    <div v-if="randomProduct" class="random-product lg:container lg:mx-auto flex box-content justify-center p-3 flex-wrap">
        <div class="product-image">
                <img :src="randomProduct.img_url" class="shadow-lg object-scale-down h-64 w-64 rounded-md border-gray-900">
            </div>
        <div class="product-details-box flex flex-col items-start text-left justify-around  p-3">   
            <h1 class="text-3xl font-medium line-clamp-2 max-w-xl"> {{ randomProduct.name }} </h1> 
            <div class="product-details flex flex-col justify-center items-start pb-3">        
                <h4 class="text-xl pt-1"> Precio: {{ randomProduct.formatted_price }} </h4>
                <h4 v-if="randomProduct.stock_quantity" class="text-green-500 pt-1"> Hay existencias </h4>
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
        props: {randomProduct: {
                type: Object,
                default: null
                }   
            },         
        mounted() {
            fetch(`https://production-cactus.herokuapp.com/api/${type}?company=${client}`)
                .then(response => response.json())
                .then(data => {this.$emit('random-product',data.selected_product)}); 
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
</style>
