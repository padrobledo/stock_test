// helpers/random_string.js

// This function returns a random string for a given amount of characters

function randomString(length) {
    
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  let result = '';

  for (let i = 0; i < length; i++) {

    result += chars.charAt(Math.floor(Math.random() * chars.length));

  }
  
  return result;
}

module.exports = randomString;
