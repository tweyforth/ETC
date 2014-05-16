import traceback


def deco_retry(f):
    def func_retry(*args, **kwargs):
        while True:
            try:
                res = f(*args, **kwargs)
                break
            except Exception as e:
                print traceback.format_exc(e)
                print "Please try again"
    return func_retry


class Team(object):
    possibleArmies = ['wood elves', 'dark elves', 'high elves', 'dwarves', 'vampire counts', 'skaven', 'tomb kings', 'orcs',
                      'empire', 'bretonnians', 'beastmen', 'chaos dwarves', 'daemons', 'warriors']

    def __init__(self, name, armies):
        self.armies = []
        self.name = name
        self.armyUpStaging = ""
        self.armyCounterStaging = []
        self.pickedArmies = []
        for army in armies:
            if army not in self.__class__.possibleArmies:
                raise Exception("%s is not a valid army, your choices are: %s" % (army, self.__class__.possibleArmies))
            self.armies.append(army)

    @deco_retry
    def putArmyUp(self):
        input = raw_input("Which army is Team %s putting up?" % self.name)
        if input not in self.armies:
            raise Exception("Army is not available")
        self.armyUpStaging = (input)
        self.armies.remove(input)

    @deco_retry
    def counterArmy(self, army):
        input1 = raw_input("You need to counter %s with two of your armies, what is your first choice?" % army)
        if input1 not in self.armies:
            raise Exception("%s is not a valid choice, your choices are: %s" % (input1, self.armies))
        self.armyCounterStaging.append(input1)
        self.armies.remove(input1)
        input2 = raw_input("You need to counter %s with two of your armies, what is your second choice?" % army)
        self.armyCounterStaging.append(input2)
        self.armies.remove(input2)

    @deco_retry
    def selectArmy(self, opposingArmy, lastRoundFlag=False):
        if len(self.armyCounterStaging) != 2:
            raise Exception("Improper number of armies in staging")
        print self.armyCounterStaging
        print "Team %s Pick either %s or %s to face against your %s" % (self.name, self.armyCounterStaging[0], self.armyCounterStaging[1], opposingArmy)
        choice = raw_input("Which army do you pick?")
        if choice not in self.armyCounterStaging:
            raise Exception("Army is not available, available armies are: %s" % self.armyCounterStaging)
        self.pickedArmies.append(choice)
        self.armyCounterStaging.remove(choice)
        if lastRoundFlag:
            self.pickedArmies.append(self.armyCounterStaging[0])
        else:
            self.armies.append(self.armyCounterStaging[0])
        self.armyCounterStaging = []

    def moveArmyUpStagingToPicked(self):
        self.pickedArmies.append(self.armyUpStaging)
        self.armyUpStaging = ""


def workflow():
    ##make team size a variable!!!

    #teamA_name = raw_input("What is the name of team A?")
    #teamA = Team(teamA_name, [raw_input("What is army #%s for team %s" % (num, teamA_name)) for num in xrange(1, 9)])
    teamA = Team("one", ['wood elves', 'dark elves', 'high elves', 'dwarves', 'vampire counts', 'skaven', 'tomb kings', 'orcs'])
    #teamB_name = raw_input("What is the name of team B?")
    teamB = Team("two", ['wood elves', 'dark elves', 'high elves', 'dwarves', 'vampire counts', 'skaven', 'tomb kings', 'orcs'])
    #teamB = Team(teamB_name, [raw_input("What is army #%s for team %s" % (num, teamB_name)) for num in xrange(1, 9)])
    for _ in xrange(3):
        teamA.putArmyUp()
        teamB.putArmyUp()
        teamA.counterArmy(teamB.armyUpStaging)
        teamB.counterArmy(teamA.armyUpStaging)
        teamA.selectArmy(teamB.armyUpStaging)
        teamB.moveArmyUpStagingToPicked()
        teamB.selectArmy(teamA.armyUpStaging)
        teamA.moveArmyUpStagingToPicked()
    teamA.putArmyUp()
    teamB.putArmyUp()
    teamA.counterArmy(teamB.armyUpStaging)
    teamB.counterArmy(teamA.armyUpStaging)
    teamA.selectArmy(teamB.armyUpStaging, lastRoundFlag=True)
    teamB.moveArmyUpStagingToPicked()
    teamB.pickedArmies.append(teamB.armies[0])
    teamB.selectArmy(teamA.armyUpStaging, lastRoundFlag=True)
    teamA.moveArmyUpStagingToPicked()
    teamA.pickedArmies.append(teamA.armies[0])
    print teamA.armies, teamA.pickedArmies
    print teamB.armies, teamB.pickedArmies


if __name__ == "__main__":
    workflow()