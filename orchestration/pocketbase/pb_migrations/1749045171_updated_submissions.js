/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // update collection data
  unmarshal({
    "indexes": [
      "CREATE UNIQUE INDEX `idx_NTMjf679hJ` ON `submissions` (`href`)"
    ]
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // update collection data
  unmarshal({
    "indexes": [
      "CREATE INDEX `idx_NTMjf679hJ` ON `submissions` (`href`)"
    ]
  }, collection)

  return app.save(collection)
})
