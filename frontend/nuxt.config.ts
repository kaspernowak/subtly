// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  typescript: {
    typeCheck: true
  },
  devtools: { enabled: true },
  modules: ['@nuxt/ui', '@nuxt/eslint', '@pinia/nuxt'],
  css: ['~/assets/css/main.css'],
  
  // Runtime config
  runtimeConfig: {
    // Private keys are only available on the server
    apiSecret: process.env.API_SECRET,

    // Public keys that are exposed to the client
    public: {
      apiUrl: process.env.API_URL || 'http://localhost:8000'
    }
  },

  // Hybrid rendering setup
  routeRules: {
    // Generated at build time for SEO purpose
    '/': { prerender: true },
    // Public pages - SSR with cache
    '/about': { swr: 3600 },

    // Auth required pages - CSR only
    '/login': { ssr: false },
    '/register': { ssr: false },
    '/dashboard/**': { ssr: false },
    '/translate/**': { ssr: false },
    '/profile/**': { ssr: false },

    // Admin section - CSR only
    '/admin/**': { ssr: false },

    // API proxy rules
    '/api/v1/**': {
      proxy: process.env.API_URL || 'http://localhost:8000'
    }
  },

  // Nitro config for API proxy
  nitro: {
    devProxy: {
      '/api/v1': {
        target: process.env.API_URL || 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },

  future: {
    compatibilityVersion: 4
  },
  compatibilityDate: '2024-12-12'
})