from splinter import Browser
from flask import Flask
import pytest

app = Flask(__name__)
app.config['TESTING'] = True
app.config['LIVESERVER_PORT'] = 5000
app.config['LIVESERVER_TIMEOUT'] = 10

@pytest.fixture(scope="module")
def browser():
    with Browser("chrome", headless=True) as browser:
        yield browser

@pytest.fixture(scope="module")
def live_server():
    server = app.run(port=5000)
    yield server
    server.teardown_appcontext()

def test_add_ta(browser, live_server):
    browser.visit('http://localhost:5000/api/login')
    browser.fill('username', 'admin')
    browser.fill('password', 'admin')
    browser.find_by_text('Sign In').click()
    assert browser.status_code.is_success()
    browser.visit('http://localhost:5000/api/ta')
    browser.fill('id', '1')
    browser.fill('native_english_speaker', 'True')
    browser.fill('course_instructor', 'John Smith')
    browser.fill('course', 'CS101')
    browser.fill('semester', 'Spring')
    browser.fill('class_size', '25')
    browser.fill('performance_score', '4.5')
    browser.find_by_text('Add TA').click()
    assert browser.status_code.is_success()

def test_update_ta(browser, live_server):
    browser.visit('http://localhost:5000/api/login')
    browser.fill('username', 'admin')
    browser.fill('password', 'admin')
    browser.find_by_text('Sign In').click()
    assert browser.status_code.is_success()
    browser.visit('http://localhost:5000/api/ta/1')
    browser.fill('native_english_speaker', 'False')
    browser.fill('course_instructor', 'Jane Doe')
    browser.find_by_text('Update TA').click()
    assert browser.status_code.is_success()

def test_get_ta(browser, live_server):
    browser.visit('http://localhost:5000/api/login')
    browser.fill('username', 'admin')
    browser.fill('password', 'admin')
    browser.find_by_text('Sign In').click()
    assert browser.status_code.is_success()
    browser.visit('http://localhost:5000/api/ta/1')
    assert browser.status_code.is_success()

def test_delete_ta(browser, live_server):
    browser.visit('http://localhost:5000/api/login')
    browser.fill('username', 'admin')
    browser.fill('password', 'admin')
    browser.find_by_text('Sign In').click()
    assert browser.status_code.is_success()
    browser.visit('http://localhost:5000/api/ta/1')
    browser.find_by_text('Delete TA').click()
    assert browser.status_code.is_success()
