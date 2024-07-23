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
        self.companyName = "Liverpool John Moores University"
        self.ownerUsername = "liverpooljohnmooresuniversity"
        self.scrapPageURL = "https://jobs.ljmu.ac.uk/vacancies.html"
        self.feedType = self.feedTypeWebScrap
        self.defaultLocation = "Liverpool"
        #     Company Details End

    def loadScrapPage(self):

        self.chrome.getComplete(self.scrapPageURL)

    # Scraper Function
    def loadJobs(self):

        self.loadScrapPage()

        try:

            jobContainers = self.chrome.find_elements_by_css_selector("#icams_inserted .searchresults .jobpost")
            for jobContainer in jobContainers:

                title = str(jobContainer.find_element_by_css_selector(".jobpost_body > h2").text)
                title = title.strip()
                self.job.setTitle(title)

                location = self.defaultLocation
                self.job.setLocation(location)

                link = jobContainer.find_element_by_css_selector(".jobpost_body  a").get_attribute("href")
                self.job.setLink(link)


                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)
                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):

                self.chrome.getComplete(job.getLink())
                self.chrome.pageWait()

                try:
                    if len(self.chrome.find_elements_by_css_selector('#salary_range')) > 0:
                        salary_range = self.chrome.find_element_by_xpath('//*[@id="salary_range"]').text.strip()
                        self.jobs[currentJobIndex].setSalary(salary_range)
                    elif len(self.chrome.find_elements_by_css_selector('#salary')) > 0:
                        salary = self.chrome.find_element_by_xpath('//*[@id="salary"]').text.strip()
                        self.jobs[currentJobIndex].setSalary(salary)
                except Exception as e:
                    exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)

                self.sanitizeElementsForDescription()
                descriptionElement = self.chrome.find_element_by_css_selector('.job_postings .job_description')
                description = descriptionElement.get_attribute('innerHTML').strip()
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False