/// <reference path="../pb_data/types.d.ts" />
// import data from "..data/draft_categories.json"
migrate((app) => {
  // const fs = require("fs");
  // const path = require("path");

  // const jsonPath= path.join(__dirname, "..data/draft_categories.json");


    // const jsonData = fs.readFileSync(jsonPath, "utf8");
  //   // const draftCategories = JSON.parse(jsonData);
  // const concepts = data.map(item => item.concept);

  const collection = new Collection({
    "createRule": null,
    "deleteRule": null,
    "fields": [
      {
        "autogeneratePattern": "[a-z0-9]{15}",
        "hidden": false,
        "id": "text3208210256",
        "max": 15,
        "min": 15,
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
        "id": "text724990059",
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
        "autogeneratePattern": "",
        "hidden": false,
        "id": "text1843675174",
        "max": 0,
        "min": 0,
        "name": "description",
        "pattern": "",
        "presentable": false,
        "primaryKey": false,
        "required": false,
        "system": false,
        "type": "text"
      },
      {
        "cascadeDelete": false,
        "collectionId": "pbc_526341563",
        "hidden": false,
        "id": "relation3182418120",
        "maxSelect": 999,
        "minSelect": 0,
        "name": "author",
        "presentable": false,
        "required": false,
        "system": false,
        "type": "relation"
      },
      {
        "hidden": false,
        "id": "select2765332939",
        "maxSelect": 2,
        "name": "draft_category",
        "presentable": false,
        "required": false,
        "system": false,
        "type": "select",
        "values": [
          "Production/Supply",
          "Plastic products & Chemicals of concern",
          "Plastic Product design",
        ]
      },
      {
        "exceptDomains": null,
        "hidden": false,
        "id": "url888727361",
        "name": "href",
        "onlyDomains": null,
        "presentable": false,
        "required": false,
        "system": false,
        "type": "url"
      },
      {
        "autogeneratePattern": "",
        "hidden": false,
        "id": "text3494172116",
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
        "hidden": false,
        "id": "autodate2990389176",
        "name": "created",
        "onCreate": true,
        "onUpdate": false,
        "presentable": false,
        "system": false,
        "type": "autodate"
      },
      {
        "hidden": false,
        "id": "autodate3332085495",
        "name": "updated",
        "onCreate": true,
        "onUpdate": true,
        "presentable": false,
        "system": false,
        "type": "autodate"
      }
    ],
    "id": "pbc_1225573716",
    "indexes": [],
    "listRule": null,
    "name": "Submissions",
    "system": false,
    "type": "base",
    "updateRule": null,
    "viewRule": null
  });

  return app.save(collection);
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716");

  return app.delete(collection);
})