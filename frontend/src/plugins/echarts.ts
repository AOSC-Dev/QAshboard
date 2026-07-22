import type { App } from "vue";
import { registerPreprocessor } from "echarts/core";
import { THEME_KEY } from "vue-echarts";
import vuetify from "./vuetify";

registerPreprocessor((option) => {
  option.backgroundColor ??= "transparent";
});

export default {
  install(app: App) {
    app.provide(THEME_KEY, () =>
      vuetify.theme.global.current.value.dark ? "dark" : "default",
    );
  },
};
