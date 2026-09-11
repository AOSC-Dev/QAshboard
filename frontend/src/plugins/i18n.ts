import { createI18n } from "vue-i18n";

const messages = {
  en: {
    home: {
      title: "Home",
      links: {
        aoscIo: "Official website of AOSC",
        aoscPackages: "AOSC Packages website",
        aoscBuildIt: "AOSC BuildIt! building automation infrastructure",
      },
      allBuilds: "All builds",
    },
    stats: {
      title: "Stats",
      start: "Start",
      end: "End",
    },
    builds: {
      title: "Builds",
      columns: {
        package_name: "Package name",
        success: "Status",
        timestamp: "Time ({0})",
        architecture: "Architecture",
        buildbot: "Buildbot",
        failure_reason: "Failure reason",
      },
    },
  },
};

export default createI18n({
  legacy: false,
  locale: "en",
  fallbackLocale: "en",
  messages,
});
