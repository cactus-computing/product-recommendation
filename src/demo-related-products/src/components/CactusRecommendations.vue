<template>
    <div id="cactusContainer">
        <div class="cross-sell slider" id="cross-sell-slider">
            <div class="cross-sell title">
                <h2>Productos Relacionados</h2>
            </div>
            <div class="cross-sell slide-box" id="cross-sell-slide-box">
                <button class="cross-sell ctrl-btn pro-prev">  </button>
                <div class="cross-sell slide" id="cross-sell-slide">
                <button class="cross-sell ctrl-btn pro-next"> > </button>
        <div class="up-sell slider" id="up-sell-slider">
            <div class="cross-sell title">
                <h2>Productos Relacionados</h2>
            </div>
            <div class="up-sell slide-box" id="up-sell-slide-box">
                <button class="up-sell ctrl-btn pro-prev">  </button>
                <div class="up-sell slide" id="up-sell-slide">
                <button class="up-sell ctrl-btn pro-next"> > </button>
    </div>
</template>

<script>
    const client = 'quema';
    const type = 'random_product';
    export default {
        data() {
            return {
                random_product: null,
            }
        },
        mounted() {
            fetch(`https://dev.cactusco.cl/api/${type}?company=${client}`)
                .then(response => response.json())
                .then(data => this.random_product = data.selected_product);
        },
    }
</script>

<style>
    #app {
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
    }
</style>
