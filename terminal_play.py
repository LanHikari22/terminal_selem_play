# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from typing import Tuple
import sys
from os import path
import json

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        self.replay_file = g_replay_file

        email, passwd = self.loadAuth()
        self.email = email
        self.passwd = passwd

        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.duckduckgo.com/"
        self.verificationErrors = []
        self.accept_next_alert = True


    def loadAuth(self) -> Tuple[str, str]:
        # find path in project directory or relative
        secret_filename = 'c1terminal.secret'
        secret_path = ''
        if path.exists(path.relpath(secret_filename)):
            secret_path = path.relpath(secret_filename)
        elif path.exists(path.join(path.dirname(__file__), secret_filename)):
            secret_path = path.join(path.dirname(__file__), secret_filename)
        if secret_path == '':
            print('error: could not find {} to fetch auth data from'.format(secret_filename))
        else:
            print('fetching auth data from {}'.format(secret_path))

        with open(secret_path) as authdata:
            jdata = json.load(authdata)
            return (jdata['email'], jdata['password'])

    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("https://terminal.c1games.com/")
        driver.find_element_by_id("ledger-signup-btn").click()
        driver.find_element_by_id("id_login").click()
        driver.find_element_by_id("id_login").clear()
        driver.find_element_by_id("id_login").send_keys(self.email)
        driver.find_element_by_xpath("//html[@id='index-page']/body/div/div/div/div[2]/div").click()
        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.passwd)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Play").click()
        driver.find_element_by_xpath("//div[@id='playground_config']/div/button").click()
        driver.find_element_by_name("replayFiles").clear()
        driver.find_element_by_name("replayFiles").send_keys(self.replay_file)
        driver.find_element_by_xpath("//div[@id='upload-replay']/div/i").click()
    
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
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)


def print_usage():
    print("\n\tusage: {} replay_file".format(sys.argv[0]))


if __name__ == "__main__":
    global g_replay_file
    if len(sys.argv) != 2:
        print_usage()
        exit(1)
    g_replay_file = path.abspath(sys.argv[1])
    if not path.exists(g_replay_file):
        print('error: could not find {}'.format(g_replay_file))
        exit(1)

    sys.argv = sys.argv[:1]
    unittest.main()
