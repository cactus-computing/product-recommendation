<template>
    <div id="main">
        <Header/>
        <div id="demo">    
            <div class="random-product text-center pt-8 inset-x-0 bottom-0 flex flex-col items-center">
                <Title/>
                <RandomProduct :random-product="random_product" @random-product = "setRandomProduct" />
                <RelatedProducts v-if="random_product" :random-product="random_product.name" />
            </div>
        </div>
        <FooterWithSitemap/>
    </div>
</template>

<script>
    import RandomProduct from './components/RandomProduct.vue'
    import Header from './components/Header.vue'
    import Footer from './components/Footer.vue'
    import RelatedProducts from './components/CactusRecommendations.vue'
    import Title from './components/Title.vue'

    export default {
        components: {
            RandomProduct,
            Header,
            Footer,
            RelatedProducts,
            Title,
        },
        data() {
            return {
                random_product: null,
            }
        },
        methods: {
            setRandomProduct(selected_product) {
                this.random_product = selected_product
            }        
        }
    }
</script>

<style>

</style>