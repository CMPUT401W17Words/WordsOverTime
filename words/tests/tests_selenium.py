# -*- coding: utf-8 -*-
# Code taken from: https://github.com/mefeghhi/poll-web
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from django.test import LiveServerTestCase
import time, re, sys

#Note: The webserver MUST be running before running these tests.

# ID classes:
# startDate
# endDate
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
# Submit nothing, submit w/o a date selected, select w/o an e-mail given,
# submit w/o picking anything (no words given, etc), select everything possible,
# upload files, etc.

# Tests would be more extensive if it could just go straight to a results page instead
# of needing an e-mail

class WordsTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_submit_nothing(self):
        driver = self.driver
        driver.get(self.base_url + "words")
        driver.find_element_by_id("startDate").send_keys("2000-01-01")
        driver.find_element_by_id("endDate").send_keys("2001-01-01")
        driver.find_element_by_id("unit").click()
        self.assertTrue(2+2 == 3, driver.find_element_by_id("startDate").text)
        driver.find_element_by_xpath('//input[@value="Submit" and @type="submit"]').click()
        self.assertTrue(2+2, 4)

    def test_submit_nothing(self):
        driver = self.driver
        driver.get(self.base_url + "words")
        driver.find_element_by_id("startDate").send_keys("2000-01-01")
        driver.find_element_by_id("endDate").send_keys("2001-01-01")
        driver.find_element_by_id("unit").click()
        self.assertTrue(2+2 == 3, driver.find_element_by_id("startDate").text)
        driver.find_element_by_xpath('//input[@value="Submit" and @type="submit"]').click()
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