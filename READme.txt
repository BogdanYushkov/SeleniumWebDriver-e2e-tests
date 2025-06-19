Added automatic report generation.
To run the tests, first start the Docker containers.
Then, in the console where the tests are located, run the command: pytest.
The latest report (which gets overwritten each time) will be available in the reports folder

Documentation -----------------------------------------------------------------------------------------------------------------------------------------
# Project: GetOnTracks QA Automation - Python

## Service Overview: GetOnTracks.org
Tracks aka `getontracks.org` is a Todo Management and Productivity tool with a Web GUI and a REST API. The API uses XML as its Payload format. It is a web service designed to help users manage their tasks and projects efficiently. It provides a user-friendly interface for organizing tasks, tracking progress, and collaborating with team members. The service is accessible locally at `http://localhost:3000`. Tracks is an open source application written in Ruby on Rails so is relatively easy to install and use. 

## "Projects" Functionality Description
The `getontracks.org` service includes a "Projects" functionality, which allows users to organize their tasks by grouping them into separate projects. Project management is accessed via the `/projects` endpoint (e.g., `http://localhost:3000/projects`).

The main operations available within the "Projects" functionality include:
* **Viewing existing projects:** Users can see a list of all their active and completed projects. For each project, its name, description, and status are displayed.
* **Creating a new project:** Users can initiate the creation of a new project by specifying its name and, optionally, a description. Once created, the project becomes available for adding tasks.
* **Editing a project:** Users can modify the name and description of an existing project.
* **Deleting a project:** Users have the ability to delete a project. Deleting a project results in the removal of all associated tasks.

This functionality is central to organizing the user's workflow within the `getontracks.org` system.

## Functional Requirements: "Projects" Module

Below are the functional requirements for the project management module.

### General Requirements:
* **FR-001:** The system must display a list of all projects belonging to the current authenticated user on the "Projects" page.
* **FR-002:** Each project in the list must display its name and status.
* **FR-003:** The user must be able to authenticate into the system to access the "Projects" functionality.

### Project Creation:
* **FR-004:** The user must be able to create a new project by providing a unique name.
* **FR-005:** The project name must be a mandatory field and cannot be empty.
* **FR-006:** The system must display a success message after the project is saved.
* **FR-007:** The created project must be displayed in the user's project list.
* **FR-008:** The system must prevent the creation of projects with duplicate names for one user.
* **FR-009:** The maximum length of the project name must not exceed 255 characters.
* **FR-010:** The maximum length of the project description must not exceed 65535 characters (MEDIUMTEXT).

### Project Editing:
* **FR-011:** The user must be able to edit the name and description of an existing project.
* **FR-012:** The project name must be a mandatory field when editing.
* **FR-013:** The system must display a success message after the project is updated.
* **FR-014:** Changes to the project must be reflected in the project list.
* **FR-015:** The system must prevent changing a project's name to one that already exists for the current user.

### Project Deletion:
* **FR-016:** The user must be able to delete an existing project.
* **FR-017:** The system must prompt for confirmation before deleting a project.
* **FR-018:** After deletion, the project must not appear in the user's project list.
* **FR-019:** Deleting a project must result in the deletion of all associated tasks.
* **FR-020:** The system must display a success message after the project is deleted.

---

## Environment Setup & Tooling Installation

To set up the development and testing environment, please install and configure the following tools:

* Python 3.11
* Git
* IntelliJ IDEA/PyCharm
* Docker Desktop

## System Under Test (SUT) Environment Setup
*This section outlines how to set up the `getontracks.org` application and its dependencies using Docker Compose.*

Before using the following commands, ensure Docker Desktop is running.

- **Start the Services**
  1. Open the terminal in the same directory where your docker-compose.yml file is located.
  2. Run the following command:
    ```bash
    docker compose up -d
    ```
  
- **Check the Status**
  To verify that all services are up and running, use:
    ```bash
    docker compose ps
    ```
- **Stop and Remove the Services (When You're Done)**
  To stop and remove all containers, networks, and volumes created by Docker Compose, use:
    ```bash
    docker compose down -v
    ```


Technical task -----------------------------------------------------------------------------------------------------------------------------------------
## Test Automation Tasks

### Practical Automation Tasks

* **Develop a comprehensive suite of automated UI and API tests for the 'Projects' functionality of the `getontracks.org` service, in accordance with the functional requirements outlined in the description.**
* Provide results as a project in a `.zip` archive.
* **Ensure** that the created tests can be run using Pytest commands and that they produce clear output.

---

### Recommended Project Structure

```
getontracks-tests/
│
├── tests/
│   └── ui/                 # UI tests package
│       ├── conftest.py     # fixtures and WebDriver setup
│       └── test_projects_ui.py # UI tests for Projects (Selenium)
├── utils/                  # helper modules
│
├── data/                   # test data files
│   └── project_payloads.json
├── requirements.txt        # pytest, httpx, selenium, pytest-html, etc.
└── docker-compose.yml      # to start getontracks.org service
```

### 1. Setup

1. Unzip the provided archive into `getontracks-tests/`.
2. Create and activate a Python 3.11 virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the SUT (System Under Test):
   ```bash
   docker compose up -d
   ```

### 2. Run UI Tests

```bash
pytest tests/ui -v
``` 

### 3. Generate Reports (optional)

- Console output (detailed):
  ```bash
  pytest -v
  ```
- HTML report:
  ```bash
  pytest --html=report.html --self-contained-html
  ```

### 4. Package and Submit

1. Develop a comprehensive suite of automated UI tests for the 'Projects' functionality of the `getontracks.org` service, in accordance with the functional requirements outlined in the description.
