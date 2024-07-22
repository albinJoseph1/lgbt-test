# Required Packages
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
        self.companyName = "Ab agri"
        self.ownerUsername = "abagri"
        self.scrapPageURL = "https://careers.abagri.com/vacancies/vacancy-search-results.aspx"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):

        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentContainer_ctl00_VacancyListView"))
        )

    def nextPage(self):

        has_next_button = bool(self.chrome.find_element_by_css_selector('.paginator > a:nth-last-of-type(2)').text == 'Next')
        if has_next_button:
            next_button = self.chrome.find_element_by_css_selector('.paginator > a:nth-last-of-type(2)')
            next_button.click()
            time.sleep(3)
            return has_next_button
        else:
            return False


    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()

        try:
            while True:
                jobContainers = self.chrome.find_elements_by_css_selector("#ctl00_ContentContainer_ctl00_VacancyListView .vsr-job")
                for jobContainer in jobContainers:
                    link = jobContainer.find_element_by_css_selector(".vsr-job__title a").get_attribute('href')
                    self.job.setLink(link)

                    title = jobContainer.find_element_by_css_selector(".vsr-job__title").text
                    self.job.setTitle(title)

                    location = jobContainer.find_element_by_css_selector("[data-id='div_content_VacV_LocationID']").text
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

                try:
                    description = self.chrome.find_element_by_css_selector(".vac-details__description #div_VacV_Description").get_attribute("innerHTML")
                    self.jobs[currentJobIndex].setDescription(description)
                except:
                    exception_message = "There is no description found for the job : "+job.getTitle()+"\n"
                    self.exceptionLogging('warning', exception_message)


            return True
        except:
            self.exceptionLogging()
            return False