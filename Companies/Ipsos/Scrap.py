# Required Packages
import time

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
        self.companyName = "Ipsos"
        self.ownerUsername = "ipsos"
        self.scrapPageURL = "https://ecqf.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/IpsosCareers/requisitions?lastSelectedFacet=LOCATIONS&location=United+Kingdom"
        self.feedType = self.feedTypeWebScrap
        #     Company Details End

    def loadScrapPage(self):
        self.chrome.getComplete(self.scrapPageURL)

        WebDriverWait(self.chrome, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-qa='searchResultItem']"))
        )
        
        self.chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)



    def loadJobs(self):
        self.loadScrapPage()
        try:
            jobContainers = self.chrome.find_elements_by_css_selector("[data-qa='searchResultItem']")
            for jobContainer in jobContainers:
                title = jobContainer.find_element_by_css_selector(".job-tile__title").text
                self.job.setTitle(title)

                link = jobContainer.find_element_by_css_selector(".job-list-item__link").get_attribute('href')
                self.job.setLink(link)

                location = jobContainer.find_element_by_css_selector(".job-tile__subheader span:first-child").text
                self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, currentJobInfo in enumerate(self.jobs):
                self.chrome.getComplete(currentJobInfo.getLink())

                self.sanitizeElementsForDescription()
                
                description =""
                hasOverview =  bool(self.chrome.find_elements_by_css_selector("[data-bind='html: pageData().job.description']"))
                hasAboutTheTeam =  bool( self.chrome.find_elements_by_css_selector("[data-bind='html: pageData().job.organizationDescription']"))
                hasAboutUs =   bool(self.chrome.find_elements_by_css_selector("[data-bind='html: pageData().job.corporateDescription']") )

                if(hasOverview):
                    description = description + self.chrome.find_element_by_css_selector("[data-bind='html: pageData().job.description']").get_attribute('innerHTML')
                if(hasAboutTheTeam):
                    description = description + "<h2>About The Team</h2>" + self.chrome.find_element_by_css_selector("[data-bind='html: pageData().job.organizationDescription']").get_attribute('innerHTML')
                if(hasAboutUs):
                    description = description + "<h2>About Us</h2>" + self.chrome.find_element_by_css_selector("[data-bind='html: pageData().job.corporateDescription']").get_attribute('innerHTML')

                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False