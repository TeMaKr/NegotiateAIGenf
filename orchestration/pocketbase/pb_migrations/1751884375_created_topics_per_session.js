/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = new Collection({
    "createRule": null,
    "deleteRule": null,
    "fields": [
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
    "id": "pbc_771152906",
    "indexes": [],
    "listRule": null,
    "name": "topics_per_session",
    "system": false,
    "type": "view",
    "updateRule": null,
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id from submissions group by topic",
    "viewRule": null
  });

  return app.save(collection);
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_771152906");

  return app.delete(collection);
})
