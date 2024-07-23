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
        self.companyName = "Stroud Council"
        self.ownerUsername = "stroud"
        self.scrapPageURL = "https://www.stroud.gov.uk/jobs"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#page_body"))
        )

        # Scraper Function

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#page_body .content .col-md-8 h3")
            containerNumber = 1
            for jobContainer in jobContainers:
                title = jobContainer.text
                self.job.setTitle(title)

                link = self.chrome.find_element_by_css_selector("#page_body .content h3:nth-of-type("+str(containerNumber)+") ~ a").get_attribute("href")
                self.job.setLink(link)

                jobdatas = self.chrome.find_element_by_css_selector("#page_body .content h3:nth-of-type("+str(containerNumber)+") ~ p").text
                jobdatas = jobdatas.splitlines()
                salary = jobdatas[0].split("Salary:")[1].strip()
                self.job.setSalary(salary)

                expireDate = jobdatas[2].split("Closing date:")[1].strip()
                possibleExpiryDateFormats = [
                    "%A %d %b %Y",
                    "%d %B %Y",
                    "%dth %B %Y",
                    "%dnd %B %Y",
                    "%drd %B %Y",
                ]

                formattedExpireDate = None
                for expiryDateFormat in possibleExpiryDateFormats:
                    try:
                        formattedExpireDate = datetime.strptime(expireDate, expiryDateFormat).strftime('%Y-%m-%d')
                        break
                    except:
                        pass

                if formattedExpireDate is None:
                    exception_message = str(title) + ' : Unknown expiry date format ' + expireDate + "\n"
                    self.exceptionLogging('warning', exception_message)
                else:
                    self.job.setExpireDate(formattedExpireDate)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

                containerNumber = containerNumber + 1

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                availableDescriptionClasses = [
                    ".job-description",
                    ".details__descr-text",
                    ".alert-jobadvert",
                ]

                description = None
                for descriptionClass in availableDescriptionClasses:
                    try:
                        description = self.chrome.find_element_by_css_selector(descriptionClass).get_attribute("innerHTML")
                        break
                    except:
                        pass

                if description is None:
                    exception_message = str(title) + ' : Selector for description is unknown.'
                    self.exceptionLogging('warning', exception_message)
                else:
                    self.jobs[currentJobIndex].setDescription(description)
 
            return True
        except:
            self.exceptionLogging()
            return False