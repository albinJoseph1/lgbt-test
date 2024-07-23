# Required Packages
from Resource import htmlmin
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from Managers import lgbtManager
from Companies.StandardAgent import ScrapAgent

class Agent(ScrapAgent):
    def __init__(self, storage = None):
        super().__init__()
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0
        self.XML = None

        #Company Details Start
        self.companyName = "Burberry"
        self.ownerUsername = "burberry"
        self.scrapPageURL = "https://burberrycareers.com/feed/361600"
        self.feedType = self.feedTypeXML
        self.locationFilters = ['UK','GB']
        self.maxScrapPageLimit = 20
          # Company Details End



    def loadScrapPage(self):
        pass

    def loadXML(self):
        with urlopen(self.scrapPageURL) as xml:
            tree = ET.parse(xml)
            self.jobsContainer = tree.getroot().find('jobs')

    # Scraper Function
    def loadJobs(self):
        self.loadXML()
        try:
            for job in self.jobsContainer.findall('job'):
                country = job.find('country').text
                hasLocationFilter = False
                for locationFilter in self.locationFilters:
                    if locationFilter == country:
                        hasLocationFilter = True
                        break
                if hasLocationFilter:
                    title = job.find('title').text
                    title = title.strip()

                    apply_link = job.find('url').text
                    apply_link = apply_link.strip()

                    city = job.find('city').text


                    description = job.find('description').text

                    contract = job.find('jobtype').text

                    self.job.setTitle(title)
                    self.job.setLocation(city)

                    self.job.setLink(apply_link)
                    self.job.setContract(contract)

                    self.job.setDescription(description)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

            return True

        except:
            self.exceptionLogging()
            return False

