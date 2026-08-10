import js from '@eslint/js';
import globals from 'globals';

// H6-B.2 lint layer (issue #64 item 6). Core-only flat config — no React
// plugin yet (tracked enhancement, recorded in DECISION_LOG). JSX is parsed
// natively; PascalCase vars are exempted from no-unused-vars because core
// ESLint cannot see JSX usage without the React plugin's jsx-uses-vars.
export default [
  { ignores: ['dist/', 'node_modules/'] },
  js.configs.recommended,
  {
    files: ['**/*.{js,jsx}'],
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: 'module',
      parserOptions: { ecmaFeatures: { jsx: true } },
      globals: { ...globals.browser },
    },
    rules: {
      'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z]' }],
    },
  },
];
