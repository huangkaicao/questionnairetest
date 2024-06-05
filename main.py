from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
from sentence_pool.sentencepool import sentence_pool

def Explicit_Wait_func(element_to_wait_for_id):
    wait = WebDriverWait(driver, 10)

    ele=wait.until(EC.visibility_of_element_located((By.ID, element_to_wait_for_id)))

    if ele.get_attribute("type") == "text":
        wait.until(EC.element_to_be_clickable((By.ID, element_to_wait_for_id)))

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://hkc.com/study ')

# time.sleep(2)
Explicit_Wait_func("divQuestion")

sentence_pool = sentence_pool()

def handle_single_choice(question_div):
    options = question_div.find_elements(By.CSS_SELECTOR, 'div[class*="ui-radio"]')
    unselected_options = [opt for opt in options if 'checked' not in opt.get_attribute('class')]
    if unselected_options:
        random.choice(unselected_options).click()

def handle_multiple_choice(question_div):
    options = question_div.find_elements(By.CSS_SELECTOR, 'div[class*="ui-checkbox"]')
    for option in options:
        if 'checked' not in option.get_attribute('class') and random.choice([True, False]):
            option.click()

def handle_text_input(question_div):
    input_box = question_div.find_element(By.CSS_SELECTOR, 'input[type="text"], textarea')
    if not input_box.get_attribute('value'):
        input_box.send_keys(random.choice(sentence_pool))

def determine_question_type(question_div):
    if question_div.find_elements(By.CSS_SELECTOR, 'input[type="radio"]'):
        return 'single-choice'
    elif question_div.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]'):
        return 'multiple-choice'
    elif question_div.find_elements(By.CSS_SELECTOR, 'input[type="text"], textarea'):
        return 'text-input'
    return 'unknown'

def handle_all_questions():
    all_questions_div = driver.find_element(By.ID, "divQuestion")
    processed_question_ids = set()
    
    while True:
        new_questions_found = False
        questions = all_questions_div.find_elements(By.CSS_SELECTOR, 'div[class*="field ui-field-contain"]')
        
        for question_div in questions:
            question_id = question_div.get_attribute('id')
            if question_id in processed_question_ids:
                continue
            if question_div.value_of_css_property('display') == 'none':
                continue
            
            question_type = determine_question_type(question_div)
            if question_type == 'single-choice':
                handle_single_choice(question_div)
            elif question_type == 'multiple-choice':
                handle_multiple_choice(question_div)
            elif question_type == 'text-input':
                handle_text_input(question_div)
            
            processed_question_ids.add(question_id)
            new_questions_found = True
        
        if not new_questions_found:
            break
        time.sleep(1)

handle_all_questions()

submit_button = driver.find_element(By.ID, "ctlNext")
submit_button.click()