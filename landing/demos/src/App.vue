<template>
    <div>
        <Hero/>
        <Features/>
        <Features2/>
        <Pricing/>
        <Contact/>
        <Footer/>
        <router-view/> 
    </div>
</template>

<script>
    import Hero from './components/Hero.vue'
    import Footer from './components/Footer.vue'
    import Features from './components/Features.vue'
    import Features2 from './components/Features2.vue'
    import Cta from './components/Cta.vue'
    import Pricing from './components/Pricing.vue'
    import Contact from './components/Contact.vue'

    export default {
        components: {
            Hero,
            Footer,
            Features,
            Features2,
            Cta,
            Pricing,
            Contact,
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
  margin-top: 20px;
}
</style> 