/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {

  const submissions = app.findAllRecords("submissions");

  submissions.forEach((submission) => {
    if (!submission.get("session_temp")) {
      submission.set("session_temp", submission.get("session"));
    }
    app.save(submission);
  });

});
