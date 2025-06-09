const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    https: true,
    host: '0.0.0.0',
    port: 8080,
    allowedHosts: 'all',
    client: {
      webSocketURL: 'wss://crypto-stock-exchange.com/ws',
    },
    proxy: {
      '/api': {
        target: 'http://backend:5000',
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
      },
    },
  },
})
