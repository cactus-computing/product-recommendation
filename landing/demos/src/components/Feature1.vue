<template>
    <div class="flex flex-wrap justify-between items-center py-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="w-full md:w-7/12 lg:ml-0">
            <div class="relative flex flex-col mt-12 min-w-0 break-words bg-white w-full mb-3 ">
                    <img
                    alt="..."
                    src="https://www.cactusco.cl/static/img/up_y_cross_sells.png"
                    class="relative w-full align-middle p-2 sm:p-6 md:p-0 lg:p-0 relative rounded-lg"
                    />
            </div>
        </div>
        <div class="w-full md:w-5/12 lg:pl-10 lg:pr-4 text-right flex flex-col items-center md:items-end">
            <div class="relative flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white">
              <!-- Heroicon name: outline/globe-alt -->
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-3xl my-2 font-semibold leading-normal">
                Siempre hay algo más que comprar
            </h3>
            <p class="text-lg font-light leading-relaxed mt-4 mb-4 text-gray-700">
                El carrusel de up-sells ofrece <span class="font-medium">productos similares</span> al que el cliente estaba buscando así tiene mas variedad para escoger, <span class="font-medium">todo en el mismo lugar.</span>
            </p>
            <p class="text-lg font-light leading-relaxed mt-0 mb-4 text-gray-700">
                El carrusel de cross-sells muestra <span class="font-medium">productos relacionados</span> al que el cliente buscó asi puede complementar su compra y llevar todo lo que necesita <span class="font-medium">(o no).</span>
            </p>
            <div class="mt-4 flex lg:mt-6 lg:flex-shrink-0">
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