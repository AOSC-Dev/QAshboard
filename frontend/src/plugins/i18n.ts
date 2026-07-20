import { createI18n } from "vue-i18n";

const messages = {
  en: {
    home: {
      title: "Home"
    },
    builds: {
      title: "Builds",
    },
  },
};

export default createI18n({
  legacy: false,
  locale: "en",
  fallbackLocale: "en",
  messages,
});
