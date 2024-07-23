# Required Packages
from Resource import htmlmin
import time
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
        self.companyName = "Hyde"
        self.ownerUsername = "hyde"
        self.scrapPageURL = "https://www.hyde-housing.co.uk/careers/search-and-apply/job-vacancies/"
        self.jobIndicesToRemove = []
        self.feedType = self.feedTypeWebScrap
        self.jobKey = 'title'

        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#main_content .m-vacancies"))
        )

        # Scraper Function

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector(".m-vacancies .m-vacancies__vacancy")
            for jobContainer in jobContainers:
                link = self.scrapPageURL
                self.job.setLink(link)

                title = jobContainer.find_element_by_css_selector(".m-vacancies__content_wrapper .m-vacancies__heading").text
                self.job.setTitle(title)

                listItems = jobContainer.find_elements_by_css_selector(".m-vacancies__list .m-vacancies__list_item")
                for listItem in listItems:
                    listItemMetaName = listItem.find_element_by_css_selector(".m-vacancies__metaname").text
                    if 'Location' in listItemMetaName:
                        location = listItem.find_element_by_css_selector(".m-vacancies__metavalue").text
                        self.job.setLocation(location)
                    elif 'Salary' in listItemMetaName:
                        salary = listItem.find_element_by_css_selector(".m-vacancies__metavalue").text
                        self.job.setSalary(salary)
                    elif 'Application close' in listItemMetaName:
                        expireDate = listItem.find_element_by_css_selector(".m-vacancies__metavalue").text

                        possibleExpiryDateFormats = [
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
                            exception_message = str(title + ' : Unknown expiry date format ' + expireDate + "\n")
                            self.exceptionLogging('warning', exception_message)
                        else:
                            self.job.setExpireDate(formattedExpireDate)

                self.chrome.clickElement(jobContainer.find_element_by_css_selector(".m-vacancies__expand_wrapper"))

                description = jobContainer.find_element_by_css_selector(".m-vacancies__body").get_attribute("innerHTML")
                self.job.setDescription(description)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            return True
        except:
            self.exceptionLogging()
            return False