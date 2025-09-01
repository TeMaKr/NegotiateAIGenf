/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1380977566");

  return app.delete(collection);
}, (app) => {
  const collection = new Collection({
    "createRule": null,
    "deleteRule": null,
    "fields": [
      {
        "autogeneratePattern": "",
        "hidden": false,
        "id": "_clone_7r79",
        "max": 0,
        "min": 0,
        "name": "verified",
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
    "id": "pbc_1380977566",
    "indexes": [],
    "listRule": "",
    "name": "verified",
    "system": false,
    "type": "view",
    "updateRule": null,
    "viewQuery": "SELECT verified, (ROW_NUMBER() OVER()) AS id FROM documents GROUP BY verified",
    "viewRule": null
  });

  return app.save(collection);
})
