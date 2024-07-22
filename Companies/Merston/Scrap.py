# Required Packages
from datetime import datetime
import htmlmin
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, storage = None):
        super().__init__()
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Marstons"
        self.ownerUsername = "marstons"
        self.location = "Durham"
        self.scrapPageURLS = ["https://apply.runamarstonspub.co.uk/feeds/datafeed.ashx?format=xml","https://www.marstonscareers.co.uk/feeds/datafeed.ashx?format=xml"]
        self.feedType = self.feedTypeXML

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

    def loadJobs(self):
        try:
            for feedUrl in self.scrapPageURLS:
                with urlopen(feedUrl) as f:
                    tree = ET.parse(f)
                    root = tree.getroot()


                for x in root.findall('Item'):
                    title = x.find('Title').text
                    link = x.find('Link').text
                    description = x.find('Description').text
                    try:
                        description += x.find('Qualifications').text
                    except:
                        pass
                    location = x.find('Location').text

                    try:
                        salary = x.find('EstimatedWeeklySales').text
                        self.job.setSalary(salary)
                    except:
                        pass


                    title = title.strip()
                    self.job.setTitle(title)
                    self.job.setLink(link)
                    self.job.setLocation(location)
                    self.job.setDescription(description)


                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

            return True

        except:
            self.exceptionLogging()
            return False

    def loadScrapPage(self):
        pass