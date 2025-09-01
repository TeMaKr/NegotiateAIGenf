/// <reference path="../pb_data/types.d.ts" />

// fires only for "users" and "articles" collections
onCollectionAfterCreateSuccess((e) => {
  let collection = $app.findCollectionByNameOrId("api_tokens");
  let record = new Record(collection);
  const config = require(`${__hooks}/config.js`);
  const settings = config.settings();

  record.set("value", settings.pocketbase.token);

  $app.save(record);

  e.next();
}, "api_tokens");
