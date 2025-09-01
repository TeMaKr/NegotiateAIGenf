/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // update collection data
  unmarshal({
    "indexes": [
      "CREATE UNIQUE INDEX `idx_vXcPPha` ON `submissions` (`href`) WHERE `href` != ''",
      "CREATE UNIQUE INDEX `idx_IwkzHEorw7` ON `submissions` (`retriever_id`)"
    ]
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // update collection data
  unmarshal({
    "indexes": [
      "CREATE UNIQUE INDEX `idx_vXcPPha` ON `submissions` (`href`) WHERE `href` != ''"
    ]
  }, collection)

  return app.save(collection)
})
