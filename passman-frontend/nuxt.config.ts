// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  ssr: false,
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  runtimeConfig: {
    public: {
      apiURL: process.env.API_URL || 'http://localhost:8000/api',
    },
  },
  tailwindcss: {
    exposeConfig: true,
    viewer: true,
    cssPath: '~/assets/css/input.css'
  }
})
