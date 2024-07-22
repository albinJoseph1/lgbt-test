# Required Packages
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from datetime import datetime

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "The Premier League"
        self.ownerUsername = "premierleague"
        self.scrapPageURL = "https://premierleague.pinpointhq.com/jobs/indeed_feed.xml"
        self.feedType = self.feedTypeXML
        self.maxScrapPageLimit = 20
        #     Company Details End


    def loadScrapPage(self):
        pass

    def loadXML(self):
        with urlopen(self.scrapPageURL) as xml:
            tree = ET.parse(xml)
            self.jobsContainer = tree.getroot()

    def loadJobs(self):
        self.loadXML()
        try:
            for job in self.jobsContainer.findall('job'):
                apply_link = job.find('url').text.split('?')[0].strip()
                self.job.setLink(apply_link)

                title = job.find('title').text
                self.job.setTitle(title)

                description = job.find('description').text
                self.job.setDescription(description)

                location = job.find('country').text
                self.job.setLocation(location)

                contract = job.find('jobtype').text
                self.job.setContract(contract)

                expireDate = job.find('expiration_date').text

                possibleExpiryDateFormats = [
                    "%Y-%m-%d"
                ]
                for possibleExpireDate in possibleExpiryDateFormats:
                    try:
                        expireDate = datetime.strptime(expireDate, possibleExpireDate).strftime('%Y-%m-%d')
                        self.job.setExpireDate(expireDate)
                    except Exception as e:
                        exception_message = str(title) + ' : ' + str(e) + "\n"
                        self.exceptionLogging('warning', exception_message)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            return True

        except:
            self.exceptionLogging()
            return False