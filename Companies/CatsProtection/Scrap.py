
import os
from requests import get
from bs4 import BeautifulSoup

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Cats Protection"
        self.ownerUsername = "jennikirk"
        self.scrapPageURL = "https://talos360.com/feeds/jobboardonemail5"
        self.passWord = '^!C.hBTX5D;a'
        self.userName = 'feeds.lgbtjobs@cats.co.uk'
        self.feedType = self.feedTypeXML
        #     Company Details End

    def loadScrapPage(self):
        pass

    def loadXML(self):
        responseJobData = get(self.scrapPageURL, auth=(self.userName, self.passWord))
        jobDataFilePath = './Companies/CatsProtection/XMLFeed/'
        jobDataFile = jobDataFilePath + 'jobXMLFeed.xml'
        if not os.path.exists(jobDataFilePath):
            os.makedirs(jobDataFilePath)
        writeJobData = open(jobDataFile, "w+")
        writeJobData.write(responseJobData.text)

        with open(jobDataFile, 'r') as f:
            data = f.read()

        self.jobData = BeautifulSoup(data, "xml")

    # Scraper Function
    def loadJobs(self):
        self.loadXML()
        try:
            jobContainers = self.jobData.find_all('item')
            for jobContainer in jobContainers:
                title = jobContainer.find('jobtitle').text
                self.job.setTitle(title)

                link = jobContainer.find('link').text
                self.job.setLink(link)

                description = jobContainer.find('description').text
                self.job.setDescription(description)

                location = jobContainer.find('joblocation').text
                self.job.setLocation(location)

                salary = "£"+jobContainer.find('jobsalaryfrom').text.split(".")[0] + " to £" + jobContainer.find('jobsalaryto').text.split(".")[0] 
                self.job.setSalary(salary,"£(\d{1,5}(?:,\d{5})*) to £(\d{1,5}(?:,\d{5})*)", is_salary_text=True)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()
            return True
        except:
            self.exceptionLogging()
            return False