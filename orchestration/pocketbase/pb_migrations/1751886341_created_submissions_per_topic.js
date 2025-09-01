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
      },
      {
        "hidden": false,
        "id": "json525672509",
        "maxSize": 1,
        "name": "topic_id",
        "presentable": false,
        "required": false,
        "system": false,
        "type": "json"
      },
      {
        "hidden": false,
        "id": "number1073325736",
        "max": null,
        "min": null,
        "name": "submissions_count",
        "onlyInt": false,
        "presentable": false,
        "required": false,
        "system": false,
        "type": "number"
      }
    ],
    "id": "pbc_1469303883",
    "indexes": [],
    "listRule": null,
    "name": "submissions_per_topic",
    "system": false,
    "type": "view",
    "updateRule": null,
    "viewQuery": "SELECT (ROW_NUMBER() OVER()) as id, json_extract(value, '$') as topic_id, COUNT(*) as submissions_count\nFROM submissions, json_each(submissions.topic)\nGROUP BY topic_id",
    "viewRule": null
  });

  return app.save(collection);
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1469303883");

  return app.delete(collection);
})
