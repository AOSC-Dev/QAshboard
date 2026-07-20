<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
    <v-bottom-navigation>
      <v-btn to="/" exact>
        <v-icon icon="mdi-home" />
        <span>{{ $t("home.title") }}</span>
      </v-btn>
      <v-btn to="/builds">
        <v-icon icon="mdi-wrench" />
        <span>{{ $t("builds.title") }}</span>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
</template>
