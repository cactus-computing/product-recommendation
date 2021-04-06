<template>
    <div id="cactusContainer">
        <div class="up-sell slider" id="up-sell-slider">
            <div class="cross-sell title">
                <h2>Productos Recomendados</h2>
            </div>
            <div class="up-sell slide-box" id="up-sell-slide-box">
                <button class="up-sell ctrl-btn pro-prev"> > </button>
                <div class="up-sell slide" id="up-sell-slide">
                    <div v-for="related_product in related_products" :key="related_product.id" class="product">
                        <a :href="related_product.permalink">
                            <img :src="related_product.img_url" class="product-image">
                        </a>
                        <div class="product-name-box">
                            <a :href="related_product.permalink">
                                <h2 class="product-name">{{ related_product.name }}</h2>
                            </a>
                        </div>
                        <div class="product-price-box">
                            <span class="product-price">{{ related_product.price }}</span>
                        </div>
                    </div>
                </div>
                <button class="up-sell ctrl-btn pro-next"> > </button>
            </div>
        </div>
    </div>
</template>

<script>
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
// const productName = productName;
const client = urlParams.get("client");
const type = "up_sell";
const k = 30;

export default {
  data() {
    return {
      related_products: null,
    };
  },
  props: ['productName'],
  mounted() {
    fetch(`https://dev.cactusco.cl/api/${type}?name=${productName}&company=${client}&top-k=${k}`)
      .then((response) => response.json())
      .then((data) => (this.related_products = data.data));
  },
};
</script>

<style src='.././assets/styles/demo.css'> </style>

