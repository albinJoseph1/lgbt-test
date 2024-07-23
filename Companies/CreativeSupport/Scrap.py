# Required Packages
import json
from datetime import datetime
import requests

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
        self.XML = None

        #Company Details Start
        self.companyName = "Creative Support"
        self.ownerUsername = "creativesupport"
        self.scrapPageURL = "https://www.creativesupport.co.uk/work-for-us/search/"
        self.requestURL = "https://www.creativesupport.co.uk/wp-admin/admin-ajax.php"
        self.requestData = {
          'action': 'search_jobs',
          'form[search_distance]': '20',
          'form[search_region]': 'all',
          'form[search_county]': 'all',
          'form[search_authority]': 'all',
          'pages[max_num_pages]': '1',
          'pages[paged]': '1',
          'pages[per_page]': '1000', #no: of  jobs to be scrapped
          'pages[is_last_page]': 'false'
        }
        self.feedType = self.feedTypeWebScrap
        self.maxScrapPageLimit = 20
        # Company Details End



    def loadScrapPage(self):
        pass

    # Scraper Function
    def loadJobs(self):
        try:
            response = requests.post(self.requestURL, data=self.requestData)
            response = json.loads(response.text)
            jobs = response["jobs"]
            for job in jobs:
                self.job.setTitle(job["title"])
                self.job.setLink(job["permalink"])
                self.job.setSalary(job["salary_type"])
                self.job.setLocation(job["location"])

                expireDate= job["closing_date"]
                expireDate = expireDate.split()
                day = int(''.join(filter(str.isdigit, expireDate[1])))
                day = str(day).zfill(2)
                expireDateText = day+" "+expireDate[2]+" "+expireDate[3]
                expireDate = datetime.strptime(expireDateText, '%d %B %Y').strftime('%Y-%m-%d')
                self.job.setExpireDate(expireDate)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            for currentJobIndex, job in enumerate(self.jobs):
                self.chrome.getComplete(job.getLink())
                WebDriverWait(self.chrome, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.container"))
                )
                self.sanitizeElementsForDescription()
                description = self.chrome.find_element_by_css_selector(".job-page-card-desc").get_attribute('innerHTML')
                self.jobs[currentJobIndex].setDescription(description)

            return True

        except:
            self.exceptionLogging()
            return False

