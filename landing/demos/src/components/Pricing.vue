<template>
  <!-- component -->
  <div id="pricing" class="py-12 flex justify-center items-center bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ">
      <div class="text-center ">
        <h2 class="text-base text-cactus-green font-semibold tracking-wide uppercase">Precios</h2>
        <h1 class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
          <span>Planes a tu medida</span>
        </h1>
        <p class="px-8 mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
          Si no estas contento, contáctanos dentro de los primeros 14 días y te
          devolveremos lo pagado, sin preguntas.
        </p>
      </div>
      <div class="pt-6 flex flex-row flex-wrap justify-center">
        <!-- Basic Card -->
        <div class="w-80 p-8 m-4 bg-white text-center rounded-xl shadow-xl border-blue-600 border-2">
          <h1 class="text-black font-semibold text-2xl">Emprendedor</h1>
          <p class="pt-2 tracking-wide">
            <span class="text-gray-400 align-top">$ </span>
            <span class="text-2xl font-semibold line-through">1 UF</span>
            <span class="text-3xl font-semibold ">0,5 UF</span>
            <span class="text-gray-400 font-medium">/ mes</span>
          </p>
          <hr class="mt-4 border-1" />
          <div class="pt-8">
            <div class="flex justify-start">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#2563EB"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <p class="font-semibold text-gray-400 text-left">
                <span class="pl-2">
                  Hasta <span class="text-black">500 SKU's</span>
                </span>
              </p>
            </div>
            <div class="flex justify-start  pt-5">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#2563EB"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
                <p class="font-semibold text-gray-400 text-left">
                <span class="pl-2">
                    Máx <span class="text-black">5.000 sesiones</span> / mes
                </span>
                </p>
            </div>
            <div class="flex justify-start  pt-5">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#2563EB"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
                <p class="font-semibold text-gray-400 text-left">
                <span class="pl-2">
                    Página de<span class="text-black"> producto</span>
                </span>
                </p>
            </div>
                <a href="#contact" class="">
                <p class="w-full py-4 bg-blue-600 mt-8 rounded-xl text-white">
                    <span class="font-medium"> Quiero este Plan </span>
                </p>
                </a>
          </div>
        </div>
        <!-- StartUp Card
        <div
          class="w-80 p-8 m-4 bg-gray-900 text-center rounded-xl text-white shadow-2xl"
        >
          <h1 class="text-white font-semibold text-2xl">Startup</h1>
          <p class="pt-2 tracking-wide">
            <span class="text-gray-400 align-top">$ </span>
            <span class="text-3xl font-semibold">29.990</span>
            <span class="text-gray-400 font-medium">/ mes</span>
          </p>
          <hr class="mt-4 border-1 border-gray-600" />
          <div class="pt-8">
            <div class="flex justify-start">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#2563EB"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>    
                <p class="font-semibold text-gray-400 text-left">
                <span class="pl-2">
                    Hasta <span class="text-white">5.000 SKU's</span>
                </span>
                </p>
            </div>
            <div class="flex justify-start pt-5">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#2563EB"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
                <p class="font-semibold text-gray-400 text-left">
                <span class="pl-2">
                    <span class="text-white">100.000 sesiones</span> / mes
                </span>
                </p>
            </div>
            <div class="flex justify-start pt-5">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#2563EB"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
                <p class="font-semibold text-gray-400 text-left">
                <span class="pl-2">
                    <span class="text-white">Up, Cross y Vistos recientemente</span>
                </span>
                </p>
            </div>
                <a href="#contact" class="">
                <p class="w-full py-4 bg-blue-600 mt-8 rounded-xl text-white">
                    <span class="font-medium"> Quiero este Plan </span>
                </p>
                </a>
          </div>
        </div>
         -->
        <!-- Enterprise Card -->
        <div class="w-80 p-8 m-4 bg-white text-center rounded-xl shadow-xl border-blue-600 border-2">
          <h1 class="text-black font-semibold text-2xl">Gran Empresa</h1>
          <p class="pt-2 tracking-wide">
            <span class="text-2xl font-semibold text-blue-600">Contáctanos </span>
          </p>
          <hr class="mt-4 border-1" />
          <div class="pt-8">
              <div class="flex justify-start">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#2563EB"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
                <p class="font-semibold text-gray-400 text-left">
            
                <span class="pl-2">
                    SKU's <span class="text-black">ilimitados</span>
                </span>
                </p>
              </div>
              <div class="flex justify-start pt-5">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#2563EB"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
                <p class="font-semibold text-gray-400 text-left">
                <span class="pl-2">
                    Sesiones <span class="text-black">ilimitadas</span>
                </span>
                </p>
            </div>
            <div class="flex justify-start pt-5">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="#2563EB"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    >
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                    <p class="font-semibold text-gray-400 text-left">
                    <span class="pl-2">
                        Página de<span class="text-black"> producto, <br>home, mail, checkout</span>
                    </span>
                    </p>
            </div>
            <a href="#contact" class="">
              <p class="w-full py-4 bg-blue-600 mt-8 rounded-xl text-white">
                <span class="font-medium bottom-0"> Quiero este Plan </span>
              </p>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Pricing",
};
</script>

<style>
</style>
