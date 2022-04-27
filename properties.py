#COTP Automation Properties File
#
#Please adjust the settings to match your account. 
#Please keep the '' and "" in the code, do not remove them.

# The script will cycle trades then wait between 7300 and 7500 second before trying to cyle again
# If it does not cycle, then it will wait between 30 and 120 seconds before trying again. 

# Single Account only right now. Multi account coming soon (tm)

website = 'https://cotps.com/#/'  # - do not edit this unless the website changes. 


countryCode ='1'        # - Do not add a + here. Just the number
phone ='4232558697'     # - No spaces or punctuation

password ='Boostmobile2'     # - Dont have spaces between the '' - should look like: ='P4ssW0rd'


doCycle = True          # Cycle Trades - must be set true or it wont wait 7300~7500
doReferral = True       # Collect Referral Bonuses.

delayStartTimer = 0     # The number of seconds the script will wait before attempting the first trade cycle.


# Donations are welcome to the dev who made this script possible
# If you feel like donating to their work, please see below crypto addresses 
# TRC20-USDT - TMmixvUftduuAX6JzGnEyb9jHmV8NttBN4
# ETH ERC-20 - 0x261e3Da1cB14C7C4a2C0FBa0E9483c3904482133


#########     OPTIONAL   ##############
#IF This Then That -  Webhooks and Profit Timings
#
# If you know what IFTTT is, you can set up an account for free and receive email notifications when your script runs.

iftttEnabled = False

iftttKeyCode = 'xxxxxx'

iftttSuccess = 'COTPCycled'    #Notification when trades have been cycled
iftttProblem = 'COTPProblem'   #There was an issue with the script, please check it
iftttProfit = 'COTPCycled'     #Profits are ready to be collected

iftttNames = 'Main'

dailyProfit = 0        # - the potential DOLLAR AMOUNT of your account to leave out of Transaction for profit take ONCE A DAY. - the script will run until under this amount
minTimeForProfits = 0     # the min time window of day Profits will be available to withdraw ***IN UTC*** - Hour Only - no minutes
maxTimeForProfits = 0     # the max time window of day Profits will be available to withdraw ***IN UTC***

logLevel = 'INFO'       # Sets the logging level of the application
                        # - CRITICAL [50]
                        # - ERROR [40]
                        # - WARNING [30]
                        # - INFO [20]
                        # - DEBUG [10]
                        # - NOTSET [0]

headless = 'Auto'       # Options: Auto/True/False
