<template>
    <div class="flex flex-wrap justify-between items-center pb-12 md:pb-12 max-w-7xl mx-auto px-6 sm:px-6 lg:px-8">

        <div class="w-full md:w-5/12 lg:pr-10 lg:pl-4 text-justify md:text-left">
            <div class="relative flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white">
              <!-- Heroicon name: outline/globe-alt -->
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-3xl my-2 font-semibold leading-normal">
                Vistos recientemente
            </h3>
            <p class="text-lg font-light leading-relaxed mt-4 mb-4 text-gray-700">
            Una persona tiene que ver algo por lo menos <span class="font-semibold">7 veces</span> antes de decidirse a comprarlo.
            </p>
            <p class="text-lg font-light leading-relaxed mt-0 mb-4 text-gray-700">
            Nuestro carrusel trackea el recorrido de tus clientes en tu e-Commerce y muestra los productos a lo largo del ciclo de compra para <span class="font-semibold"> aumentar la probabilidad de conversión.</span>
            </p>
            <div class="mt-4 flex lg:mt-6 lg:flex-shrink-0">
            <a href="#contact" class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
                Empieza a recomendar
            </a>
            </div>
        </div>
        <div class="w-full md:w-7/12 lg:ml-0 ml-auto">
            <div class="relative flex flex-col mt-12 min-w-0 break-words bg-white w-full mb-3 ">
                <a href="https://protteina.com/products/beyond-meat-the-beyond-sausage-hot-italian">  
                    <img
                    alt="..."
                    src="/static/img/recently_viewed.webp"
                    class="relative w-full align-middle p-2 sm:p-6 md:p-0 lg:p-0 relative rounded-lg"
                    />
                </a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: "Feature2",
};
</script>

<style>
</style>