# Required Packages
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage=None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Avon & Somerset Police"
        self.ownerUsername = "talentevents"
        self.scrapPageURL = "https://asp.tal.net/vx/lang-en-GB/mobile-0/appcentre-External/brand-3/candidate/jobboard/vacancy/14/adv/"
        self.feedType = self.feedTypeWebScrap
        self.jobKey = 'title'

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#tile-results-list"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#tile-results-list li")
            for jobContainer in jobContainers:
                link = jobContainer.find_element_by_css_selector(".candidate-opp-tile h3 a").get_attribute('href')
                self.job.setLink(link)

                title = jobContainer.find_element_by_css_selector(".candidate-opp-tile h3 a").text
                self.job.setTitle(title)

                location = jobContainer.find_element_by_css_selector(".candidate-opp-tile .candidate-opp-field-3").text
                location = location.split(":")[1].strip()
                self.job.setLocation(location)


                expireDate = jobContainer.find_element_by_css_selector(".candidate-opp-tile .candidate-opp-field-4").text
                expireDate = expireDate.split("Closing Date:")[1].strip()

                possibleExpiryDateFormats = [
                    "%d %b %Y %H:%M GMT",
                    "%d %b %Y %H:%M BST"
                ]
                for possibleExpireDate in possibleExpiryDateFormats:
                    try:
                        expireDate = datetime.strptime(expireDate, possibleExpireDate).strftime('%Y-%m-%d')
                        self.job.setExpireDate(expireDate)
                    except Exception as e:
                        exception_message = str(title) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)

                hasSalary = bool(jobContainer.find_elements_by_css_selector(".candidate-opp-tile .candidate-opp-field-5"))
                if hasSalary:
                    salary = jobContainer.find_element_by_css_selector(".candidate-opp-tile .candidate-opp-field-5").text
                    salary = salary.split(":")[1].strip()
                    self.job.setSalary(salary)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector(".form_section .htmltype-textarea").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False