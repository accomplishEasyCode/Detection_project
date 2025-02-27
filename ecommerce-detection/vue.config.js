module.exports = {
  devServer: {
    allowedHosts: 'all',
    proxy: {
      '/api': {
        target: 'http://192.168.222.35:5000', // 后端服务地址
        changeOrigin: true, // 必须设置为 true，支持跨域
        // pathRewrite: { '^/api': '/api' }, // 保证路径正确
      },
    },
    client: {
      overlay: false
    }
  },
};
