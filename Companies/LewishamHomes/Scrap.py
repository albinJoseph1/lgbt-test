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
        self.companyName = "Lewisham Homes"
        self.ownerUsername = "lewishamhomes"
        self.scrapPageURL = "https://ig29.i-grasp.com/fe/tpl_lewishamhomes01.asp?KEY=56242810&C=985478832356&PAGESTAMP=dbqvyyuywtjzdjrtxs&nexts=INIT_JOBLISTSTART&nextss=&mode=1&newQuery=yes&searchrefno=&searchindustry=0&searchpositiontype=0&searchjobgenerallist2id=0&searchtext=&formsubmit4=Search+and+Apply"
        self.feedType = self.feedTypeWebScrap
        self.jobKey = 'title'
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#searchresultslist"))
        )

    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("#searchresultslist tbody tr")
            for jobContainer in jobContainers:
                link = jobContainer.find_element_by_css_selector(".igsearchresultstitle a").get_attribute('href')
                self.job.setLink(link)

                title = jobContainer.find_element_by_css_selector(".igsearchresultstitle").text
                self.job.setTitle(title)

                contract = jobContainer.find_element_by_css_selector(".igsearchresultspositiontype").text
                self.job.setContract(contract)

                salary = jobContainer.find_element_by_css_selector(".igsearchresultsgeneral2").text
                self.job.setSalary(salary)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())

                self.sanitizeElementsForDescription()

                location = self.chrome.find_element_by_css_selector("#igMainJobDescription").text
                try:
                    location = location.split('Location')[1].split("Salary")[0].strip()
                    self.jobs[currentJobIndex].setLocation(location)
                except Exception as e:
                    exception_message = str(job.getTitle()) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)

                description = self.chrome.find_element_by_css_selector("#igMainJobDescription").get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True
        except:
            self.exceptionLogging()
            return False