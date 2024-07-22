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
        self.companyName = "Immediate"
        self.ownerUsername = "immediatemedia"
        self.scrapPageURL = "https://careers-immediatemedia.icims.com/jobs/search?ss=1"
        self.jobTrackingVariable = "mode=job&iis=Job+Board&iisn=<site_domain>"
        self.feedType = self.feedTypeWebScrap
        self.maxScrapPageLimit = 20
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        self.chrome.switch_to.frame(0)
        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".iCIMS_ListingsPage  "))
        )


    def nextPage(self):
        try:
            next_button = self.chrome.find_element_by_css_selector('.iCIMS_Paging > a:nth-last-child(2)')
        except:
            return False

        has_next_page = next_button.get_attribute("class") != 'glyph invisible'
        if has_next_page:
            next_button.click()
            time.sleep(3)
            WebDriverWait(self.chrome, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".iCIMS_Paging a"))
            )
            return has_next_page
        else:
            return False

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try:
            while True:
                jobContainers = self.chrome.find_elements_by_css_selector(".iCIMS_JobsTable > .row")

                for jobContainer in jobContainers:
                    title = str(jobContainer.find_element_by_css_selector(".title .iCIMS_Anchor h2").text)
                    title = title.strip()
                    self.job.setTitle(title)

                    link = jobContainer.find_element_by_css_selector(".title .iCIMS_Anchor").get_attribute("href")
                    self.job.setLink(link, self.jobTrackingVariable)

                    self.job.hasExpireDate = bool(jobContainer.find_elements_by_css_selector(".additionalFields dd"))

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

                if self.nextPage():
                    pass
                else:
                    break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                self.chrome.switch_to.frame(0)

                location = self.chrome.find_element_by_css_selector(".iCIMS_JobsTable .col-xs-6.header.left span:last-child").text
                self.jobs[currentJobIndex].setLocation(location)

                if job.hasExpireDate:
                    expireDate = self.chrome.find_element_by_css_selector(".additionalFields dl:nth-of-type(2) dd.iCIMS_JobHeaderData").text
                    try:
                        expireDate = datetime.strptime(expireDate, "%d/%m/%Y").strftime('%Y-%m-%d')
                        self.jobs[currentJobIndex].setExpireDate(expireDate)
                    except Exception as e:
                        exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)

                tableElement = self.chrome.find_element_by_css_selector(".iCIMS_JobsTable")
                logoElement = self.chrome.find_element_by_css_selector(".iCIMS_Logo")
                optionsElement = self.chrome.find_element_by_css_selector(".iCIMS_JobOptions")
                elementToRemove = [tableElement, logoElement, optionsElement]
                self.sanitizeElementsForDescription(elementToRemove)

                descriptionElement = self.chrome.find_element_by_class_name("iCIMS_JobContent")
                description = descriptionElement.get_attribute('innerHTML')

                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

