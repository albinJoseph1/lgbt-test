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
        self.companyName = "Nottingham College"
        self.ownerUsername = "nottinghamcollege"
        self.scrapPageURL = "https://www.nottinghamcollege.ac.uk/about-us/working-for-us/vacancies?query=&index=hrJobVacancies"
        self.feedType = self.feedTypeWebScrap

        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)
        
        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".m-vacancy-result"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector(".m-vacancy-result")
            for jobContainer in jobContainers:
                title = jobContainer.find_element_by_css_selector(".m-vacancy-result__title .h4").text
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector(".m-vacancy-result__title .h4 a").get_attribute('href')
                self.job.setLink(link)

                jobFields = jobContainer.find_elements_by_css_selector(".m-vacancy-result__meta li")
                for field in jobFields:
                    fieldContent = field.text
                    if 'Location' in fieldContent:
                        location = fieldContent.replace("Location:","").strip()
                        self.job.setLocation(location)
                    elif 'Salary' in fieldContent:
                        salary = fieldContent.replace("Salary:","").strip()
                        self.job.setSalary(salary)
                    elif 'Employment type' in fieldContent:
                        contract = fieldContent.replace("Employment type:","").strip()
                        self.job.setContract(contract)
                
                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()
                description = self.chrome.find_element_by_css_selector(".u-styled-lists.intro--first").get_attribute("innerHTML")
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False
