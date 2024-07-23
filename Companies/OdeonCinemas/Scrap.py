# Required Packages
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
        self.companyName = "ODEON"
        self.ownerUsername = "odeoncinemas"
        self.scrapPageURL = "https://www.jobtrain.co.uk/odeon5/Home/Job"
        self.feedType = self.feedTypeWebScrap


    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".job-search__results-items"))
        )

    def nextPage(self):
        self.chrome.clickElement(
            self.chrome.find_element_by_css_selector("#searchResultsLoadMore #searchResultsLoadMoreBtn"))

    def loadJobs(self):
        self.loadScrapPage()
        try:

            while True:
                LoadMoreButton = self.chrome.find_element_by_css_selector(
                    "#searchResultsLoadMore").value_of_css_property(
                    "display")
                if 'none' in LoadMoreButton:
                    break
                else:
                    self.nextPage()

            jobContainers = self.chrome.find_elements_by_css_selector(".job-search__results-items .job-card")
            for jobContainer in jobContainers:
                title = jobContainer.find_element_by_css_selector('.job-row__details').text
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector('.job-card__link').get_attribute("href")
                self.job.setLink(link)

                location = jobContainer.find_element_by_css_selector('.jobdetailsitem.location').text
                location = location.split('Location:')[1]
                self.job.setLocation(location)

                salary = jobContainer.find_element_by_css_selector('.jobdetailsitem.salary').text
                self.job.setSalary(salary)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.chrome.execute_script("""jQuery(".JT-images img").remove();""")

                self.sanitizeElementsForDescription()

                description = self.chrome.find_element_by_css_selector("#Media_Rich_Advert").get_attribute(
                    'innerHTML')
                self.jobs[currentJobIndex].setDescription(description)


            return True
        except:
            self.exceptionLogging()
            return False