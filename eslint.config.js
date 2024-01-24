import antfu from "@antfu/eslint-config";

export default antfu(
  {
    typescript: true,
    stylistic: {
      quotes: "double",
      semi: true,
    },
  },
  {
    rules: {
      "curly": ["error", "all"],
      "no-lone-blocks": "off",
      "style/brace-style": "off",
      "ts/brace-style": ["error", "1tbs"],
    },
  },
);
