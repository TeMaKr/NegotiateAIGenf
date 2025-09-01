/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1609645464");

  return app.delete(collection);
}, (app) => {
  const collection = new Collection({
    "createRule": null,
    "deleteRule": null,
    "fields": [
      {
        "autogeneratePattern": "",
        "hidden": false,
        "id": "_clone_rtYT",
        "max": 0,
        "min": 0,
        "name": "draft_categories",
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
    "id": "pbc_1609645464",
    "indexes": [],
    "listRule": "",
    "name": "draft_categories",
    "system": false,
    "type": "view",
    "updateRule": null,
    "viewQuery": "SELECT draft_categories, (ROW_NUMBER() OVER()) AS id FROM documents GROUP BY draft_categories",
    "viewRule": null
  });

  return app.save(collection);
})
