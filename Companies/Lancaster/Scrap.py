# Required Packages
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from Companies.StandardAgent import ScrapAgent

class Agent(ScrapAgent):
    def __init__(self, storage = None):
        super().__init__()
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0
        self.XML = None

        #Company Details Start
        self.companyName = "Lancaster"
        self.ownerUsername = "jcwilliams"
        self.scrapPageURL = "https://ats-lancaster.jgp.co.uk/vacancies.rss?"
        self.location = "Lancaster"
        self.feedType = self.feedTypeXML
        self.maxScrapPageLimit = 20
          # Company Details End



    def loadScrapPage(self):
        pass

    def loadXML(self):
        with urlopen(self.scrapPageURL) as xml:
            tree = ET.parse(xml)
            self.jobsContainer = tree.getroot().find('channel')

    # Scraper Function
    def loadJobs(self):
        self.loadXML()
        try:
            for job in self.jobsContainer.findall('item'):
                title = job.find('title').text
                apply_link = job.find('link').text
                description = job.find('description').text

                self.job.setTitle(title)
                self.job.setLink(apply_link)
                self.job.setDescription(description)
                self.job.setLocation(self.location)
                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            return True

        except:
            self.exceptionLogging()
            return False

