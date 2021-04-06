<template>
    <div id="main">
        <Header/>
        <div id="demo">    
            <div class="random-product text-center pt-8 inset-x-0 bottom-0">
                <h1 class="pt-8 text-4xl font-medium"> Demo productos relacionados </h1>
                <RandomProduct/>
            </div>
        </div>
        <FooterWithSitemap/>
    </div>
</template>

<script>
    import RandomProduct from './components/RandomProduct.vue'
    import Header from './components/Header.vue'
    import FooterWithSitemap from './components/Footer.vue'

    export default {
        components: {
            RandomProduct,
            Header,
            FooterWithSitemap,
        }
    }
</script>

<style>

</style>