# Required Packages
from datetime import datetime
from Resource import htmlmin
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Companies.StandardAgent import ScrapAgent

class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Durham University"
        self.ownerUsername = "durham"
        self.location = "Durham"
        self.scrapPageURL = "https://durham.taleo.net/careersection/du_ext/jobsearch.ftl"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.ID, "jobsTableContainer"))
        )

    def nextPage(self):

        has_next_button = bool(self.chrome.find_elements_by_css_selector('#jobPager > .pagersectionpanel:last-child a'))

        if has_next_button:
            next_button = self.chrome.find_element_by_css_selector('#jobPager > .pagersectionpanel:last-child a')
            has_next_page = next_button.get_attribute("class") != "navigation-link-disabled"
            if has_next_page:
                next_button.click()
                time.sleep(3)
                return has_next_page
            else:
                return False

    def loadJobs(self):
        self.loadScrapPage()

        try:

            while True:
                jobContainers = self.chrome.find_elements_by_css_selector("#jobs .jobsbody tr")
                for jobContainer in jobContainers:
                    title = str(jobContainer.find_element_by_css_selector("th[scope = 'row'] a").text)
                    title = title.strip()
                    self.job.setTitle(title)

                    link = jobContainer.find_element_by_css_selector("th[scope = 'row'] a").get_attribute("href")
                    self.job.setLink(link)

                    salary = jobContainer.find_element_by_css_selector("td:nth-of-type(2)").text
                    self.job.setSalary(salary)

                    self.job.setLocation(self.location)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

                if self.nextPage():
                    pass
                else:
                    break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                hasExpireDate = bool(self.chrome.find_elements_by_id("requisitionDescriptionInterface.reqUnpostingDate.row1"))
                checkExpireDate = self.chrome.find_element_by_id("requisitionDescriptionInterface.reqUnpostingDate.row1").text
                checkExpireDate = checkExpireDate[0].isdigit()

                if hasExpireDate and checkExpireDate:
                    expireDate = self.chrome.find_element_by_id("requisitionDescriptionInterface.reqUnpostingDate.row1").text
                    try:
                        if 'AM' in expireDate:
                            expireDate = datetime.strptime(expireDate, '%d-%b-%Y, %H:%M:%S AM')
                        elif 'PM' in expireDate:
                            expireDate = datetime.strptime(expireDate, '%d-%b-%Y, %H:%M:%S PM')
                        expireDate = expireDate.strftime('%Y-%m-%d')
                        self.jobs[currentJobIndex].setExpireDate(expireDate)
                    except Exception as e:
                        exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)



                self.sanitizeElementsForDescription()

                descriptionOuter = self.chrome.find_element_by_id("requisitionDescriptionInterface.descRequisition")
                description = descriptionOuter.find_element_by_css_selector(".editablesection > .contentlinepanel:nth-last-child(3)").get_attribute("innerHTML") + self.chrome.find_element_by_css_selector(".editablesection > .contentlinepanel:nth-last-child(2)").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True


        except:
            self.exceptionLogging()
            return False
