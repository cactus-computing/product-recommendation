<template>
    <div v-if="related_products !== null" id="cactusContainer">
        <div class="up-sell slider" id="up-sell-slider">
            <div class="cross-sell title">
                <h2>Productos Recomendados</h2>
            </div>
            <div class="up-sell slide-box" id="up-sell-slide-box">
                <button @click="slideLeft" class="up-sell ctrl-btn pro-prev"> > </button>
                <div class="up-sell slide" id="up-sell-slide">
                    <div v-for="related_product in related_products" :key="related_product.id" class="product">
                        <a :href="related_product.permalink">
                            <img :src="related_product.img_url" class="product-image">
                        </a>
                        <div class="product-name-box">
                            <a :href="related_product.permalink">
                                <h2 class="product-name line-clamp-3">{{ related_product.name }}</h2>
                            </a>
                        </div>
                        <div class="product-price-box">
                            <span class="product-price">{{ related_product.price }}</span>
                        </div>
                    </div>
                </div>
                <button @click="slideRight" class="up-sell ctrl-btn pro-next"> > </button>
            </div>
        </div>
    </div>
</template>

<script>

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const client = urlParams.get("client");
const endpoint = "up_selling";
const k = 30;
const type= 'up-sell';
const width = 210; // product box + margin width
const visibleProductsWanted = 3;

export default {
  data() {
    return {
        related_products: null,
    };
  },
  props: ['randomProduct'],
  mounted() {
    fetch(`https://production-cactus.herokuapp.com/api/${endpoint}?name=${this.randomProduct}&company=${client}&top-k=${k}`)
        .then((response) => response.json())
        .then((data) => (
            this.related_products = data.data));
  },
  methods: {
        slideRight() {
            const slide = document.getElementById(`${type}-slide`);
            slide.scroll({ left: slide.scrollLeft += visibleProductsWanted * width });
        },
        slideLeft() {
            const slide = document.getElementById(`${type}-slide`);
            slide.scroll({ left: slide.scrollLeft -= visibleProductsWanted * width });
        }
    }
};

</script>

<style src='.././assets/styles/demo.css'> </style>

