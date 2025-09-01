/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // remove field
  collection.fields.removeById("select2765332939")

  // add field
  collection.fields.addAt(10, new Field({
    "cascadeDelete": false,
    "collectionId": "pbc_2800040823",
    "hidden": false,
    "id": "relation2638274075",
    "maxSelect": 999,
    "minSelect": 0,
    "name": "topic",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "relation"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1225573716")

  // add field
  collection.fields.addAt(4, new Field({
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
      "Releases & leakages",
      "Waste management",
      "Trade",
      "Existing plastic pollution",
      "Principles & approaches",
      "Exemptions",
      "Financial resources & mechanism",
      "Reporting, monitoring & effectiveness evaluation",
      "Capacity-building, technical assistance, technology transfer, international cooperation",
      "Information & research",
      "Institutional arrangements & final provisions",
      "National plans",
      "primary plastic polymers",
      "supply, sustainable production",
      "transparency, tracking, monitoring and labeling",
      "chemicals and polymers of concern",
      "plastic products and chemicals of concern as used in plastic products",
      "problematic and avoidable plastic products, including short-lived and single use plastic products and intentionally added microplastics",
      "problematic and avoidable plastic products, including short-lived and single use plastic products",
      "alternative plastics and plastic products",
      "non-plastic substitutes",
      "intentionally added microplastics",
      "micro- and nanoplastics",
      "review of chemicals and polymers of concern, microplastics and problematic and avoidable products",
      "transparency, tracking, monitoring and labeling",
      "product design, composition and performance",
      "product design and performance",
      "reduce, reuse, refill and repair of plastics and plastic products",
      "use of recycled plastic contents",
      "alternative plastics and plastic products",
      "non-plastic substitutes",
      "intentionally added microplastics micro- and nanoplastics",
      "transparency, tracking, monitoring and labeling",
      "releases and leakages",
      "emissions and releases of plastic throughout its life cycle",
      "micro- and nanoplastics",
      "fishing gear",
      "overarching provision related to part ii",
      "waste management (29)",
      "waste management (30)",
      "transboundary movement of plastic waste",
      "fishing gear",
      "extended producer responsibility",
      "transparency, tracking, monitoring and labeling",
      "trade in listed chemicals, polymers and products, and in plastic waste",
      "trade in listed chemicals, polymers and products",
      "transboundary movement of plastic waste",
      "transparency, tracking, monitoring and labeling",
      "existing plastic pollution, including in the marine environment",
      "Existing plastic pollution (Art. 9 of INC-5)",
      "Principles",
      "exemptions available to a party upon request",
      "financing",
      "extended producer responsibility",
      "reporting on progress",
      "periodic assessment and monitoring of the progress of implementation of the instrument * and effectiveness evaluation",
      "capacity-building, technical assistance and technology transfer",
      "international cooperation",
      "information exchange",
      "awareness-raising, education and research",
      "stakeholder engagement",
      "institutional arrangements",
      "governing body",
      "subsidiary bodies",
      "secretariat",
      "settlement of disputes",
      "amendment",
      "National plans",
      "overarching provision related to part ii"
    ]
  }))

  // remove field
  collection.fields.removeById("relation2638274075")

  return app.save(collection)
})
