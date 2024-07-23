# Required Packages
from datetime import datetime
from Resource import htmlmin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re as regex

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Walton Centre NHS Foundation Trust"
        self.ownerUsername = "waltoncentrenhsfoundationtrust"
        self.scrapPageURL = "https://www.jobs.nhs.uk/extsearch?client_id=120725"
        self.location = "Liverpool"
        self.feedType = self.feedTypeWebScrap
        self.maxScrapPageLimit = 20
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        cookie = WebDriverWait(self.chrome, 25).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/form/input[2]"))
        )
        cookie.click()
        WebDriverWait(self.chrome, 55).until(
            EC.presence_of_element_located((By.CLASS_NAME, "resultsContainer"))
        )

    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()
        try :

            jobContainers = WebDriverWait(self.chrome, 30).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.resultsContent.panel .vacancy"))
                         )
            for jobContainer in jobContainers:
                title = str(jobContainer.find_element_by_css_selector('.vacancy > h2 > a').text)
                title = title.strip()
                self.job.setTitle(title)

                contract = jobContainer.find_element_by_css_selector('.vacancy-summary > .left > dl:last-child > dd').text
                contract = contract.strip()
                self.job.setContract(contract)

                salary = jobContainer.find_element_by_css_selector('.vacancy-summary > .left > dl:first-child > dd').text
                salary = salary.strip()
                self.job.setSalary(salary)

                link = jobContainer.find_element_by_css_selector('.vacancy > h2 > a').get_property('href')
                self.job.setLink(link)

                expire = jobContainer.find_element_by_css_selector('.vacancy-summary > .right > dl:first-child > dd').text
                try:
                    expire = datetime.strptime(expire, '%d/%m/%Y').strftime('%Y-%m-%d')
                    self.job.setExpireDate(expire)
                except Exception as e:
                    exception_message = str(self.job.getTitle()) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)

                self.job.setLocation(self.location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                elementsToRemove = []
                elementsToBeRemoved = ['.agencyLogo','.h2Strong','dl.pairedData','table.list','ul.awardList.clear.noPad']
                for element in elementsToBeRemoved:
                    hasElement = bool(self.chrome.find_elements_by_css_selector("#maincontent " + element))
                    if hasElement:
                        elementObjects = self.chrome.find_elements_by_css_selector("#maincontent " + element)
                        for objectToRemove in elementObjects:
                            elementsToRemove.append(objectToRemove)
                self.sanitizeElementsForDescription(elementsToRemove)

                try:
                   description = self.chrome.find_element_by_css_selector('.directApplyVacancyContainer .panel').get_attribute("innerHTML")
                except:
                    description = self.chrome.find_element_by_css_selector(
                        '.info').get_attribute("innerHTML")
                description = regex.sub(r'[^\x00-\x7F]+', ' ', description)

                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False