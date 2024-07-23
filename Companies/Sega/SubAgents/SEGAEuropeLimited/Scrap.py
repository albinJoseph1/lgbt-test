from Companies.Sega.SubAgents.StandardSegaAgent import Agent as ScrapAgent

class Agent(ScrapAgent):
    def __init__(self, chrome):
        self.chrome = chrome
        super(Agent, self).__init__(self.chrome)

        #     Company Details Start
        self.companyName = "SEGA Europe Limited"
        self.companyHint = "SEGA"
        #     Company Details End



