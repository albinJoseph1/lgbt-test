# Required Packages
import time
import requests
import json

from Resource import htmlmin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Companies.StandardAgent import ScrapAgent

from requests.structures import CaseInsensitiveDict

class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0
        self.jobIndicesToRemove = []

        #     Company Details Start
        self.companyName = ""
        self.ownerUsername = "sega"
        self.scrapPageURL = "https://careers.sega.co.uk/api/jobs"
        self.companyHint = ""
        self.jobDatas = []
        #     Company Details End

    def getCompanyName(self):
        return self.companyName

    def getFeedType(self):
        return self.feedType

    def getFeedUrl(self):
        return self.scrapPageURL

    def getSourceJobCount(self):
        return 0

    def getScrapedJobCount(self):
        return len(self.jobs)

    def getOwnerUsername(self):
        return self.ownerUsername

    def loadScrapPage(self):
        headers = CaseInsensitiveDict()
        headers["careers-api-key"] = "0MgSWGd5UcWLRgquu1Jgk5vjLt8bRqf9"
        self.jobDatas = requests.get(self.scrapPageURL, headers=headers)
        self.jobDatas = self.jobDatas.text
        self.jobDatas = json.loads(self.jobDatas)

    def loadJobs(self):
        self.loadScrapPage()
        try:
            for job in self.jobDatas:
                isJobToPost = False
                # print(job['studio'])
                companyMentioned = job['studio']
                if self.companyHint in companyMentioned:
                    isJobToPost = True
                if isJobToPost:
                    title = job['title']
                    self.job.setTitle(title)

                    link = job['link']['apply']
                    self.job.setLink(link)

                    location = job['country']
                    self.job.setLocation(location)

                    description = job['description']
                    self.job.setDescription(description)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()
            return True
        except:
            self.exceptionLogging()
            return False