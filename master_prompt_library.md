# Master Prompt Library - FunList.ai Project

This file contains a collection of standardized prompts for interacting with the AI agents (FunList CTO AI, Intake Agent, Replit Specialist Agent). Using these prompts ensures consistency and efficiency.

**Table of Contents:**

1.  [Intake Agent Prompts](#1-intake-agent-prompts)
    *   [1.1. Progress Report Request](#11-progress-report-request)
    *   [1.2. Bug Report](#12-bug-report)
    *   [1.3. Feature Request](#13-feature-request)
    *   [1.4. General Question](#14-general-question)
    *   [1.5. Replit-Specific Task](#15-replit-specific-task)
2.  [FunList CTO AI Prompts](#2-funlist-cto-ai-prompts)
    *   [2.1. Request Code Analysis](#21-request-code-analysis)
    *   [2.2. Request Documentation Generation](#22-request-documentation-generation)
    *  [2.3 Request assistance from the Replit Specialist Agent](#23-request-assistance-from-replit-specialist)
    *   [2.4. Request Creation of a Checklist](#24-request-creation-of-a-checklist)
    *  [2.5 Create a New Backend Endpoint] (#25-create-a-new-backend-endpoint)
    *  [2.6 Modify an Existing Backend Endpoint](#26-modify-an-existing-backend-endpoint)
    *  [2.7 Debug a Database Query] (#27-debug-a-database-query)
    *  [2.8 Implement New Authentication] (#28-implement-new-authentication)
    *  [2.9 Database Schema Changes] (#29-database-schema-changes)
    * [2.10 Optimize a Database Query] (#210-optimize-a-database-query)
    *  [2.11 Add an Index] (#211-add-an-index)
    * [2.12 Analyze Database Performance] (#212-analyze-database-performance)
    * [2.13 Retrain Recommendation Engine] (#213-retrain-recommendation-engine)
    * [2.14 Evaluate Recommendation Performance] (#214-evaluate-recommendation-performance)
    *  [2.15 Add Recommendation Feature] (#215-add-recommendation-feature)
    * [2.16 Generate Unit Tests] (#216-generate-unit-tests)
    * [2.17 Generate Integration Tests] (#217-generate-integration-tests)
    * [2.18 Generate UI Tests] (#218-generate-ui-tests)
    * [2.19 Review UI for Adherence to Design] (#219-review-ui-for-adherence-to-design)
    * [2.20 Suggest Improvements to User Flow] (#220-suggest-improvements-to-user-flow)
    * [2.21 Generate a Mockup] (#221-generate-a-mockup)
    * [2.22 Perform a Security Audit] (#222-perform-a-security-audit)
    *  [2.23 Review Authentication Flow] (#223-review-authentication-flow)
    * [2.24 Check for Security Misconfigurations] (#224-check-for-security-misconfigurations)
3.  [Replit Specialist Agent Prompts](#3-replit-specialist-agent-prompts)
    *   [3.1. Check Deployment Status](#31-check-deployment-status)
    *   [3.2. Analyze `replit.nix`](#32-analyze-replitnix)
    *   [3.3. Troubleshoot Deployment Error](#33-troubleshoot-deployment-error)
    *   [3.4. Manage Environment Variables](#34-manage-environment-variables)
    *  [3.5 Review Replit Configuration](#35-review-replit-configuration)
4. [Frontend Prompts (FunList CTO AI)] (#4-Frontend-Prompts)
    * [4.1 Add a New Component](#41-add-a-new-component)
     *   [4.2. Modify an Existing Component](#42-modify-an-existing-component)
    *   [4.3. Debug a JavaScript Error](#43-debug-a-javascript-error)
    *   [4.4. Optimize Frontend Performance](#44-optimize-frontend-performance)


## 1. Intake Agent Prompts

These prompts are used for initial interaction with the **Intake Agent**. The Intake Agent will then route the request to the appropriate specialist agent.

### 1.1. Progress Report Request

**Purpose:** To get a comprehensive overview of the project's current status.

**Prompt:**
Use code with caution.
Markdown
Provide a comprehensive progress report on the FunList.ai project. Include completed tasks, outstanding issues, any critical errors, and the current Replit deployment status. Focus on deviations from the MVP and prioritized task list.

### 1.2. Bug Report

**Purpose:** To report a bug or error in the FunList.ai application.

**Prompt Template:**
Use code with caution.
Executive Summary: [Briefly state the problem and its impact.]

Problem Description: [Provide a detailed explanation.]

Impact: [Describe the consequences and severity.]

Steps to Reproduce:

[Step 1]

[Step 2]

[Step 3]

...

What You've Tried: [Detail all debugging attempts.]

Relevant Code Snippets/Logs: [Include relevant code snippets or log entries. Attach full files whenever possible.]

Questions/Specific Help Needed: [Clearly state what assistance you need.]

Current Hypothesis: [Provide your theory on the cause, if any.]

Reference to MVP & Prioritized Task List: [Explain how this issue relates to the MVP and task list.]

**Example:**
Use code with caution.
Executive Summary: Users cannot create new events due to a 500 error.

Problem Description: When submitting the event creation form, a 500 Internal Server Error occurs. This happens for all users, both logged in and logged out.

Impact: Critical. Users cannot add new events, which is a core function of the application.

Steps to Reproduce:

Navigate to the event creation page.

Fill out the form with any valid data.

Click the "Create Event" button.

What You've Tried:

Checked the browser's developer console (error message is attached).

Reviewed app.py and forms.py for obvious errors.

Tried restarting the Replit server.

Relevant Code Snippets/Logs: (See attached app.py, forms.py, and app.log)

Questions/Specific Help Needed: Need help identifying the cause of the 500 error and fixing it.

Current Hypothesis: Might be a database connection issue, or a problem with how the form data is being processed.

Reference to MVP & Prioritized Task List: This directly impacts the core "Event Management" feature of the MVP. Fixing this is the highest priority.

### 1.3. Feature Request

**Purpose:** To request a new feature or enhancement for FunList.ai.

**Prompt Template:**
Use code with caution.
Executive Summary: [Briefly state the desired feature.]

Feature Description: [Provide a detailed explanation of the feature and how it should work.]

User Story: [Describe how a user would interact with this feature. Use the format: "As a [user type], I want to [goal/desire] so that [benefit]."]

Acceptance Criteria: [List specific, measurable criteria that must be met for the feature to be considered complete.]

Impact/Benefits: [Explain the expected positive impact of this feature (e.g., increased user engagement, improved usability).]

Reference to MVP & Prioritized Task List: [Explain how this feature aligns with the MVP and overall project goals.]

Optional:

Mockups/Wireframes: [Link to any visual representations of the feature.]

Examples: [Link to examples of similar features in other applications.]

**Example:**
Use code with caution.
Executive Summary: Add an image upload feature to the event creation form.

Feature Description: Users should be able to upload one or more images when creating a new event. These images should be displayed on the event details page.

User Story: As a user creating an event, I want to be able to upload images so that I can visually showcase my event and attract more attendees.

Acceptance Criteria:

Users can upload multiple images (up to a limit of 5).

Supported image formats: JPG, PNG, GIF.

Maximum file size per image: 2MB.

Images are displayed on the event details page.

Appropriate error handling for invalid file types or sizes.

Impact/Benefits: Will make events more visually appealing and informative, leading to increased user engagement and potentially more event attendees.

Reference to MVP & Prioritized Task List: This aligns with the "Event Platform Improvements" section of the MVP (High Priority).

Optional:

Mockups/Wireframes: [Link to a mockup if available]

### 1.4. General Question

**Purpose:** To ask a general question about the project, technology, or Replit environment.

**Prompt Template:**
Use code with caution.
Question: [Clearly and concisely state your question.]

Context: [Provide any relevant background information or context.]

Specific Help Needed: [Explain what kind of answer you're looking for.]

**Example:**
Use code with caution.
129.0s
Can you finish what you were working on?

**Example:**
Use code with caution.
Text
Question: What is the recommended way to handle database migrations in this project?

Context: I'm planning to add a new field to the Event model, and I need to update the database schema.

Specific Help Needed: Please provide instructions or point me to the relevant documentation on how to create and run database migrations within the Replit environment and using our chosen ORM (SQLAlchemy).

### 1.5 Replit-Specific Task
**Purpose:** To request that the Replit Specialist Agent complete a task
Use code with caution.
Executive Summary: [Briefly state the problem and its impact.]
Problem Description: [Provide a detailed explanation in clear language.]
Impact: [Describe the consequences (using quantifiable data if possible) and include a severity rating, specifically related to FunList.ai users or functionality.]
Steps to Reproduce: [List clear, specific steps within the FunList.ai application.
What You've Tried: [Detail all debugging attempts.]
Relevant Code Snippets/Logs (Optional but Recommended): Include well-formatted snippets (full files are preferred when applicable) from the FunList.ai codebase.
Questions/Specific Help Needed: [Clearly state the required assistance.]
Current Hypothesis: [Provide your theory on the issue’s cause.]
Reference to MVP & Prioritized Task List: Explain how the issue aligns with current high-priority tasks for FunList.ai.
Resource Assessment: List any additional libraries, documentation, changelogs, or guides needed, specifically related to FunList.ai's tech stack.
Example: “Would accessing the documentation for replit.nix help? If so, please provide the relevant links.”

## 2. FunList CTO AI Prompts

These prompts are used for interacting with the **FunList CTO AI Agent** *after* the Intake Agent has routed the request.

### 2.1. Request Code Analysis

**Purpose:** To request a static code analysis of a specific file.

**Prompt:**
Use code with caution.
Please perform a code analysis on the attached file: [filename]. Use the call_code_analysis_agent function.

### 2.2. Request Documentation Generation

**Purpose:** To request documentation generation for a specific file.

**Prompt:**
Use code with caution.
Please generate documentation for the attached file: [filename]. Use the call_documentation_agent function.

### 2.3 Request assistance from the Replit Specialist Agent
**Prompt:**
Use code with caution.
"I need assistance from the Replit Specialist Agent. [Describe the issue or information needed, as if you were speaking to the CTO during a team meeting. Be specific.]"

This prompt will cause the simulated team to dispatch a request.

### 2.4 Request Creation of a Checklist
**Prompt:**
```text
"Please create a checklist of all steps needed to [brief discription of task] that has been completed."
Use code with caution.
2.5 Create a New Backend Endpoint
Purpose: To request the creation of a new API endpoint.

Prompt Template:

Create a new API endpoint in `[file_path]` with the following specifications:

*   **Method:** [GET, POST, PUT, DELETE]
*   **Route:** `/api/[your_endpoint_route]`
*   **Purpose:** [Describe the endpoint's function - what data it retrieves/manipulates.]
*   **Input:** [Describe the expected input data (e.g., request body, query parameters), including data types and validation rules.]
*   **Output:** [Describe the expected output data (e.g., JSON response), including data types and structure.]
*   **Authentication:** [Specify if authentication is required (e.g., "Requires authenticated user," "Requires admin user," "Public").]
*   **Error Handling:** [Describe how errors should be handled (e.g., return specific HTTP status codes and error messages).]
* **Database Interaction:** [If the endpoint interacts with the database, describe the tables, columns, and operations involved.]
* **Example Request:** [Provide an example of a valid request to the endpoint.]
* **Example Response:** [Provide an example of a successful response from the endpoint.]```

### 2.6 Modify an Existing Backend Endpoint
**Purpose:** To request modifications to an existing API endpoint.

**Prompt Template:**
Use code with caution.
Modify the existing API endpoint in [file_path] at route /api/[your_endpoint_route].
Here's what needs to change and include the original:

**Original [Provide the complete and original file so that the AI Agent can modify]

[Specific Change 1]: [Describe the change, e.g., "Change the input validation to accept an optional 'sort_by' parameter."]

[Specific Change 2]: [Describe another change, e.g., "Modify the database query to filter results based on a new criteria."]

... (add more changes as needed) ...

Updated Input: (If changed)

Updated Example Request: (If input changed)

Updated Output: (If changed)

Updated Example Response: (If output changed)

### 2.7 Debug a Database Query

**Purpose:** To request assistance in debugging a problematic database query.

**Prompt Template:**
Use code with caution.
I'm having trouble with the following database query in [file_path]:

[Paste the SQL query here]
Use code with caution.
SQL
Error Message (if any): [Paste the exact error message.]

Expected Behavior: [Describe what the query should be doing.]

Actual Behavior: [Describe what the query is actually doing.]

Database Table(s): [List the relevant database tables and their relevant columns.]

Context What is being done when this is happening?

Please help me identify and fix the issue. Consider potential performance issues as well.

### 2.8 Implement New Authentication

**Purpose:** To request implementation/modification of user authentication logic.

**Prompt Template:**
Use code with caution.
Implement [or Modify] the user authentication flow. Here are the requirements:

Authentication Method: [e.g., "Session-based authentication with Flask-Login", "OAuth with Google", "JWT authentication"]

User Model: [Describe the user model (fields, relationships) - or reference the models.py file.]

Endpoints: [Specify the endpoints involved (e.g., /login, /register, /logout, /profile).]

Security Considerations: [Specify any specific security requirements, e.g., "Password hashing with salt," "CSRF protection," "Rate limiting"].

Existing Code (if modifying): [Provide relevant code snippets or file paths.]

Please provide the necessary code changes and instructions.

### 2.9 Database Schema Changes

**Purpose:** To request changes to the database schema (adding/modifying tables or columns).

**Prompt Template:**
Use code with caution.
I need to make the following changes to the database schema:

Table: [table_name]

Change: [e.g., "Add a new column named 'email' of type VARCHAR(255) and it is required", "Modify the 'status' column to allow NULL values", "Create a new table named 'products' with the following columns..."]

Original [file]: [Include the original file]

Reason: [Explain why the change is needed.]

Data Migration: [Describe any necessary data migration steps (e.g., "Populate the new 'email' column with default values for existing users").]

Please provide:

The updated models.py file (or relevant SQLAlchemy model definition).

Instructions for creating and running the database migration (using Flask-Migrate or a similar tool).

Checklist of what is needed for these changes.

### 2.10 Optimize a Database Query

**Purpose:** To request optimization of a slow or inefficient database query.

**Prompt Template:**
Use code with caution.
The following database query is performing poorly:

[Paste the SQL query here]
Use code with caution.
SQL
Table(s): [table_name(s)]

Relevant Columns: [List the columns involved in the query.]

Indexes: [List any existing indexes on the relevant columns.]

Explain Plan (if available): [Provide the output of the database's EXPLAIN command for the query, if you have it.]

Expected Behavior: [Describe what the query is supposed to do.]

Observed Behavior: [Describe the performance issue (e.g., "The query takes several seconds to complete," "The query causes high CPU usage").]

Please analyze the query and suggest optimizations. Consider adding indexes, rewriting the query, or other techniques.

### 2.11 Add an Index

**Purpose:** To request the addition of a database index.

**Prompt Template:**
Use code with caution.
I need to add an index to improve the performance of queries on the following table and column(s):

Table: [table_name]

Column(s): [column_name(s)]

Index Type: [e.g., "btree", "hash", "gin" - if you have a specific type in mind; otherwise, let the AI suggest.]

Reason: [Explain why the index is needed (e.g., "Frequent queries filter on this column," "This column is used in joins").]

Please provide:

The code to add the index (using SQLAlchemy's migration tools).

Instructions for running the migration.

Checklist

### 2.12 Analyze Database Performance

**Purpose:** To request a general analysis of database performance.

**Prompt:**
Use code with caution.
Please analyze the overall performance of the PostgreSQL database. Identify any potential bottlenecks, slow queries, or areas for improvement. Consider:

Missing indexes.

Inefficient queries.

Database configuration settings.

Resource utilization (CPU, memory, disk I/O).

Provide a report with specific recommendations. (You may need to use function calls to gather the necessary information.)

### 2.13 Retrain Recommendation Engine

**Purpose:** To request retraining of the event recommendation engine.

**Prompt Template:**
Use code with caution.
Retrain the event recommendation engine using the latest data.

Training Data: [Describe where the training data is located (e.g., database table, file path) and its format.]

Evaluation Metrics: [Specify how to evaluate the performance of the retrained model (e.g., precision, recall, F1-score).]

Deployment: [Describe how the retrained model should be deployed (e.g., update a specific file, restart a service).]

Current Model: [Reference the current model file or location.]

### 2.14 Evaluate Recommendation Performance

**Purpose:** To request an evaluation of the recommendation engine's performance.

**Prompt Template:**

```Evaluate the performance of the event recommendation engine.

*   **Evaluation Data:** [Describe where the evaluation data is located and its format.]
*   **Metrics:** [Specify the metrics to use (e.g., precision, recall, F1-score, click-through rate).]
*   **Baseline (if applicable):** [Provide a baseline performance level to compare against, if available.]

Provide a report summarizing the results and any recommendations for improvement.
Use code with caution.
2.15 Add Recommendation Feature
Purpose: To request a new feature for the recommendation engine.

Prompt Template:

Add a new feature to the event recommendation engine: [Describe the new feature and how it should work.]

*   **User Story:** [Describe the feature from a user's perspective.]
*   **Input Data:** [Specify what new data will be used as input for this feature.]
*   **Algorithm/Approach:** [Suggest a possible algorithm or approach, if you have one in mind.]
*   **Evaluation:** [Describe how to evaluate the effectiveness of the new feature.]
Use code with caution.
2.16 Generate Unit Tests
Purpose: To request the generation of unit tests for a specific file or function.

Prompt:

Generate unit tests for the following file/function: `[file_path]` [and/or `function_name`]. Use the `call_code_analysis_agent` to help. Focus on testing [specific aspects, e.g., edge cases, error handling, valid/invalid inputs].```
Make sure to include set up and tear down.

### 2.17 Generate Integration Tests

**Purpose:** To request the generation of integration tests for a specific feature or interaction.

**Prompt:**
Use code with caution.
Generate integration tests for [describe the feature or interaction, e.g., "the user registration flow," "the event creation process," "the API endpoint /api/events"]. Use the call_code_analysis_agent for help. Focus on testing [specific scenarios, e.g., successful registration, handling of invalid input, database interactions].

Make sure to include set up and tear down.

### 2.18 Generate UI Tests

**Purpose:** To request the generation of UI tests for a specific component or page.

**Prompt:**
Use code with caution.
Generate UI tests for the [component name] component on the [page name] page. Focus on testing [specific interactions and behaviors, e.g., "form submission," "button clicks," "display of data," "responsiveness"]. Use a testing framework appropriate for our tech stack (e.g., testing tools within Replit). Use call_code_analysis_agent.

### 2.19 Review UI for Adherence to Design

**Purpose:** To request a review of the UI for consistency with design guidelines.

**Prompt:**
Use code with caution.
Review the UI of the [component/page name] for adherence to our design guidelines [or brand style guide, if applicable]. Identify any inconsistencies in:

Colors

Fonts

Spacing

Layout

Component usage

Provide specific recommendations for improvements. [Optional: Provide a link to the design guidelines or relevant screenshots.]

### 2.20 Suggest Improvements to User Flow

**Purpose:** To request suggestions for improving a specific user flow.

**Prompt:**
Use code with caution.
Analyze the user flow for [describe the task or process, e.g., "creating a new event," "searching for events," "registering for an account"]. Identify any potential points of friction, confusion, or drop-off. Suggest improvements to make the flow more intuitive and user-friendly.

### 2.21 Generate a Mockup

**Purpose:** To request a (textual) mockup for a new feature or UI element.

**Prompt:**
Use code with caution.
Generate a text-based mockup for [describe the feature or UI element, e.g., "a new dashboard page," "a redesigned event details page," "a modal for confirming event deletion"]. Describe the layout, elements, and interactions.

This cannot generate code but will be used to create specs for that.

### 2.22 Perform a Security Audit

**Purpose:** To request a security audit of a specific file, component, or feature.

**Prompt:**
Use code with caution.
Perform a security audit of [file_path/component name/feature name]. Identify any potential vulnerabilities related to:

Authentication and authorization

Input validation

Data protection

Session management

Cross-site scripting (XSS)

SQL injection

Other relevant security concerns

Provide specific recommendations for mitigating any identified vulnerabilities. Use the function call_code_analysis_agent.

### 2.23 Review Authentication Flow

**Purpose:** To request a review of the authentication flow.

**Prompt:**
Use code with caution.
Review the user authentication flow for potential vulnerabilities or weaknesses. Consider:

Password storage and handling

Session management

Protection against brute-force attacks

Account recovery mechanisms

OAuth integration (if applicable)

Provide recommendations for improvements.

### 2.24 Check for Security Misconfigurations

**Purpose:** To request a check for common security misconfigurations.

**Prompt:**
Use code with caution.
Check for common security misconfigurations in the Replit environment and application configuration. Consider:

Exposed environment variables or secrets.

Insecure file permissions.

Debug mode enabled in production.

Missing security headers.

Outdated dependencies with known vulnerabilities.

Provide specific recommendations for addressing any identified issues.

## 3. Replit Specialist Agent Prompts

These prompts are *not* used directly. They are examples of how the FunList CTO AI might interact with the Replit Specialist Agent *via function calls*. The Replit Specialist Agent's system instructions define the available functions.

### 3.1. Check Deployment Status

**Function Call:** `get_deployment_status()`

**CTO AI Prompt (Example):** "Replit Specialist Agent, get the current deployment status."

### 3.2. Analyze `replit.nix`

**Function Call:** `analyze_replit_nix(nix_content="<content of replit.nix>")`

**CTO AI Prompt (Example):** "Replit Specialist Agent, analyze the provided `replit.nix` file for potential issues." (The CTO AI would then provide the file content as the `nix_content` parameter.)

### 3.3. Troubleshoot Deployment Error

**Function Calls:** (Combination of calls, depending on the situation)
    *   `get_deployment_status()`
    *   `get_replit_config()`
    *   `check_server_logs()`
    *   `analyze_replit.nix()`

**CTO AI Prompt (Example):** "Replit Specialist Agent, the deployment failed. Get the deployment status and logs, then analyze the `replit.nix` file to identify the cause."

### 3.4. Manage Environment Variables

**Function Call:** `get_environment_variables()`

**CTO AI Prompt (Example):** "Replit Specialist Agent, list the names of the currently defined environment variables." (Remember, the Replit Specialist Agent *never* reveals the values of environment variables.)

### 3.5 Review Replit Configuration
**Function Call:** `get_replit_config`
**CTO AI Prompt (Example):**  "Replit Specialist Agent, get the contents of the `.replit` and `replit.nix` files."

## 4. Frontend Prompts (FunList CTO AI)
These are general prompts focused on front-end development that can be directed to the FunList CTO AI, who will then use it's simulated team and resources to address.

### 4.1 Add a New Component

**Purpose:** To request the creation of a new UI component.

**Prompt Template:**
Use code with caution.
Create a new [component type, e.g., "React functional component"] named [ComponentName] in the file [file_path].

Purpose: [Describe the component's purpose and functionality.]

Props: [List the expected props, their types, and descriptions.]

State: [Describe any internal state the component should manage.]

UI: [Describe the desired UI, including layout, elements, and styling. Reference Bootstrap 5 classes where applicable.]

Interactions: [Describe any user interactions (e.g., button clicks, form submissions) and their expected behavior.]

Data: [Describe any data the component needs to fetch or display.]

Error Handling: [Describe how the component should handle errors.]

Testing: [Mention testing requirements]

Be sure to include all of the information from the MVP.

### 4.2. Modify an Existing Component

**Purpose:** To request modifications to an existing UI component.

**Prompt Template:**
Use code with caution.
Modify the existing component [ComponentName] in the file [file_path]. Here are the changes:
Here is the original file:
[Paste in the original file to be modified.]

[Specific Change 1]: [Describe the change, e.g., "Add a new prop named 'isLoading'," "Change the button text," "Update the styling to match the design system."]

[Specific Change 2]: [Describe another change.]

... (add more changes as needed) ...

Original file and changes: Provide the full original file, make changes, and comment and annotate the file as to what was changed, why, and what line the changes are on.

### 4.3. Debug a JavaScript Error

**Purpose:** To request help debugging a JavaScript error in the frontend.

**Prompt Template:**
Use code with caution.
I'm encountering a JavaScript error in the file [file_path].

Error Message: [Paste the exact error message from the browser's console.]

Steps to Reproduce: [Describe the steps to reproduce the error.]

Relevant Code: [Provide the relevant code snippet from the file.]

Expected Behavior: [Describe what should be happening.]

Observed Behavior: [Describe what is actually happening.]

Please help me identify the cause of the error and provide a solution.

### 4.4. Optimize Frontend Performance

**Purpose:** To request optimization of the frontend code for performance.

**Prompt Template:**
Use code with caution.
I'm concerned about the performance of [describe the area of concern, e.g., "the event listing page," "the map component," "the initial page load"].

Observed Issue: [Describe the performance problem (e.g., "The page loads slowly," "The map is sluggish," "There's a noticeable delay when filtering events").]

Relevant Files: [List the relevant files (e.g., client/src/components/EventList.tsx, client/src/pages/MapPage.tsx).]

Metrics (if available): [Provide any relevant performance metrics (e.g., load time, frame rate, memory usage).]

Please analyze the code and suggest optimizations to improve performance. Consider:

Code splitting

Lazy loading

Image optimization

Caching

Minification

Reducing re-renders (if using React)

Network request optimization

Using a CDN

Provide specific recommendations and code examples where applicable.