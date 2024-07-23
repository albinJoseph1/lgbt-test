# Required Packages
import requests
from urllib3 import poolmanager
import ssl
import xml.dom.minidom

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage = None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Civica"
        self.ownerUsername = "civica"
        self.scrapPageURL = "https://www.civica.com/en-gb/about-us/careers/job-family-listing-pages/all-available-positions/feed/"
        self.feedType = self.feedTypeXML
        #     Company Details End

    def loadScrapPage(self):
        pass

    def loadXML(self):
        url =  self.scrapPageURL

        class TLSAdapter(requests.adapters.HTTPAdapter):

            def init_poolmanager(self, connections, maxsize, block=False):
                """Create and initialize the urllib3 PoolManager."""
                ctx = ssl.create_default_context()
                ctx.set_ciphers('DEFAULT@SECLEVEL=1')
                self.poolmanager = poolmanager.PoolManager(
                    num_pools=connections,
                    maxsize=maxsize,
                    block=block,
                    ssl_version=ssl.PROTOCOL_TLS,
                    ssl_context=ctx)

        tls = TLSAdapter()
        session = requests.session()
        session.mount('https://', TLSAdapter())
        response = session.get(url)
        self.XML = response.text

    def loadJobs(self):
        self.loadXML()
        try:
            xmlparse = xml.dom.minidom.parseString(self.XML)
            self.errorJobLinks = []
            jobContainers = xmlparse.getElementsByTagName('item')
            for jobContainer in jobContainers:
                link = jobContainer.getElementsByTagName('link')[0].firstChild.nodeValue
                self.job.setLink(link)

                title = jobContainer.getElementsByTagName('title')[0].firstChild.nodeValue
                self.job.setTitle(title)

                description = jobContainer.getElementsByTagName('description')[0].firstChild.nodeValue
                self.job.setDescription(description)

                hasCity = bool(jobContainer.getElementsByTagName('city'))
                if hasCity:
                    location = jobContainer.getElementsByTagName('city')[0].firstChild.nodeValue
                    self.job.setLocation(location)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            return True
        except:
            self.exceptionLogging()
            return False