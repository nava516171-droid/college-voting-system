module.exports = {
  webpack: (config) => {
    config.resolve.fallback = {
      ...(config.resolve.fallback || {}),
      fs: false,
      path: false,
      crypto: false,
    };
    return config;
  },
  devServer: (configFunction) => {
    return function (proxy, allowedHost) {
      const config = configFunction(proxy, allowedHost);
      return {
        ...config,
        host: '0.0.0.0',
        port: 3000,
        allowedHosts: 'all',
      };
    };
  },
};
