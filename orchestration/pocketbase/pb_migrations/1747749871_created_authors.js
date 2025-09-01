/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = new Collection({
    "createRule": null,
    "deleteRule": null,
    "fields": [
      {
        "autogeneratePattern": "",
        "hidden": false,
        "id": "_clone_nMC1",
        "max": 0,
        "min": 0,
        "name": "author",
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
    "id": "pbc_4091785131",
    "indexes": [],
    "listRule": null,
    "name": "authors",
    "system": false,
    "type": "view",
    "updateRule": null,
    "viewQuery": "SELECT author, (ROW_NUMBER() OVER()) AS id FROM documents GROUP BY author",
    "viewRule": null
  });

  return app.save(collection);
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_4091785131");

  return app.delete(collection);
})
