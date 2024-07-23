# Required Packages
from datetime import datetime
import requests
from urllib3 import poolmanager
import ssl
import xml.dom.minidom
from Resource import htmlmin

from Companies.StandardAgent import ScrapAgent

class Agent(ScrapAgent):
    def __init__(self, storage = None):
        super().__init__()
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0
        self.XML = None

        #Company Details Start
        self.companyName = "Croud"
        self.ownerUsername = "croud"
        self.scrapPageURL = "https://careers.croud.com/jobs.rss"
        self.feedType = self.feedTypeXML
        self.maxScrapPageLimit = 20
          # Company Details End



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


    # Scraper Function
    def loadJobs(self):
        self.loadXML()
        try:
            xmlparse = xml.dom.minidom.parseString(self.XML)
            jobContainers = xmlparse.getElementsByTagName('item')
            for jobContainer in jobContainers:
                link = jobContainer.getElementsByTagName('link')[0].firstChild.nodeValue
                self.job.setLink(link)

                title = jobContainer.getElementsByTagName('title')[0].firstChild.nodeValue
                self.job.setTitle(title)

                description = jobContainer.getElementsByTagName('description')[0].firstChild.nodeValue
                self.job.setDescription(description)


                try:
                    address = str(jobContainer.getElementsByTagName('tt:address')[0].firstChild.nodeValue)
                    city = str(jobContainer.getElementsByTagName('tt:city')[0].firstChild.nodeValue)
                    location = address+", "+city
                    self.job.setLocation(location)
                except Exception as e:
                    exception_message = str(self.job.getTitle()) + ' : ' + str(e) + "\n"
                    self.exceptionLogging('warning', exception_message)

                self.job.setCompanyName(self.companyName)
                self.job.setOwnnerUsername(self.ownerUsername)

                self.addToJobs()

            return True

        except:
            self.exceptionLogging()
            return False
