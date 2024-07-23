# Required Packages
import time
from datetime import datetime
import datetime
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
        self.companyName = "DHL Supply Chain"
        self.ownerUsername = "dhlsupplychain"
        self.scrapPageURL = "https://supplychainjobs.dhl.com/jobs/"
        self.feedType = self.feedTypeXML
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-inputs"))
        )

        locationSearch = self.chrome.find_element_by_css_selector(
            "#quicksearch_form #Home_quicksearch_filter_locationradius")
        locationSearch.send_keys("United Kingdom")

        submitButton = self.chrome.find_element_by_css_selector("#quicksearch_SaveButtonRow_formRow .buttonSubmit")
        self.chrome.clickElement(submitButton)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ListGridContainer .rowContainer"))
        )


    def nextPage(self):

        time.sleep(2)
        has_next_button = bool(self.chrome.find_element_by_css_selector('.pagingButtons .scroller_movenext').get_attribute('class') == 'normalanchor ajaxable scroller scroller_movenext buttonEnabled')
        if has_next_button:
            next_button = self.chrome.find_element_by_css_selector('.pagingButtons .scroller_movenext')
            self.chrome.clickElement(next_button)
            time.sleep(3)
            return has_next_button
        else:
            return False



    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()

        try:
            while True:
                time.sleep(5)
                jobContainers = self.chrome.find_elements_by_css_selector(".ListGridContainer .rowContainer")
                for jobContainer in jobContainers:
                    title = jobContainer.find_element_by_css_selector(".rowHeader a").text
                    self.job.setTitle(title)

                    link = jobContainer.find_element_by_css_selector(".rowHeader a").get_attribute("href")
                    self.job.setLink(link)

                    salary = jobContainer.find_element_by_css_selector(".displaysalarydescription_vacancyColumn").text
                    self.job.setSalary(salary)

                    hasExpireDate = bool(jobContainer.find_elements_by_css_selector(".pospublishenddate_vacancyColumn"))
                    if hasExpireDate:
                        expireDate = jobContainer.find_element_by_css_selector(".pospublishenddate_vacancyColumn").text.split(
                            "Closing Date ")[1]
                        possibleExpiryDateFormats = [
                            "%dth %B %Y",
                            "%dst %B %Y",
                            "%drd %B %Y",
                            "%dnd %B %Y",
                            "%d %B %Y"
                        ]
                        formattedExpireDate = None
                        for expiryDateFormat in possibleExpiryDateFormats:
                            try:
                                formattedExpireDate = datetime.strptime(expireDate, expiryDateFormat).strftime(
                                    '%Y-%m-%d')
                                break
                            except:
                                pass
                        self.job.setExpireDate(formattedExpireDate)

                    location = jobContainer.find_element_by_css_selector(".codelist4value_vacancyColumn").text
                    self.job.setLocation(location)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

                if self.nextPage():
                    pass
                else:
                    break

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector(".earcu_posdescriptionContainer .earcu_posdescription").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False
