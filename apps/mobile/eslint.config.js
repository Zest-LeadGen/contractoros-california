import js from '@eslint/js';
import globals from 'globals';

// H6-B.2 lint layer (issue #64 item 6). Core-only flat config — see the web
// config's rationale; __DEV__ is the React Native debug global.
export default [
  { ignores: ['node_modules/', '.expo/'] },
  js.configs.recommended,
  {
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: 'module',
      parserOptions: { ecmaFeatures: { jsx: true } },
      globals: { ...globals.node, __DEV__: 'readonly' },
    },
    rules: {
      'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z]' }],
    },
  },
];
