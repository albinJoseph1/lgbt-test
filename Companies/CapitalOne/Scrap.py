# Required Packages

from selenium.common.exceptions import NoSuchElementException
import requests
from Managers import lgbtManager
from Objects import Job
from bs4 import BeautifulSoup
from ftplib import FTP
from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, chrome, storage=None):
        super().__init__()
        self.chrome = chrome
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Capital One"
        self.ownerUsername = "capitalone"
        self.FTPhost = "ftp.tmpwebeng.com"
        self.FTPuserName = "FTPCAPITALONE"
        self.FTPpassword = "k-ygW6pxhd"
        self.feedType = self.feedTypeXML
        #     Company Details End

    def loadScrapPage(self):
        pass

    def loadXML(self):
        pass

    def loadJobs(self):
        try:
            ftp = FTP(self.FTPhost)
            ftp.login(self.FTPuserName, self.FTPpassword)
            dir_struct = ftp.nlst()
            for xml_feed in dir_struct:
                if xml_feed in ('CapitalOne_Radancy_UK.xml'):
                    localfile = xml_feed
                    ftp.retrbinary("RETR " + xml_feed, open(localfile, 'wb').write)
                    with open(localfile, 'r') as f:
                        data = f.read()
                    Bs_data = BeautifulSoup(data, "xml")
                    jobContainers = Bs_data.find_all('job')
                    for x in jobContainers:
                        title = x.find('title').text
                        link = x.find('url').text
                        description = x.find('description').text
                        location = x.find('city').text

                        self.job.setTitle(title)
                        self.job.setLink(link)
                        self.job.setLocation(location)
                        self.job.setDescription(description)

                        self.job.setCompanyName(self.companyName)
                        self.job.setOwnnerUsername(self.ownerUsername)

                        self.addToJobs()
                    return True
            ftp.quit()


        except:
            self.exceptionLogging()
            return False
