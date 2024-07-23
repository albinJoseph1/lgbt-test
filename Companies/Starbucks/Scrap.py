# Required Packages
from datetime import datetime
import htmlmin
# from urllib.request import urlopen
# import xml.etree.ElementTree as ET
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pysftp
import os
from bs4 import BeautifulSoup

from Companies.StandardAgent import ScrapAgent


class Agent(ScrapAgent):
    def __init__(self, storage = None):
        super().__init__()
        self.storage = storage
        self.jobs = []
        self.sourceJobCount = 0

        #     Company Details Start
        self.companyName = "Starbucks"
        self.ownerUsername = "starbucks"
        self.feedType = self.feedTypeXML
        self.FTPhost = "sftp-b2b.sbux.com"
        self.FTPuserName = "ext_bmejobs"
        self.FTPpassword = "JobzRus'^&\"!"
        self.private_key = ".ppk"
        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None
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

    def loadScrapPage(self):
        pass

    def loadJobs(self):
        try:
            ukJobFeeds = []
            latest = 0
            latestfile = None
            with pysftp.Connection(
                    host=self.FTPhost,
                    username=self.FTPuserName,
                    password=self.FTPpassword,
                    private_key=self.private_key,
                    cnopts=self.cnopts) as sftp:

                sftp.cwd("tp_prs_public/out")
                directory_structure = sftp.listdir_attr()
                for file in directory_structure:
                    extension = str(os.path.splitext(file.filename)[1]).lower()
                    if extension in ('.xml') and ('euro') in file.filename:
                        ukJobFeeds.append(file)
                    else:
                        pass
                for xmlfeed in ukJobFeeds:
                    if xmlfeed.st_mtime > latest:
                        latest = xmlfeed.st_mtime
                        latestfile = xmlfeed.filename


                if latestfile is not None:
                    remote_File_Path = '/tp_prs_public/out/' + latestfile
                    local_File_Path = './Companies/Starbucks/XML_Files/' + latestfile
                    sftp.get(remote_File_Path, local_File_Path)
                    with open(local_File_Path, 'r') as f:
                        data = f.read()
                    Bs_data = BeautifulSoup(data, "xml")
                    jobContainers = Bs_data.find_all('Requisition')
                    for jobContainer in jobContainers:
                        title = jobContainer.find('jobTitle').find('value', locale="en-GB").text
                        self.job.setTitle(title)

                        link = jobContainer.find('externalURLRet').find('value', locale="en-GB").text
                        self.job.setLink(link)

                        description = jobContainer.find('DescriptionExternalHTML').find('value', locale="en-GB").text
                        description += jobContainer.find('ExternalQualificationHTML').find('value', locale="en-GB").text
                        self.job.setDescription(description)

                        location = jobContainer.find('city').find('value', locale="en-GB").text
                        self.job.setLocation(location)

                        self.job.setCompanyName(self.companyName)
                        self.job.setOwnnerUsername(self.ownerUsername)

                        self.addToJobs()
                    return True
                else:
                    pass

        except:
            self.exceptionLogging()
            return False