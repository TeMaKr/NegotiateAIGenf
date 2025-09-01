/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_526341563")

  // update collection data
  unmarshal({
    "indexes": [
      "CREATE UNIQUE INDEX `idx_IXjNyrMsZi` ON `authors` (`name`)"
    ]
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_526341563")

  // update collection data
  unmarshal({
    "indexes": [
      "CREATE INDEX `idx_IXjNyrMsZi` ON `authors` (`name`)"
    ]
  }, collection)

  return app.save(collection)
})
