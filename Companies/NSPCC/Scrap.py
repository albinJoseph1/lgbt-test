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
        self.companyName = "NSPCC"
        self.ownerUsername = "nspcc"
        self.scrapPageURLs = ["https://join-us.nspcc.org.uk/jobs/rss","https://join-us.nspcc.org.uk/volunteers/rss"]
        self.feedType = self.feedTypeXML
        self.maxScrapPageLimit = 20
          # Company Details End



    def loadScrapPage(self):
        pass

    def loadXML(self,scrapPageUrl):
        url =  scrapPageUrl

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
        responce = session.get(url)
        self.XML = responce.text

    # Scraper Function
    def loadJobs(self):
        try:
            for scrapPageUrl in self.scrapPageURLs:
                self.loadXML(scrapPageUrl)
                xmlparse = xml.dom.minidom.parseString(self.XML)
                jobContainers = xmlparse.getElementsByTagName('item')

                for jobContainer in jobContainers:
                    link = jobContainer.getElementsByTagName('link')[0].firstChild.nodeValue
                    self.job.setLink(link)

                    title = jobContainer.getElementsByTagName('title')[0].firstChild.nodeValue
                    self.job.setTitle(title)

                    mainDescription = jobContainer.getElementsByTagName('description')[0].firstChild.nodeValue

                    description = htmlmin.minify(mainDescription, remove_empty_space=True)
                    description = description.replace("\"", "'")
                    self.job.setDescription(description)

                    mainDescription = mainDescription.split(',')

                    salary = ''
                    for i in range(1,len(mainDescription)):
                        if 'Vacancy End Date' not in mainDescription[i]:
                            salary = salary + str(mainDescription[i])
                        else:
                            break
                    salary = salary.replace('Salary: ',"")
                    self.job.setSalary(salary)

                    for i in range(1, len(mainDescription)):
                        if 'Vacancy End Date' in mainDescription[i]:
                            expireDate = str(mainDescription[i])
                            break
                    expireDate = expireDate.replace('Vacancy End Date: ', "").replace(" ","")
                    expireDate = datetime.strptime(expireDate, '%Y-%m-%dT%H:%M:%S')
                    expireDate = expireDate.strftime('%Y-%m-%d')
                    self.job.setExpireDate(expireDate)

                    for i in range(1, len(mainDescription)):
                        if 'Location:' in mainDescription[i]:
                            location = str(mainDescription[i])
                            break
                    location = location.replace('Location: ',"")
                    self.job.setLocation(location)

                    self.job.setCompanyName(self.companyName)
                    self.job.setOwnnerUsername(self.ownerUsername)

                    self.addToJobs()

            return True

        except:
            self.exceptionLogging()
            return False

