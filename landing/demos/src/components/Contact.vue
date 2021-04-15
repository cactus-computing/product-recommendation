<template>
  <!-- component -->
<div id= "contact" class="relative flex items-top justify-center pb-12 bg-white dark:bg-gray-900 sm:items-center sm:pt-0">
        <div class="max-w-6xl mx-auto sm:px-6 lg:px-8">
            <div class="mt-8 overflow-hidden">
                <div class="grid grid-cols-1 md:grid-cols-2">
                    <div class="p-6 mr-2 bg-gray-50 dark:bg-gray-800 sm:rounded-lg">
                        <h2 class="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">
                            <span class="block">Convencido?</span>
                            <span class="block text-blue-600">Implementa Cactus hoy.</span>
                        </h2>
                        <div class="flex items-center ml-4 mt-12 text-gray-600 dark:text-gray-400">
                            <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" class="w-8 h-8 text-gray-500">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                            </svg>
                            <div class="ml-4 text-md tracking-wide font-semibold w-60">
                                Los Conquistadores 2461, Providencia, RM.
                            </div>
                        </div>

                        <div class="flex items-center ml-4 mt-4 text-gray-600 dark:text-gray-400">
                            <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" class="w-8 h-8 text-gray-500">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                            </svg>
                            <div class="ml-4 text-md tracking-wide font-semibold w-60">
                                +569 92991421
                            </div>
                        </div>

                        <div class="flex items-center ml-4 mt-4 text-gray-600 dark:text-gray-400">
                            <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" class="w-8 h-8 text-gray-500">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                            </svg>
                            <div class="ml-4 text-md tracking-wide font-semibold w-60">
                                hola@cactusco.cl
                            </div>
                        </div>
                    </div>

                    <form class="p-6 flex flex-col justify-center">
                        <div class="flex flex-col">
                            <label for="name" class="hidden">Full Name</label>
                            <input type="name" name="name" id="name" placeholder="Nombre" class="w-100 mt-2 py-3 px-3 rounded-md bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 font-medium focus:border-blue-500 focus:outline-none">
                        </div>

                        <div class="flex flex-col mt-2">
                            <label for="company" class="hidden">Company</label>
                            <input type="company" name="company" id="company" placeholder="Empresa" class="w-100 mt-2 py-3 px-3 rounded-md bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 font-medium focus:border-blue-500 focus:outline-none">
                        </div>

                        <div class="flex flex-col mt-2">
                            <label for="email" class="hidden">Email</label>
                            <input type="email" name="email" id="email" placeholder="Email" class="w-100 mt-2 py-3 px-3 rounded-md bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 font-medium focus:border-blue-500 focus:outline-none">
                        </div>

                        <div class="flex flex-col mt-2">
                            <label for="tel" class="hidden">Number</label>
                            <input type="tel" name="tel" id="tel" placeholder="Número de Teléfono" class="w-100 mt-2 py-3 px-3 rounded-md bg-white dark:bg-gray-800 border border-gray-400 dark:border-gray-700 text-gray-800 font-medium focus:border-blue-500 focus:outline-none">
                        </div>

                        <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-md mt-3 hover:bg-blue-50 transition ease-in-out duration-300">
                            Quiero un Demo
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Contact'
}
</script>

<style>
</style>