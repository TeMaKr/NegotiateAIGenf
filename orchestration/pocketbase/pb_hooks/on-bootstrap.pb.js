/// <reference path="../pb_data/types.d.ts" />

onBootstrap((e) => {
  e.next();

  /* configure app */
  // set metadata
  e.app.settings().meta.appName =
    $os.getenv("META_APP_NAME") || "Negotiate-AI";
  e.app.settings().meta.appURL =
    $os.getenv("META_APP_URL") || "http://localhost:3000";
  e.app.settings().meta.hideControls =
    $os.getenv("META_HIDE_CONTROLS") === "1" ? true : false;
  e.app.settings().meta.senderAddress = "noreply@and-effect-hosting.de";
  e.app.settings().meta.senderName =
    $os.getenv("META_SENDER_NAME") || "Negotiate-AI";

  // set smtp settings
  e.app.settings().smtp.enabled =
    $os.getenv("SMTP_ENABLED") === "1" ? true : false;
  e.app.settings().smtp.host = $os.getenv("SMTP_HOST");
  e.app.settings().smtp.port = $os.getenv("SMTP_PORT") || 587;
  e.app.settings().smtp.username = $os.getenv("SMTP_USER");
  e.app.settings().smtp.password = $os.getenv("SMTP_PASSWORD");
  e.app.settings().smtp.authMethod = "LOGIN";
  e.app.settings().smtp.tls = true;
  

  // set batch settings
  e.app.settings().batch.enabled = true;
  e.app.settings().batch.maxRequests = 50;
  e.app.settings().batch.timeout = 3;

});
 