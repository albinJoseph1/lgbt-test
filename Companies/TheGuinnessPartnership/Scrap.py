# Required Packages
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
        self.companyName = "The Guinness Partnership"
        self.ownerUsername = "guinnesspartnership"
        self.scrapPageURL = "https://careers.guinnesspartnership.com/jobs/vacancy/find/results/"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#posBrowser_ResultsGrid_pageBlock"))
        )

    def nextPage(self):

        max_pages = self.chrome.find_element(By.CSS_SELECTOR, '.pagingText').text.split()[-1]
        current_page_number = self.chrome.find_element(By.CSS_SELECTOR, '.pagingText').text.split()[1]

        if max_pages != current_page_number:
            next_button = self.chrome.find_element(By.CSS_SELECTOR, '.normalanchor.ajaxable.scroller.scroller_movenext.buttonEnabled').get_attribute("href")
            self.chrome.getComplete(next_button)
            WebDriverWait(self.chrome, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ListGridContainer .rowContainer"))
            )

            return True
        else:
            return False


    # Scraper Function
    def loadJobs(self):
        self.loadScrapPage()

        try:
            while True:
                jobContainers = self.chrome.find_elements(By.CSS_SELECTOR, ".ListGridContainer .rowContainer")

                for jobContainer in jobContainers:

                    title = jobContainer.find_element(By.CSS_SELECTOR, ".rowHeader a").text
                    self.job.setTitle(title)

                    link = jobContainer.find_element(By.CSS_SELECTOR, ".rowHeader a").get_attribute("href")
                    self.job.setLink(link)

                    location = jobContainer.find_element(By.CSS_SELECTOR, ".vacancyColumn").text
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

                salary = self.chrome.find_element(By.CSS_SELECTOR, ".jobValues .SumItem_displaysalarydescription .jobSumValue").text
                self.jobs[currentJobIndex].setSalary(salary, "£?(\d+(?:,?)\d+)(?:\.\d+)?\s*-\s*£?(\d+(?:,?)\d+)(?:\.\d+)?|£?(\d+(?:,?)\d+)(?:\.\d+)?", is_salary_text=True)

                description = self.chrome.find_element(By.CSS_SELECTOR, ".LeftJobBox .earcu_posdescription").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False
