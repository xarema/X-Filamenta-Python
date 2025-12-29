import js from "@eslint/js";
import globals from "globals";

export default [
  { ignores: [".venv/**", "coverage/**", "**/node_modules/**"] },
  js.configs.recommended,
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
        htmx: "readonly",
        Tabulator: "readonly",
        module: "writable",
      },
      ecmaVersion: "latest",
      sourceType: "module",
    },
    rules: {
      "no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
      "no-console": "warn",
      eqeqeq: ["error", "always"],
    },
  },
];
