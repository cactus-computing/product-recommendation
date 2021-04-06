<template>
    <div id="main">
        <Header/>
        <div id="demo">    
            <div class="random-product text-center pt-8 inset-x-0 bottom-0 flex flex-col items-center">
                <h1 class="text-4xl font-medium"> Demo recomendaciones </h1>
                <div class="client-logo justify-self-center bg-black bg-opacity-75">
                    <img class="h-8 w-auto sm:h-10 justify-self-center" src="https://d1mm7fnxb6z2bq.cloudfront.net/static/img/logos/footer_logo.png" alt="">
                </div>
                <RandomProduct/>
                <RelatedProducts/>
            </div>
        </div>
        <FooterWithSitemap/>
    </div>
</template>

<script>
    import RandomProduct from './components/RandomProduct.vue'
    import Header from './components/Header.vue'
    import FooterWithSitemap from './components/Footer.vue'
    import RelatedProducts from './components/CactusRecommendations.vue'

    export default {
        components: {
            RandomProduct,
            Header,
            FooterWithSitemap,
            RelatedProducts
        }
    }
</script>

<style>

</style>