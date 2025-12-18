# Function Definitions

This file documents the "functions" available to the FunList CTO AI and Replit Specialist Agents.  It serves as a manual lookup for simulating function calls until true API integration is available.

## Agent: Replit Specialist Agent

---

### Function Name: `get_replit_config`

**Description:** Retrieves the Replit configuration settings.
**Parameters:** None
**Expected Output:** A JSON object (represented as a string) containing the key Replit configuration settings, including `nix` configuration (packages, build commands, runtime environment), environment variables (structure only, no secret values), and deployment settings.
**Example Call:** `get_replit_config()`
**Manual Execution Instructions:**
    1. Open the `replit.nix` file in the Replit editor. Copy the entire contents.
    2. Open the "Secrets" tool in the Replit sidebar. Create a temporary, formatted JSON that mirrors the *structure* from secrets. Do NOT include the actual secret values; use placeholders like "REDACTED_API_KEY".
    3.  Check the Replit "Deployment" section to obtain information such as, "Deployed to production", "Last deployment".
    4. Construct a JSON string that includes:
        - `nix`: The content of `replit.nix`.
        - `env_vars`: The *structure* of the environment variables (from step 2, with placeholder values).
        - `deployment`: Describe the current deployment settings.
    5. Provide the combined, final JSON string.
**Error Handling:** None (This function should always succeed; if there's a problem, it's a Replit environment issue).

---

### Function Name: `get_deployment_status`

**Description:** Retrieves the current deployment status of the Replit application.
**Parameters:** None
**Expected Output:** A string describing the deployment status (e.g., "Deployed", "Deploying", "Failed", "Stopped").  If available, include the timestamp of the last deployment.
**Example Call:** `get_deployment_status()`
**Manual Execution Instructions:**
    1. In Replit, go to the "Deployments" section (usually in the sidebar).
    2. Observe the current status and any recent deployment information.
    3. Provide a concise string summarizing the status (e.g., "Deployed. Last deployment: 2024-07-24 15:30 UTC").
**Error Handling:** None (This function should always succeed).

---

### Function Name: `get_environment_variables`

**Description:** Retrieves the *structure* (names and descriptions, but NOT values) of the environment variables defined in Replit.
**Parameters:** None
**Expected Output:** A JSON object (represented as a string) where keys are environment variable names and values are *descriptions* of the variables (or empty strings if no description is available).  Do NOT include the actual values.
**Example Call:** `get_environment_variables()`
**Manual Execution Instructions:**
    1. In Replit, go to the "Secrets" section (usually in the sidebar).
    2.  Create a temporary, formatted JSON that mirrors the structure from secrets. Do *NOT* include the actual secret values; use placeholders like "REDACTED_API_KEY".
    3. Provide the JSON object.
**Error Handling:** None (This function should always succeed).

---
### Function Name: `analyze_replit_nix`

**Description:** Analyzes the `replit.nix` file for potential issues (missing dependencies, incorrect configurations, etc.). This is a *descriptive* analysis, not an automated check.
**Parameters:** None
**Expected Output:** A string containing a human-readable analysis of the `replit.nix` file, highlighting any potential problems or areas for improvement.
**Example Call:** `analyze_replit_nix()`
**Manual Execution Instructions:**
    1. Open the `replit.nix` file in the Replit editor.
    2. Examine the file content. Look for:
       - Missing or incorrect package names in the `deps` array.
       - Incorrect Python or Node.js versions.
       - Build commands that might be failing.
       - Any obvious errors or inconsistencies.
    3. Describe any potential issues you find in a clear and concise string.  If no issues are found, state "No issues found."
**Error Handling:** None (This is a manual analysis).

---

### Function Name: `check_python_version`
**Description:** Checks the currently active Python version in the Replit environment.
**Parameters:** None
**Expected Output:** A string containing the Python version (e.g., "3.11.4").
**Example Call:** `check_python_version()`
**Manual Execution Instructions:**
1. Open the Replit Shell.
2. Run the command: `python3 --version`
3. Copy the output from the shell and provide it as a string.
**Error Handling:** If the command fails, provide the exact error message from the shell.

---

### Function Name: `check_nodejs_version`

**Description:** Checks the currently active Node.js version in the Replit environment.
**Parameters:** None
**Expected Output:** A string containing the Node.js version (e.g., "18.16.0").
**Example Call:** `check_nodejs_version()`
**Manual Execution Instructions:**
    1. Open the Replit Shell.
    2. Run the command: `node --version`
    3. Copy the output from the shell and provide it as a string.
**Error Handling:** If the command fails, provide the exact error message from the shell.

---
### Function Name: `list_installed_packages`

**Description:** Lists the installed Python packages and their versions in the Replit environment.
**Parameters:**
    * `package_manager` (string, optional): Specifies the package manager to use. Can be "pip" (default) or "poetry".
**Expected Output:** A string containing a list of installed packages and their versions. The format should match the output of `pip list` or `poetry show`.
**Example Call:** `list_installed_packages()`, `list_installed_packages(package_manager='poetry')`
**Manual Execution Instructions:**
    1. Open the Replit Shell.
    2. If `package_manager` is "poetry" or not specified:
        - Run the command: `poetry show`
    3.  If `package_manager` is "pip":
        -   Run the command: `pip list`
    4. Copy the output from the shell and provide it as a string.
**Error Handling:** If the command fails, provide the exact error message from the shell.

---

### Function Name: `call_code_analysis_agent`

**Description:** Calls a separate AI agent specialized in static code analysis.
**Parameters:**
    *   `file_content` (string, required): The complete content of the code file to be analyzed.
**Expected Output:** A string containing a report from the code analysis agent, including identified issues and recommendations.
**Example Call:** N/A (This is a placeholder for future integration with a separate agent).
**Manual Execution Instructions:**
    1.  Copy the `file_content`.
    2.  Paste the content into a new prompt to the Code Analysis Agent, with a prompt requesting a thorough analysis.
    3.  Copy the response from the Code Analysis Agent.
    4.  Paste the copied response as a string.
**Error Handling:** Report any errors from the Code Analysis Agent.

---

### Function Name: `call_documentation_agent`

**Description:** Calls a separate AI agent specialized in generating documentation from code.
**Parameters:**
    *   `file_content` (string, required): The complete content of the code file.
**Expected Output:** A string containing generated documentation for the provided code.
**Example Call:** N/A (This is a placeholder for future integration with a separate agent).
**Manual Execution Instructions:**
    1.  Copy the `file_content`.
    2.  Paste the content into a new prompt to the Documentation Agent, with a prompt requesting documentation generation.
    3.  Copy the response from the Documentation Agent.
    4.  Paste the copied response as a string.
**Error Handling:** Report any errors from the Documentation Agent.

---

## Agent: FunList CTO AI Agent

---

### Function Name: `get_database_schema`

**Description:** Retrieves the schema (structure) of a specified database table.
**Parameters:**
    *   `table_name` (string, required): The name of the database table.
**Expected Output:** A string representation of the database schema. May be in JSON or a similar structured format. (For now, we will use the output of the `psql` command `\d table_name`).
**Example Call:** `get_database_schema(table_name='events')`
**Manual Execution Instructions:**
    1. Open the Replit Shell.
    2. Connect to the PostgreSQL database using `psql` (you may need to set the `DATABASE_URL` environment variable first if it's not already set).
    3. Run the command: `\d <table_name>`; (Replace `<table_name>` with the actual table name).
    4. Copy the *entire* output from the `psql` command, including any column definitions, indexes, and constraints.
    5. Paste the copied output as a string.
**Error Handling:** If the command fails (e.g., table not found), provide the exact error message from `psql`.

---

### Function Name: `check_server_logs`

**Description:** Retrieves recent entries from the application server logs.
**Parameters:**
    *   `log_file` (string, required): The name of the log file (e.g., "app.log").
    *   `lines` (integer, optional): The number of lines to retrieve (default: 100).
**Expected Output:** A string containing the log entries, separated by newlines. If the log file doesn't exist, return the string "Log file not found."
**Example Call:** `check_server_logs(log_file='app.log', lines=50)`
**Manual Execution Instructions:**
    1. Open the Replit Shell.
    2. Use the `tail` command to get the log entries. For example: `tail -n 50 app.log` (if `lines` is 50). If `lines` is not specified, use `tail -n 100 app.log`.
    3. Copy the output from the shell.
    4. If the file doesn't exist you will receive an error. Copy that.
    5. Paste the copied output as a string.
**Error Handling:**
    *   If the `tail` command fails (e.g., file not found), provide the exact error message from the shell.

---

### Function Name: `execute_python_code`

**Description:** (USE WITH EXTREME CAUTION) Executes a small snippet of Python code. *Only* for simple calculations/data transformations, *never* for database modification or security-sensitive operations.
**Parameters:**
    *   `code` (string, required): The Python code to execute.
**Expected Output:** The result of the code execution. May be an error message if the code fails.
**Example Call:** `execute_python_code(code='2 + 2')`
**Manual Execution Instructions:**
    1.  **CAREFULLY REVIEW THE CODE.** Ensure it's safe and does not perform any harmful actions.
    2.  Open the Replit Shell.
    3.  Start a Python interpreter by typing `python3`.
    4.  Paste the code snippet into the interpreter and press Enter.
    5.  Copy the output from the interpreter.
    6.  Paste the copied output as a string.
**Error Handling:** If the code produces an error, provide the *exact* error message from the Python interpreter.

---

### Function Name: `query_google_maps_api`

**Description:** Retrieves information from the Google Maps API (e.g., geocoding, directions). Requires a valid API key (handled securely outside this prompt).
**Parameters:**
    * `query` (string, required): The query to send to the Google Maps API.
**Expected Output:** The result from the Google Maps API (likely in JSON format).
**Example Call:** Placeholder - Requires API setup. Will be refined later.
**Manual Execution Instructions:** Placeholder - Will be refined later.
**Error Handling:** Placeholder - Will be refined later.

---

### Function Name: `query_gemini_pro`

**Description:** Queries the Gemini Pro model for more advanced reasoning and problem-solving.
**Parameters:**
    *   `query` (string, required): The question or problem description to send to Gemini Pro.
**Expected Output:** The response from Gemini Pro.
**Example Call:** N/A (This is a placeholder for direct interaction with Gemini Pro).
**Manual Execution Instructions:**
     1.  Copy the `query`
     2.  Create a new prompt with the Gemini Pro Model.
     3.  Copy the response.
     4.  Paste the copied output as a string.
**Error Handling:** Report any errors from Gemini Pro.

---

### Function Name: `get_project_document`

**Description:** Retrieves the content of a named project document stored within the Replit project directory.
**Parameters:**
     * `document_name` (string, required): The name of the document to retrieve (e.g., "agent_directory", "master_prompt_library", "mvp_requirements").
**Expected Output:**  The complete text content of the requested document.
**Example Call:** `get_project_document(document_name='function_definitions.md')`
**Manual Execution Instructions:**
    1. Open the Replit file tree.
    2. Locate the file specified by `document_name`.
    3. Open the file in the Replit editor.
    4. Select all the text (Ctrl+A or Cmd+A).
    5. Copy the selected text.
    6. Paste the copied text as a string.
**Error Handling:**
    *   If the file is not found, return the string "File not found: [filename]".

---
### Function Name: `create_checklist`

**Description:** Creates a checklist of all the files, Replit settings, and database elements that need to be updated to apply the changes to fix the error, add feature, or other request
**Parameters:** None
**Expected Output:** a Markdown formatted checklist.
**Example Call:** `create_checklist()`
**Manual Execution Instructions:** N/A - This function is handled internally by the FunList CTO AI, based on its analysis of the problem and the proposed solution.  It does not require manual intervention.
**Error Handling:** N/A
