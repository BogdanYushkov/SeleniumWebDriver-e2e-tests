import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_FR_001_project_visible_in_ui(driver, base_url, unique_project_name, login):
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    driver.find_element(By.ID, "project_name").send_keys(unique_project_name)

    driver.find_element(By.ID, "project_new_project_submit").click()

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )
    flash_message = driver.find_element(By.ID, "flash").text
    assert "Created new project" in flash_message or "successfully" in flash_message

    time.sleep(1)
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "list-active-projects"))
    )
    project_list = driver.find_element(By.ID, "list-active-projects")

    assert unique_project_name in project_list.text, f"'{unique_project_name}' not found in:\n{project_list.text}"



def test_FR_002_project_name_and_status_ui(driver, base_url, unique_project_name, login):
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "project_name"))
    )
    driver.find_element(By.ID, "project_name").send_keys(unique_project_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )
    flash = driver.find_element(By.ID, "flash").text
    assert unique_project_name in flash or "Created new project" in flash

    time.sleep(1)
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "list-active-projects"))
    )
    project_list = driver.find_element(By.ID, "list-active-projects").text

    print("\n--- PROJECT LIST ---")
    print(project_list)

    assert unique_project_name in project_list, f"'{unique_project_name}' not found in:\n{project_list}"
    assert "(0 actions)" in project_list, "Expected status '(0 actions)' not found"



def test_FR_003_redirects_to_login_if_not_authenticated(driver, base_url):

    driver.delete_all_cookies()
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "user_login")))
    assert "Please log in" in driver.page_source



def test_FR_004_create_project_via_ui(driver, base_url, unique_project_name, login):
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    driver.find_element(By.ID, "project_name").send_keys(unique_project_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//a[text()='{unique_project_name}']"))
    )

    project_list = driver.find_element(By.ID, "list-active-projects")
    assert unique_project_name in project_list.text



def test_FR_005_project_name_required_ui(driver, base_url, login):
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))

    project_name_input = driver.find_element(By.ID, "project_name")
    project_name_input.clear()

    driver.find_element(By.ID, "project_new_project_submit").click()

    assert driver.current_url.endswith("/projects")

    assert project_name_input.get_attribute("value") == ""




def test_FR_006_project_success_message_ui(driver, base_url, unique_project_name, login):
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    driver.find_element(By.ID, "project_name").send_keys(unique_project_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.ID, "flash").is_displayed() and d.find_element(By.ID, "flash").text.strip() != ""
    )
    success_message = driver.find_element(By.ID, "flash").text.strip()

    assert unique_project_name in success_message


def test_FR_007_created_project_visible_in_list(driver, base_url, unique_project_name, login):
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    driver.find_element(By.ID, "project_name").send_keys(unique_project_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )
    flash = driver.find_element(By.ID, "flash").text
    assert unique_project_name in flash or "Created new project" in flash

    time.sleep(1)
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "list-active-projects")))
    project_list = driver.find_element(By.ID, "list-active-projects").text

    print("\n--- PROJECT LIST ---")
    print(project_list)

    assert unique_project_name in project_list, f"'{unique_project_name}' not found in:\n{project_list}"



def test_FR_008_prevent_duplicate_project_names_ui(driver, base_url, unique_project_name, login):
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))

    driver.find_element(By.ID, "project_name").send_keys(unique_project_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    WebDriverWait(driver, 10).until(
        lambda d: unique_project_name in d.find_element(By.ID, "list-active-projects").text
    )

    driver.find_element(By.ID, "project_name").clear()
    driver.find_element(By.ID, "project_name").send_keys(unique_project_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    assert driver.current_url.endswith("/projects")
    assert driver.find_element(By.ID, "project_name").get_attribute("value") == unique_project_name

def test_FR_009_project_name_max_length_ui(driver, base_url, login):
    driver.get(f"{base_url}/projects")

    long_name = "x" * 256
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    driver.find_element(By.ID, "project_name").send_keys(long_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "errorExplanation"))
    )
    error_box = driver.find_element(By.ID, "errorExplanation").text

    assert "Name project name must be less than 256 characters" in error_box

# FR-010: This test assumes that the project description should be limited to 65535 characters.
# However, currently the application does not enforce this limit, so this test is expected to fail
# or may not trigger any validation error.

def test_FR_010_project_description_max_length_ui(driver, base_url, unique_project_name, login):
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "project_name")))
    driver.find_element(By.ID, "project_name").send_keys(f"{unique_project_name}_valid")

    long_description = "x" * 70000

    driver.execute_script(
        f"document.getElementById('project_description').value = '{long_description}';"
    )

    driver.find_element(By.ID, "project_new_project_submit").click()

    error_box = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "errorExplanation"))
    )

    assert "description" in error_box.text.lower() or "too long" in error_box.text.lower()


def test_FR_011_edit_project_name_and_description_ui(driver, base_url, unique_project_name, login):
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    driver.find_element(By.ID, "project_name").send_keys(unique_project_name)
    driver.find_element(By.ID, "project_description").send_keys("Initial description")
    driver.find_element(By.ID, "project_new_project_submit").click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "list-active-projects")))

    project_blocks = driver.find_elements(By.CSS_SELECTOR, "#list-active-projects .project")
    for block in project_blocks:
        if unique_project_name in block.text:
            edit_button = block.find_element(By.CSS_SELECTOR, "a[id^='link_edit_project_']")
            edit_button.click()
            break

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "project_name"))
    )

    new_name = unique_project_name + "_edited"
    new_description = "Updated description"

    name_input = driver.find_element(By.ID, "project_name")
    description_input = driver.find_element(By.ID, "project_description")

    name_input.clear()
    name_input.send_keys(new_name)

    description_input.clear()
    description_input.send_keys(new_description)

    name_input.submit()

    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "list-active-projects")))
    project_list = driver.find_element(By.ID, "list-active-projects").text

    assert new_name in project_list

def test_FR_012_edit_project_has_name_field(driver, base_url, unique_project_name, login):
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    driver.find_element(By.ID, "project_name").send_keys(unique_project_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    WebDriverWait(driver, 10).until(lambda d: "Created new project" in d.page_source)

    driver.get(f"{base_url}/projects")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "list-active-projects")))

    projects = driver.find_elements(By.CSS_SELECTOR, "#list-active-projects .project")
    for project in projects:
        if unique_project_name in project.text:
            edit_button = project.find_element(By.CSS_SELECTOR, ".project_edit_settings")
            edit_button.click()
            break
    else:
        pytest.fail(f"Project '{unique_project_name}' not found in list")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))

def test_FR_013_success_message_after_update_ui(driver, base_url, unique_project_name, login):
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    driver.find_element(By.ID, "project_name").send_keys(unique_project_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    WebDriverWait(driver, 10).until(lambda d: "Created new project" in d.page_source)

    driver.get(f"{base_url}/projects")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "list-active-projects")))

    projects = driver.find_elements(By.CSS_SELECTOR, "#list-active-projects .project")
    for project in projects:
        if unique_project_name in project.text:
            project.find_element(By.CSS_SELECTOR, ".project_edit_settings").click()
            break
    else:
        pytest.fail("Project not found for editing")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_description")))
    driver.find_element(By.ID, "project_description").send_keys(" updated")

    driver.find_element(By.CSS_SELECTOR, "button[id^='submit_project_']").click()

    WebDriverWait(driver, 10).until(
        lambda d: "Project saved" in d.find_element(By.ID, "flash").text.strip())



def test_FR_014_project_changes_reflected_in_list_ui(driver, base_url, unique_project_name, login):
    driver.get(f"{base_url}/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    driver.find_element(By.ID, "project_name").send_keys(unique_project_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    WebDriverWait(driver, 10).until(lambda d: "Created new project" in d.page_source)

    driver.get(f"{base_url}/projects")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "list-active-projects")))

    projects = driver.find_elements(By.CSS_SELECTOR, "#list-active-projects .project")
    for project in projects:
        if unique_project_name in project.text:
            project.find_element(By.CSS_SELECTOR, ".project_edit_settings").click()
            break
    else:
        pytest.fail(f"Project '{unique_project_name}' not found in project list")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_description")))
    desc_input = driver.find_element(By.ID, "project_description")
    desc_input.clear()
    desc_input.send_keys("Updated description")

    driver.find_element(By.CSS_SELECTOR, "button[id^='submit_project_']").click()
    WebDriverWait(driver, 10).until(lambda d: "Project saved" in d.page_source)

    driver.get(f"{base_url}/projects")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "list-active-projects")))
    project_list_text = driver.find_element(By.ID, "list-active-projects").text

    assert unique_project_name in project_list_text, f"'{unique_project_name}' not found in project list after update"



def test_FR_015_prevent_duplicate_name_on_edit_ui(driver, base_url, login):
    driver.get(f"{base_url}/projects")

    reserved_name = "fr_015_reserved"
    temp_name = "fr_015_temp"

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    name_input = driver.find_element(By.ID, "project_name")

    name_input.clear()
    name_input.send_keys(reserved_name)
    driver.find_element(By.ID, "project_new_project_submit").click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "flash")))

    name_input = driver.find_element(By.ID, "project_name")
    name_input.clear()
    name_input.send_keys(temp_name)
    driver.find_element(By.ID, "project_new_project_submit").click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "flash")))

    time.sleep(1)
    driver.get(f"{base_url}/projects")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "list-active-projects")))

    projects = driver.find_elements(By.CSS_SELECTOR, "#list-active-projects .project")
    for project in projects:
        if temp_name in project.text:
            try:
                project.find_element(By.CLASS_NAME, "project_edit_settings").click()
                break
            except:
                pytest.fail(f"Edit button not found for project '{temp_name}'")
    else:
        project_texts = "\n".join(p.text for p in projects)
        pytest.fail(f"Project '{temp_name}' not found in the list:\n{project_texts}")

    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.ID, "project_name").get_attribute("value") == temp_name
    )

    name_input = driver.find_element(By.ID, "project_name")
    name_input.clear()
    name_input.send_keys(reserved_name)
    driver.find_element(By.CSS_SELECTOR, "button[id^='submit_project_']").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "errorExplanation"))
    )
    error_text = driver.find_element(By.ID, "errorExplanation").text
    assert "Name already exists" in error_text


def test_FR_017_confirm_before_deleting_project(driver, base_url, login):
    driver.get(f"{base_url}/projects")
    project_name = "fr_017_deletable"

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    name_input = driver.find_element(By.ID, "project_name")
    name_input.clear()
    name_input.send_keys(project_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "flash")))
    flash_text = driver.find_element(By.ID, "flash").text
    assert project_name in flash_text or "Created new project" in flash_text

    time.sleep(1)
    driver.get(f"{base_url}/projects")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "list-active-projects")))

    projects = driver.find_elements(By.CSS_SELECTOR, "#list-active-projects .project")
    for project in projects:
        if project_name in project.text:
            delete_btn = project.find_element(By.CLASS_NAME, "delete_project_button")
            delete_btn.click()
            break
    else:
        all_text = "\n".join(p.text for p in projects)
        pytest.fail(f"Project '{project_name}' not found in the list:\n{all_text}")

    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert "Are you sure" in alert.text
    assert project_name in alert.text

    alert.dismiss()

    time.sleep(1)
    driver.refresh()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "list-active-projects")))
    remaining_projects = driver.find_elements(By.CSS_SELECTOR, "#list-active-projects .project")

    assert any(project_name in p.text for p in remaining_projects), \
        "Project was deleted after dismissing the confirmation"


def test_FR_018_deleted_project_disappears_from_list(driver, base_url, login):
    driver.get(f"{base_url}/projects")
    project_name = "fr_018_to_be_deleted"

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    name_input = driver.find_element(By.ID, "project_name")
    name_input.clear()
    name_input.send_keys(project_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    time.sleep(1)
    driver.get(f"{base_url}/projects")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "list-active-projects")))

    time.sleep(1)
    projects = driver.find_elements(By.CSS_SELECTOR, "#list-active-projects .project")
    for project in projects:
        if project_name in project.text:
            delete_btn = project.find_element(By.CLASS_NAME, "delete_project_button")
            delete_btn.click()
            break
    else:
        pytest.fail(f"Project '{project_name}' not found in the list")

    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert "Are you sure" in alert.text
    alert.accept()

    time.sleep(1)
    driver.refresh()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "list-active-projects")))
    remaining_projects = driver.find_elements(By.CSS_SELECTOR, "#list-active-projects .project")

    assert all(project_name not in p.text for p in remaining_projects), \
        f"Project '{project_name}' still appears in the list after deletion"


#FR_19 skip because I don't understand the task and app functionality

def test_FR_020_success_message_after_deletion(driver, base_url, login):
    driver.get(f"{base_url}/projects")
    project_name = "fr_020_success_message"

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "project_name")))
    name_input = driver.find_element(By.ID, "project_name")
    name_input.clear()
    name_input.send_keys(project_name)
    driver.find_element(By.ID, "project_new_project_submit").click()

    time.sleep(1)
    driver.get(f"{base_url}/projects")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "list-active-projects")))

    time.sleep(1)
    projects = driver.find_elements(By.CSS_SELECTOR, "#list-active-projects .project")
    for project in projects:
        if project_name in project.text:
            delete_btn = project.find_element(By.CLASS_NAME, "delete_project_button")
            delete_btn.click()
            break
    else:
        pytest.fail(f"Project '{project_name}' not found")

    WebDriverWait(driver, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )

    flash = driver.find_element(By.ID, "flash")
    assert project_name in flash.text and "Deleted project" in flash.text, \
        f"Unexpected or missing success message: '{flash.text}'"
