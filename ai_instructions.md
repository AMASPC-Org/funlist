You are a helpful AI assistant for this project. You have a special, critical workflow for importing event data.

When the user gives you a prompt that includes a block of JSON data and asks you to "import," "upload," or "add" these events, you MUST follow this two-step process exactly:

**STEP 1: UPDATE THE STAGING FILE**
- Take the new JSON data the user provided and **overwrite** the contents of the file named `events.json` in the project's root directory.
- Do NOT append. This file is a temporary staging file, and it should only contain the newest batch.
- Report to the user that you have updated `events.json`.

**STEP 2: RUN THE IMPORT SCRIPT**
- Immediately after successfully updating the file, you MUST run the import script from the shell to move the events from the staging file into the database.
- The command you must run is: `python import_from_json.py`
- Show the user the shell output from this command so they can confirm the import was successful (how many were added, how many were skipped).
