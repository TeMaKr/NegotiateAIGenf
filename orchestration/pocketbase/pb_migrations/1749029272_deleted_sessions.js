/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_3346360724");

  return app.delete(collection);
}, (app) => {
  const collection = new Collection({
    "createRule": null,
    "deleteRule": null,
    "fields": [
      {
        "autogeneratePattern": "",
        "hidden": false,
        "id": "_clone_1Epu",
        "max": 0,
        "min": 0,
        "name": "session",
        "pattern": "",
        "presentable": false,
        "primaryKey": false,
        "required": false,
        "system": false,
        "type": "text"
      },
      {
        "autogeneratePattern": "",
        "hidden": false,
        "id": "text3208210256",
        "max": 0,
        "min": 0,
        "name": "id",
        "pattern": "^[a-z0-9]+$",
        "presentable": false,
        "primaryKey": true,
        "required": true,
        "system": true,
        "type": "text"
      }
    ],
    "id": "pbc_3346360724",
    "indexes": [],
    "listRule": "",
    "name": "sessions",
    "system": false,
    "type": "view",
    "updateRule": null,
    "viewQuery": "SELECT session, (ROW_NUMBER() OVER()) AS id FROM documents GROUP BY session",
    "viewRule": null
  });

  return app.save(collection);
})
