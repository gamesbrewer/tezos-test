__author__ = "Some Guy called Jon"
__copyright__ = "Copyright (C) 2020 Jon aka Gamesbrewer"
__license__ = "Public Domain, Open Source"
__version__ = "1.0"

import smartpy as sp

"""
This is an entity to keep track of fishs and the exchange of said fishs. Currently it functions as a single object
tracker; future version will enable the object to branch and tracked seperately.
"""
class TilapiaOwner(sp.Contract):
    def __init__(self, initialOwner):
        self.init(owner = initialOwner,
                  nameToFishGroupData = sp.map(tkey = sp.TString))

    #general function to check event
    def checkEvent(self, name):
        sp.if ~(self.data.nameToFishGroupData.contains(name)):
            self.data.nameToFishGroupData[name] = sp.record(date = "", numFishes = 0, numWeight = "", locLongitude = "", locLatitude = "")

    #set the date of the fish something happen
    @sp.entry_point
    def setDate(self, params):
        sp.verify(sp.sender == self.data.owner)
        self.checkEvent(params.name)
        self.data.nameToFishGroupData[params.name].date = params.newDate

    #set the number and weight of fish
    @sp.entry_point
    def setFishData(self, params):
        sp.verify(sp.sender == self.data.owner)
        self.checkEvent(params.name)
        self.data.nameToFishGroupData[params.name].numFishes = params.newNumFishes
        self.data.nameToFishGroupData[params.name].numWeight = params.newNumWeight

    #set the location of the fish
    @sp.entry_point
    def setLocation(self, params):
        sp.verify(sp.sender == self.data.owner)
        self.checkEvent(params.name)
        self.data.nameToFishGroupData[params.name].locLongitude = params.newLocLongitude
        self.data.nameToFishGroupData[params.name].locLatitude = params.newLocLatitude

    #set the owner
    @sp.entry_point
    def changeOwner(self, params):
        sp.verify(sp.sender == self.data.owner)
        self.data.owner = params.newOwner


# -------------------------test start here-----------------------------------------
@sp.add_test(name = "TilapiaExchangeTest")
def test():
    scenario = sp.test_scenario()
    # Create HTML output for debugging
    scenario.h1("Fish Exchange Test")
    
    # Initialize test addresses
    fishery = sp.address("tz1-fishery-address-0001")
    driverGuy = sp.address("tz1-driverGuy-address-1234")
    pasarBorong = sp.address("tz1-pasarBorong-address-5678")
    deliveryGuy = sp.address("tz1-deliveryGuy-address-9101")
    marketOwner = sp.address("tz1-marketOwner-address-1121")

    # ---------------fish pick and packaged into a box with QR Codee at fishery-----------------------------------
    
    # Instantiate TilapiaOwner contract
    c1 = TilapiaOwner(fishery)
    
    # Print contract instance to HTML
    scenario += c1

    # Invoke TilapiaOwner entry points, name it, and set the date
    scenario.h2("Set date for Fish Exchange no #110001 to 09-09-2020")
    scenario += c1.setDate(name = "#110001", newDate = "09-09-2020").run(sender = fishery)

    # Invoke TilapiaOwner entry points, set the number of fishes and weight
    scenario.h2("Set number of fish and weight")
    scenario += c1.setFishData(name = "#110001", newNumFishes = 10, newNumWeight = "7.8").run(sender = fishery)

    # set the location the exchange is done
    scenario.h2("Set the location Longitude & Latitude")
    scenario += c1.setLocation(name = "#110001", newLocLongitude = "5.915403", newLocLatitude = "116.127269").run(sender = fishery)

    # change the owner
    scenario.h2("Change owner")
    scenario += c1.changeOwner(newOwner = driverGuy).run(sender = fishery)

    # ------------driver Guy pick up fish and drive to new place and exchange it to pasar borong----------------------

    scenario.h2("New owner sets date for fish exchange no #110001 to 10-09-2020")
    scenario += c1.setDate(name = "#110001", newDate = "10-09-2020").run(sender = driverGuy)

    # set the location the exchange is done
    scenario.h2("Set the new location Longitude & Latitude")
    scenario += c1.setLocation(name = "#110001", newLocLongitude = "5.9110722", newLocLatitude = "116.1035276").run(sender = driverGuy)

    # change the owner
    scenario.h2("Change owner")
    scenario += c1.changeOwner(newOwner = pasarBorong).run(sender = driverGuy)

    # ----------------pasar borong piss on fish and maybe spit on it if bad mood----------------------------------

    # change the owner
    scenario.h2("Change owner")
    scenario += c1.changeOwner(newOwner = deliveryGuy).run(sender = pasarBorong)

    # ---------delivery Guy pick up fish and drive to new place and exchange it to market---------------------

    scenario.h2("New owner sets date for fish exchange no #110001 to 11-09-2020")
    scenario += c1.setDate(name = "#110001", newDate = "11-09-2020").run(sender = deliveryGuy)

    # set the location the exchange is done
    scenario.h2("Set the new location Longitude & Latitude")
    scenario += c1.setLocation(name = "#110001", newLocLongitude = "5.943257", newLocLatitude = "116.081475").run(sender = deliveryGuy)

    # change the owner
    scenario.h2("Change owner")
    scenario += c1.changeOwner(newOwner = marketOwner).run(sender = deliveryGuy)

    # -----------------------------to do more, maybe-------------------------------------
#        
#    # Verify expected results
#    scenario.verify((c1.data.nameToFishGroupData["#110001"].date) == '11-09-2020')
#    scenario.verify((c1.data.nameToFishGroupData["#110001"].numFishes) == 10)
#    scenario.verify((c1.data.owner) == sp.address('tz1-marketOwner-address-1121'))