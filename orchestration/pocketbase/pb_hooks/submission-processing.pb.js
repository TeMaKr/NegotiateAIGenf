/// <reference path="../pb_data/types.d.ts" />

onRecordUpdateRequest((e) => {
  // get the config and settings
  const config = require(`${__hooks}/config.js`);
  const settings = config.settings();

  // check if there is a change for verified
  const originalRecord = $app.findRecordById(
    e.record.collection().name,
    e.record.id
  );
  const verified = e.record.get("verified");
  const file = e.record.get("file");
  const session = e.record.get("session");

  if (originalRecord.get("verified") === verified) {
    $app
      .logger()
      .info("No change in verified state, skipping further processing.");
    e.next();
    return;
  }

  // if the record is not verified and has no file, set verified to false
  if (verified && !file) {
    $app
      .logger()
      .info("Record is verified and has no file, setting verified to false.");
    e.record.set("verified", false);
    e.next();
    return;
  }

  const retrieverId = e.record.get("retriever_id");

  // if not verified no need to process further
  if (!verified) {
    try {
      const response = $http.send({
        method: "DELETE",
        url: `${settings.api.host}/api/delete-submission-vector`,
        headers: { "X-API-Token": settings.api.token },
        body: JSON.stringify({
          retriever_id: retrieverId,
        }),
      });
      if (response.statusCode < 200 || response.statusCode >= 300) {
        throw new Error(
          `HTTP ${response.statusCode}: ${response.raw || "Request failed"}`
        );
      }
      $app
        .logger()
        .info(
          "The data record has been set to “not verified.” Existing vectors deleted from Qdrant. No further processes will be initiated."
        );
    } catch (error) {
      e.record.set("verified", false);
      $app
        .logger()
        .error(
          "The data record has been set to “not verified. Failed to delete vectors from Qdrant. No further processes will be initiated.",
          error
        );
      e.next();
    }
    e.next();
    return;
  }

  // get values from the record
  const id = e.record.get("id");
  const fileUrl =
    `${settings.pocketbase.host}/api/files/submissions/` +
    e.record.get("id") +
    "/" +
    file;

  // expand record to get topics
  $app.expandRecord(e.record, ["topic"], null);
  const topics = e.record.expandedAll("topic");

  // process the topics to create a dictionary of articles to key elements
  const articleKeyElementDict = {};

  if (topics && topics.length > 0) {
    topics.forEach((topic) => {
      const keyElements = topic.get("key_element");
      const article = topic.get("article");

      if (!articleKeyElementDict[article]) {
        articleKeyElementDict[article] = [];
      }

      keyElements.forEach((keyElement) => {
        if (!articleKeyElementDict[article].includes(keyElement)) {
          articleKeyElementDict[article].push(keyElement);
        }
      });
    });
  }

  // check if the record is verified and has a file and process accordingly
  try {
    const response = $http.send({
      method: "POST",
      url: `${settings.api.host}/api/process-submission`,
      headers: { "X-API-Token": settings.api.token },
      body: JSON.stringify({
        file_path: fileUrl,
        submission_id: id,
        retriever_id: retrieverId,
        href: fileUrl,
        key_elements:
          Object.keys(articleKeyElementDict).length > 0
            ? articleKeyElementDict
            : null,
        session: session,
      }),
    });

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw new Error(
        `HTTP ${response.statusCode}: ${response.raw || "Request failed"}`
      );
    }
  } catch (error) {
    e.record.set("verified", false);
    $app.logger().error("Error creating vectors entry", error);
    e.next();
  }

  e.next();
}, "submissions");

/// <reference path="../pb_data/types.d.ts" />

onRecordAfterCreateSuccess((e) => {
  const verified = e.record.get("verified");
  const file = e.record.get("file");
  const session = e.record.get("session");

  // if the record is not verified and has no file, set verified to false
  if (verified && !file) {
    $app
      .logger()
      .info("Record is verified and has no file, setting verified to false.");
    e.record.set("verified", false);
    e.next();
    return;
  }

  // if not verified no need to process further
  if (!verified) {
    e.next();
    return;
  }

  // get the config and settings
  const config = require(`${__hooks}/config.js`);
  const settings = config.settings();

  // get values from the record
  const retrieverId = e.record.get("retriever_id");
  const id = e.record.get("id");
  const fileUrl =
    `${settings.pocketbase.host}/api/files/submissions/` +
    e.record.get("id") +
    "/" +
    file;

  // expand record to get topics
  $app.expandRecord(e.record, ["topic"], null);
  const topics = e.record.expandedAll("topic");

  // process the topics to create a dictionary of articles to key elements
  const articleKeyElementDict = {};

  if (topics && topics.length > 0) {
    topics.forEach((topic) => {
      const keyElements = topic.get("key_element");
      const article = topic.get("article");

      if (!articleKeyElementDict[article]) {
        articleKeyElementDict[article] = [];
      }

      keyElements.forEach((keyElement) => {
        if (!articleKeyElementDict[article].includes(keyElement)) {
          articleKeyElementDict[article].push(keyElement);
        }
      });
    });
  }

  // check if the record is verified and has a file and process accordingly
  try {
    const response = $http.send({
      method: "POST",
      url: `${settings.api.host}/api/process-submission`,
      headers: { "X-API-Token": settings.api.token },
      body: JSON.stringify({
        file_path: fileUrl,
        submission_id: id,
        retriever_id: retrieverId,
        href: fileUrl,
        key_elements:
          Object.keys(articleKeyElementDict).length > 0
            ? articleKeyElementDict
            : null,
        session: session,
      }),
    });
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw new Error(
        `HTTP ${response.statusCode}: ${response.raw || "Request failed"}`
      );
    }
  } catch (error) {
    e.record.set("verified", false);
    $app.logger().error("Error creating vectors entry", error);
    e.next();
  }

  e.next();
}, "submissions");

onRecordCreate((e) => {
  let retrieverId;
  let record = true;
  while (!!record) {
    retrieverId = $security.randomStringByRegex("[0-9]{1,5}");
    try {
      record = e.app.findFirstRecordByData(
        "submissions",
        "retriever_id",
        retrieverId
      );
    } catch {
      record = false;
    }
  }
  e.record.set("retriever_id", retrieverId);
  e.next();
}, "submissions");

onRecordAfterDeleteSuccess((e) => {
  const config = require(`${__hooks}/config.js`);
  const settings = config.settings();
  const retrieverId = e.record.get("retriever_id");

  try {
    const response = $http.send({
      method: "DELETE",
      url: `${settings.api.host}/api/delete-submission-vector`,
      headers: { "X-API-Token": settings.api.token },
      body: JSON.stringify({
        retriever_id: retrieverId,
      }),
    });
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw new Error(
        `HTTP ${response.statusCode}: ${response.raw || "Request failed"}`
      );
    }
    $app.logger().info("Record deleted. Existing vectors deleted from Qdrant.");
  } catch (error) {
    e.record.set("verified", false);
    $app.logger().error("Record deleted. Existing vectors not deleted", error);
    e.next();
  }
  e.next();
}, "submissions");
