<template>
    <div>
        <Hero/>
        <LogoCloud/>
        <FeaturesSummary/>
        <FeatureTitle/>
        <Feature1/>
        <Feature2/>
        <HowItWorks/>
        <Pricing/>
        <Contact/>
        <Footer/>
        <router-view/> 
    </div>
</template>

<script>
    import Hero from './components/Hero.vue'
    import Footer from './components/Footer.vue'
    import FeatureTitle from './components/FeatureTitle.vue'
    import Feature1 from './components/Feature1.vue'
    import Feature2 from './components/Feature2.vue'
    import FeaturesSummary from './components/FeaturesSummary.vue'
    import HowItWorks from './components/HowItWorks.vue'
    import Cta from './components/Cta.vue'
    import Pricing from './components/Pricing.vue'
    import Contact from './components/Contact.vue' 
    import LogoCloud from './components/LogoCloud.vue'

    export default {
        components: {
            Hero,
            Footer,
            FeatureTitle,
            Feature1,
            Feature2,
            FeaturesSummary,
            HowItWorks,
            Cta,
            Pricing,
            Contact,
            LogoCloud,
        },
    }
</script>

<style>

html {
  scroll-behavior: smooth;
}

#app {
  font-family: montserrat;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}


@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

</style> 