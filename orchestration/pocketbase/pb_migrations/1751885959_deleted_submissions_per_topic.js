/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883");

  return app.delete(collection);
}, (app) => {
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
      },
      {
        "autogeneratePattern": "",
        "hidden": false,
        "id": "_clone_RDQE",
        "max": 0,
        "min": 0,
        "name": "title",
        "pattern": "",
        "presentable": false,
        "primaryKey": false,
        "required": false,
        "system": false,
        "type": "text"
      },
      {
        "cascadeDelete": false,
        "collectionId": "pbc_2800040823",
        "hidden": false,
        "id": "_clone_9A2k",
        "maxSelect": 999,
        "minSelect": 0,
        "name": "topic",
        "presentable": false,
        "required": false,
        "system": false,
        "type": "relation"
      }
    ],
    "id": "pbc_1469303883",
    "indexes": [],
    "listRule": null,
    "name": "submissions_per_topic",
    "system": false,
    "type": "view",
    "updateRule": null,
    "viewQuery": "SELECT s.id, s.title, s.topic FROM submissions as s, json_each(topic) as topic_value",
    "viewRule": null
  });

  return app.save(collection);
})
