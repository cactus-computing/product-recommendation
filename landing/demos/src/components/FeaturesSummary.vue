<template>
  <!-- This example requires Tailwind CSS v2.0+ -->
<div id="" class="py-12 bg-gray-50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="lg:text-center">
        <h2 class="text-base text-cactus-green font-semibold tracking-wide uppercase">Resultados</h2>
        <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Aumenta las ventas hasta en un 8%
        </p>
        <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Mejorará a medida que el algoritmo aprenda de las interacciones de los usuarios.
        </p>
    </div>

    <div class="mt-10">
      <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-4 md:gap-x-10 md:gap-y-10 text-left">
        <div class="relative mr-4 sm:mr-0 flex flex-col items-start">
          <dt class="flex items-center justify-start">
            <div class="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white">
              <!-- Heroicon name: outline/globe-alt -->
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
            </div>
            <p class="text-lg leading-6 font-bold text-gray-900 text-left ml-2">Ticket Promedio</p>
          </dt>
          <dd class="mt-2 text-base text-gray-500">
               Usuarios que hacen click en nuestras recomendaciones <span class="font-semibold text-gray-900">compran un 30% más </span>por cada pedido.
          </dd>
        </div>

        <div class="relative mr-4 sm:mr-0 flex flex-col items-start">
          <dt class="flex items-center justify-start">
            <div class="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white ">
              <!-- Heroicon name: outline/scale -->
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
            </div>
            <p class="text-lg leading-6 font-bold text-gray-900 text-left ml-2">Tiempo sesión</p>
          </dt>
          <dd class="mt-2 text-base text-gray-500">
            Usuarios que hacen click en nuestras recomendaciones navegan <span class="font-semibold text-gray-900">hasta 3 veces </span> mas tiempo por tu página.
          </dd>
        </div>

        <div class="relative mr-4 sm:mr-0 flex flex-col items-start">
          <dt class="flex items-center justify-start">
            <div class="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white">
              <!-- Heroicon name: outline/lightning-bolt -->
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 2v6h6M2.66 15.57a10 10 0 1 0 .57-8.38"/></svg>
            </div>
            <p class="text-lg leading-6 font-bold text-gray-900 text-left ml-2">Rebote</p>
          </dt>
          <dd class="mt-2 text-base text-gray-500">
            Nuestros clientes han visto reducido en <span class="font-semibold text-gray-900">un 14% la tasa de rebote </span>en páginas de producto.
          </dd>
        </div>

        <div class="relative mr-4 sm:mr-0 flex flex-col items-start">
          <dt class="flex items-center justify-start">
            <div class="flex items-center justify-center h-12 w-12 rounded-md bg-blue-600 text-white">
              <!-- Heroicon name: outline/annotation -->
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.2 7.8l-7.7 7.7-4-4-5.7 5.7"/><path d="M15 7h6v6"/></svg>
            </div>
            <p class="text-lg leading-6 font-bold text-gray-900 ml-2">Conversión</p>
          </dt>
          <dd class="mt-2 text-base text-gray-500">
            Usuarios que hacen click en nuestras recomendaciónes <span class="font-semibold text-gray-900">convierten un 19% más.</span>
          </dd>
        </div>
      </dl>
    </div>
  </div>
</div>

</template>

<script>
export default {
    name: 'FeaturesSummary',
}
</script>

<style>
</style>