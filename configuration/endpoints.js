// configuration/endpoints.js

// This file contains the endpoints used across the test suite

const endpoints = {
  auth: {
    register_new_client: '/auth/register_credentials',
    validate_user_credentials: '/auth/validate_credentials',
  },
  business: {
    create_new: '/business/create_new',
  },
  health: '/health',
};

module.exports = endpoints;
