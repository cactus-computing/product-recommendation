<template>

<!-- This example requires Tailwind CSS v2.0+ -->
<div class="relative bg-white overflow-hidden">
    <div class="relative pt-6 px-6 sm:px-6 lg:pl-8 lg:pr-4 max-w-7xl mx-auto  ">
        <nav class="relative flex items-center justify-between sm:h-10" aria-label="Global">
          <div class="flex items-center flex-grow flex-shrink-0 lg:flex-grow-0">
            <div class="flex items-center justify-between w-full md:w-auto pl-4">
              <a href="#">
                <span class="sr-only">Workflow</span>
                <img class="h-7 w-auto sm:h-7" src="/static/img/imagotipo_cactus.webp">
              </a>
              <div class="-mr-2 flex items-center md:hidden">
                <button @click="isHeaderVisible = !isHeaderVisible" type="button" class="bg-white rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500" aria-expanded="false">
                  <span class="sr-only">Abrir menú principal</span>
                  <!-- Heroicon name: outline/menu -->
                  <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <div class="hidden flex justify-between md:block md:ml-3 md:pr-12 md:space-x-8">
            <a href="#features" class="font-medium text-gray-500 hover:text-gray-900">Productos</a>
            <a href="#how-it-works" class="font-medium text-gray-500 hover:text-gray-900">Como funciona</a>
            <a href="#pricing" class="font-medium text-gray-500 hover:text-gray-900">Precios</a>
            <a href="#contact" class="font-semibold text-blue-600 hover:text-blue-500">Contáctanos</a>
          </div>
        </nav>
    </div>

    <div v-show="isHeaderVisible" class="absolute top-0 inset-x-0 p-2 transition transform origin-top-right md:hidden z-10">
    <div class="rounded-lg shadow-md bg-white ring-1 ring-black ring-opacity-5 overflow-hidden">
        <div class="px-5 pt-4 flex items-center justify-between">
        <div>
            <img class="h-6 w-auto" src="/static/img/imagotipo_cactus.webp" alt="">
        </div>
        <div class="-mr-2">
            <button @click="isHeaderVisible = !isHeaderVisible" type="button" class="bg-white rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500">
            <span class="sr-only">Close main menu</span>
            <!-- Heroicon name: outline/x -->
            <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            </button>
        </div>
        </div>
        <div class="px-2 pt-2 pb-3 space-y-1 z-10">
        <a href="#features" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50">Productos</a>

        <a href="#how-it-works" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50">Como funciona</a>

        <a href="#pricing" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50">Precios</a>

        </div>
        <a href="#contact" class="block w-full px-5 py-3 text-center font-medium text-blue-600 bg-gray-50 hover:bg-gray-100">
        Contáctanos
        </a>
    </div>
    </div>
    <div class="flex flex-wrap max-w-7xl mx-auto px-6 sm:px-4 lg:px-4">
        <div class="max-w-7xl order-2 lg:order-1">
            <div class="relative z-10 pb-8 bg-white sm:pb-16 md:pb-10 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
                <main class="mt-10 max-w-7xl sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
                    <div class="text-left flex flex-col items-start justify-start">
                        <h1 class="text-3xl tracking-tight font-extrabold text-gray-900 sm:text-4xl md:text-5xl sm:max-w-xl ">
                            <span class="block xl:inline">Recomienda productos a tus clientes.</span>
                            <span class="block text-cactus-green">Aumenta las ventas de tu e-Commerce, hoy.</span>
                        </h1>
                        <p class="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl  md:mt-5 md:text-xl lg:mx-0">
                            Instala Cactus en 5 minutos y comienza a entregar recomendaciones optimizadas para que tus clientes compren más.
                        </p>
                        <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                            <div class="rounded-md shadow">
                                <a href="#contact" class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10">
                                    Empieza a recomendar
                                </a>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </div>
        <div class="md:py-12 md:mt-12 lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2 order-1 lg:order-2">
            <img class="h-72 sm:p-0 w-full object-contain sm:h-72 md:h-96 sm:object-scale-down lg:w-full lg:h-full" src="/static/img/hero_illustration_man.webp" alt="">
        </div>
    </div>
</div>


</template>

<script>
export default {
    name: "Hero",
    data() {
        return {
            isHeaderVisible: false
        }
    }
}
</script>