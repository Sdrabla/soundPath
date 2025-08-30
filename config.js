// Configuration file for SoundPath application
module.exports = {
  // MongoDB Connection
  MONGODB_URI: process.env.MONGODB_URI || 'mongodb://localhost:27017/soundpath',
  
  // JWT Secret Key
  JWT_SECRET: process.env.JWT_SECRET || 'your-super-secret-jwt-key-change-this-in-production',
  
  // Server Port
  PORT: process.env.PORT || 3000,
  
  // Session Secret
  SESSION_SECRET: process.env.SESSION_SECRET || 'your-session-secret-key',
  
  // Google OAuth Configuration
  GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID || 'your-google-client-id',
  GOOGLE_CLIENT_SECRET: process.env.GOOGLE_CLIENT_SECRET || 'your-google-client-secret',
  GOOGLE_REDIRECT_URI: process.env.GOOGLE_REDIRECT_URI || 'http://localhost:3000/auth/google/callback'
};
