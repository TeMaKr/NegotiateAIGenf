/// <reference path="../pb_data/types.d.ts" />

module.exports = Object.freeze({
  settings: function () {
    const settings = {};

    // configure API
    settings["api"] = {
      host: $os.getenv("API_FASTAPI_API__HOST") || "http://localhost:8000",
      token: $os.getenv("API_FASTAPI_API__TOKEN"),
    };

    settings["pocketbase"] = {
      host:
        $os.getenv("API_POCKETBASE_API__HOST") ||
        "http://host.docker.internal:8090",
      token: $os.getenv("API_POCKETBASE_API__TOKEN"),
    };

    return settings;
  },
});
