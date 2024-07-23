# Required Packages
from datetime import datetime
from Resource import htmlmin
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
        self.companyName = "Weetabix"
        self.ownerUsername = "weetabix"
        self.scrapPageURL = "https://apply.workable.com/weetabix/?lng=en#jobs"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 500).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#jobs li[data-ui = 'job']"))
        )

    def loadJobs(self):
        self.loadScrapPage()

        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#jobs li[data-ui = 'job']")
            for jobContainer in jobContainers:
                title = str(jobContainer.find_element_by_css_selector("[data-ui = 'job-title']").text)
                title = title.strip()
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector("a").get_attribute("href")
                self.job.setLink(link)

                location = jobContainer.find_element_by_css_selector("[data-ui = 'job-location']").text
                self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                elementsToRemove = [self.chrome.find_element_by_css_selector("[data-ui = 'apply-button']")]
                self.sanitizeElementsForDescription(elementsToRemove)

                hasExpireDate = bool(self.chrome.find_elements_by_css_selector("[data-ui = 'job-benefits'] > div:nth-child(2) > p:nth-last-child(2) strong"))
                if hasExpireDate:
                    expireDate = self.chrome.find_element_by_css_selector("[data-ui = 'job-benefits'] > div:nth-child(2) > p:nth-last-child(2) strong").text
                    possibleExpiryDateFormats = [
                        "%A %dth %B %Y",
                        "%A %dst %B %Y",
                        "%A %drd %B %Y",
                        "%A %dnd %B %Y",
                        "%dth %B %Y",
                        "%dst %B %Y",
                        "%drd %B %Y",
                        "%dnd %B %Y",
                    ]
                    formattedExpireDate = None
                    for expiryDateFormat in possibleExpiryDateFormats:
                        try:
                            formattedExpireDate = datetime.strptime(expireDate, expiryDateFormat).strftime('%Y-%m-%d')
                            break
                        except:
                            pass

                    if formattedExpireDate is None:
                        exception_message = str(job.getTitle()) + ' : Unknown expiry date format ' + expireDate + "\n"
                        self.exceptionLogging('warning', exception_message)

                    self.jobs[currentJobIndex].setExpireDate(formattedExpireDate)

                description = self.chrome.find_element_by_css_selector("[data-ui = 'job-description']").get_attribute('innerHTML') + self.chrome.find_element_by_css_selector("[data-ui = 'job-requirements']").get_attribute('innerHTML') + self.chrome.find_element_by_css_selector("[data-ui = 'job-benefits']").get_attribute('innerHTML')

                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False
