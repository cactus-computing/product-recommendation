<template>
    <div>
        <Hero/>
        <Features/>
        <Pricing/>
        <Cta/>
        <Contact/>
        <Footer/>
    </div>
</template>

<script setup>
    import Hero from '../components/Hero.vue'
    import Footer from '../components/Footer.vue'
    import Features from '../components/Features.vue'
    import Cta from '../components/Cta.vue'
    import Pricing from '../components/Pricing.vue'
    import Contact from '../components/Contact.vue'
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
</style> 