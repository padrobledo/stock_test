// configuration/endpoints.js

// This file contains the endpoints used across the test suite

const endpoints = {
  auth: {
    register_credentials: '/auth/register_credentials',
    validate_credentials: '/auth/validate_credentials',
  },
  business: {
    create_new: '/business/create_new',
  },
  data: {
    get_client: '/data/get_client'
  },
  health: '/health',
};

module.exports = endpoints;
