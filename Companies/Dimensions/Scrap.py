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
        self.companyName = "Dimensions"
        self.ownerUsername = "dimensions"
        self.scrapPageURL = "https://www.dimensionscareers.co.uk/upload/xmlJobs/xmlJobs.xml"
        self.jobTrackingVariableForLGBT = "s=lgbtjobs"
        self.jobTrackingVariableForBME = "s=bmejobs"
        self.jobTrackingVariableForDISABILITY = "s=disabilityjob"
        self.feedType = self.feedTypeXML
        self.maxScrapPageLimit = 20
          # Company Details End



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
                salary = job.find('salary').text
                salary = salary.strip()
                apply_link = job.find('url').text
                apply_link = apply_link.strip()
                city = job.find('city').text
                city = city.strip()
                description = job.find('description').text
                contract = job.find('jobtype').text
                contract = contract.strip()

                self.job.setTitle(title)
                self.job.setSalary(salary)
                self.job.setLocation(city)

                self.job.setLink(apply_link, self.jobTrackingVariableForLGBT, lgbtManager.site.LGBT)
                self.job.setLink(apply_link, self.jobTrackingVariableForBME, lgbtManager.site.BME)
                self.job.setLink(apply_link, self.jobTrackingVariableForDISABILITY, lgbtManager.site.DISABILITY)

                self.job.setContract(contract)

                self.job.setDescription(description)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            return True

        except:
            self.exceptionLogging()
            return False

