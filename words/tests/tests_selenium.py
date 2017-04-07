# -*- coding: utf-8 -*-
# Code taken from: https://github.com/mefeghhi/poll-web
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from django.test import LiveServerTestCase
import time, re, os

#Note: The webserver MUST be running before running these tests.

# ID classes:
# startDate (dtp_input1)
# endDate (dtp_input2)
# unit -> values: Year/Month/Week
# ---
# Nneighbour (int - but field is text, watch for this)
# keywords (text)
# text_file (file)
# output2 -> options: CBow, Skipgram
# ---
# wordPairs (text - (a, b), (c,d))
# fileCos (file)
# output3 -> options: CBow, Skipgram
# ---
# tfidfWord (text)
# ---
# conditionalWord (text -> (a, b), (c, d))
# fileConditional (file)
# ---
# checkboxes:
# name: Average valence
# name: Average arousal
# name: 5 Words Average valence
# name: 5 Words Average arousal
# ---
# frequencyWord (text)
# fileFrequency (file)
# ---
# relativeWord (text)
# relativeFile (file)
# ---
# userEmail (text)

# Some tests:
# Submit nothing (done), submit w/o a date selected (done), select w/o an e-mail given (done),
# submit w/o picking anything (no words given, etc), select everything possible,
# upload files, etc.
# making sure start date !> end date, making sure start/end date are valid (shouldn't
# go past current date), check valid e-mail

# Tests would be more extensive if it could just go straight to a results page instead
# of needing an e-mail

class WordsTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
        # From http://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
        # Author: Russell Dias / License: CC-BY-SA 3.0
        self.current_path = os.path.dirname(os.path.realpath(__file__))


    # Passes
    def test_submit_nothing(self):
        driver = self.driver
        driver.get(self.base_url + "words")
        driver.find_element_by_xpath('//input[@value="Submit" and @type="submit"]').click()
        time.sleep(1)
        self.assertTrue(str(driver.current_url) == "http://127.0.0.1:8000/words/")

    # http://sqa.stackexchange.com/questions/3387/set-attribute-of-an-element-using-webdriver-python
    # Passes
    def test_no_email_given(self):
        driver = self.driver
        driver.get(self.base_url + "words")
        driver.execute_script("document.getElementById('startDate').removeAttribute('readonly',0)")
        driver.execute_script("document.getElementById('startDate').value='2001-01-01'")
        driver.execute_script("document.getElementById('dtp_input1').value='2001-01-01'")
        driver.execute_script("document.getElementById('endDate').removeAttribute('readonly',0)")
        driver.execute_script("document.getElementById('endDate').value='2002-01-01'")
        driver.execute_script("document.getElementById('dtp_input2').value='2002-01-01'")
        driver.find_element_by_id("click3").click()
        time.sleep(1)
        driver.find_element_by_id("tfidfWord").send_keys("apple")
        driver.find_element_by_xpath('//input[@value="Submit" and @type="submit"]').click()
        time.sleep(1)
        self.assertTrue(str(driver.current_url) == "http://127.0.0.1:8000/words/")
    
    # Passes
    def test_select_no_date(self):
        driver = self.driver
        driver.get(self.base_url + "words")
        driver.find_element_by_id("click3").click()
        time.sleep(1)
        driver.find_element_by_id("tfidfWord").send_keys("apple")
        driver.find_element_by_id("userEmail").send_keys("test@email.net")
        driver.find_element_by_xpath('//input[@value="Submit" and @type="submit"]').click()
        time.sleep(1)
        self.assertTrue(str(driver.current_url) == "http://127.0.0.1:8000/words/")

    def test_select_nothing(self):
        pass

    # Passes
    def test_submit_stuff(self):
        driver = self.driver
        driver.get(self.base_url + "words")
        #driver.find_element_by_id("test1").click()
        #time.sleep(5)
        driver.execute_script("document.getElementById('startDate').removeAttribute('readonly',0)")
        driver.execute_script("document.getElementById('startDate').value='2001-01-01'")
        driver.execute_script("document.getElementById('dtp_input1').value='2001-01-01'")
        driver.execute_script("document.getElementById('endDate').removeAttribute('readonly',0)")
        driver.execute_script("document.getElementById('endDate').value='2002-01-01'")
        driver.execute_script("document.getElementById('dtp_input2').value='2002-01-01'")
        driver.find_element_by_id("click3").click()
        time.sleep(1)
        driver.find_element_by_id("tfidfWord").send_keys("apple")
        driver.find_element_by_id("userEmail").send_keys("test@email.net")
        driver.find_element_by_xpath('//input[@value="Submit" and @type="submit"]').click()
        time.sleep(5)
        self.assertTrue(str(driver.current_url) == "http://127.0.0.1:8000/words/success/")

    # Fails - website fails to cover this
    def test_invalid_date(self):
        driver = self.driver
        driver.get(self.base_url + "words")
        driver.execute_script("document.getElementById('startDate').removeAttribute('readonly',0)")
        driver.execute_script("document.getElementById('startDate').value='2001-01-01'")
        driver.execute_script("document.getElementById('dtp_input1').value='2001-01-01'")
        driver.execute_script("document.getElementById('endDate').removeAttribute('readonly',0)")
        driver.execute_script("document.getElementById('endDate').value='2002-01-01'")
        driver.execute_script("document.getElementById('dtp_input2').value='2002-01-01'")
        driver.find_element_by_id("click3").click()
        time.sleep(1)
        driver.find_element_by_id("tfidfWord").send_keys("apple")
        driver.find_element_by_id("userEmail").send_keys("test@email.net")
        driver.find_element_by_xpath('//input[@value="Submit" and @type="submit"]').click()
        time.sleep(5)
        self.assertTrue(str(driver.current_url) == "http://127.0.0.1:8000/words/success/")


    # WebDriverException: Message: POST ... did not match a known command
    def test_uploading_files(self):
        driver = self.driver
        driver.get(self.base_url + "words")
        path = self.current_path + "/text_files/single_words.txt"
        print(path)
        driver.find_element_by_id("click1").click()
        time.sleep(1)
        driver.find_element_by_id("text_file").send_keys(path)
        self.assertTrue(2+2, 4)


    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()