<template>
    <div class="flex flex-wrap justify-between items-center pb-12 max-w-7xl mx-auto px-6 sm:px-6 lg:px-8">
        <div class="w-full md:w-6/12 lg:ml-0">
            <div class="relative flex flex-col mt-12 min-w-0 break-words bg-white w-full mb-3 ">
                    <img
                    alt="..."
                    src="static/img/carousel_emailing.webp"
                    class="relative w-full align-middle sm:p-6 md:p-0 lg:p-0 relative rounded-lg"
                    />
            </div>
        </div>
        <div class="w-full md:w-5/12 lg:pl-10 lg:pr-4 text-left md:text-right flex flex-col items-start md:items-end order-first md:order-last">
            <div class="relative flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white">
              <!-- Heroicon name: outline/globe-alt -->
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-3xl mt-2 font-semibold leading-normal">
                Emailings
            </h3>
            <p class="text-lg font-light leading-relaxed mt-2 sm:mb-4 text-gray-700">
                <span class="font-semibold">Personalizamos y automatizamos </span> tus campañas de emailing para ofrecer a cada cliente un mix único de productos. El diseño lo escoges tu, de <span class="font-semibold">todo lo demas se encarga Cactus</span> 
            </p>
            <div class="hidden sm:list-item mt-4 flex lg:mt-6 lg:flex-shrink-0">
                <a href="#contact" class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
                    Empieza a recomendar
                </a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: "Feature1",
};
</script>

<style>
</style>