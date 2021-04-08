<template>
    <div v-if="store !== null" class="flex items-center flex-wrap justify-center">
        <h1 class="text-4xl font-medium m-3 "> Demo recomendaciones </h1>
        <div class="client-logo justify-self-center p-3 shadow-lg rounded bg-black opacity-75 w-30">
            <img class="h-8 w-auto sm:h-10 justify-self-center" :src="store.store_logo_url" alt="">
        </div>
    </div>
</template>

<script>
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const client = urlParams.get('client');
    const endpoint = 'get_store_detail';

    export default {    
        data() {
            return {
                store: null,
            };
        }, 
        mounted() {
            fetch(`https://production-cactus.herokuapp.com/api/${endpoint}?company=${client}`)
                .then(response => response.json())
                .then((data) => (this.store = data.store_data));
        }
    }

</script>

<style>

</style>
