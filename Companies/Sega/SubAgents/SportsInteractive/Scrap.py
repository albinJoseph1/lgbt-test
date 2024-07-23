
from Companies.Sega.SubAgents.StandardSegaAgent import Agent as ScrapAgent

class Agent(ScrapAgent):
    def __init__(self, chrome):
        self.chrome = chrome
        super(Agent, self).__init__(self.chrome)

        #     Company Details Start
        self.companyName = "Sports Interactive"
        self.companyHint = "Sports Interactive"
        #     Company Details End