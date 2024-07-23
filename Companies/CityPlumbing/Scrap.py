# Required Packages
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "City Plumbing"
        self.ownerUsername = "cityplumbingsuppliesholdingsltd"
        self.scrapPageURL = "https://cop-webapi-live.service.4matnetworks.com/api/jobfeed/1481108/1/012b6e20-dd4a-42f6-8bee-31a9a63d5f3c/IndeedFeed/src/PHDI"
        self.feedType = self.feedTypeXML
        #     Company Details End

    def loadScrapPage(self):
        pass

    def loadXML(self):
        with urlopen(self.scrapPageURL) as xml:
            tree = ET.parse(xml)
            self.jobsContainer = tree.getroot()

        # Scraper Function

    def loadJobs(self):
        self.loadXML()
        try:
            for job in self.jobsContainer.findall('job'):
                title = job.find('title').text
                title = title.strip()

                link = job.find('url').text.strip()
                link = link.strip()

                location = job.find('locationfreetext').text
                location = location.strip()

                description = job.find('description').text
                description = description.strip()

                contract = job.find('jobtype').text
                contract = contract.strip()

                self.job.setTitle(title)

                self.job.setLink(link)

                self.job.setLocation(location)

                self.job.setContract(contract)

                self.job.setDescription(description)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            return True
        except:
            self.exceptionLogging()
            return False