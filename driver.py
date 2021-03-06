"""
Memeily

'funny maymays'

Created by VapidAntGames
May 22nd 2021

"""

import discord
import datetime
import sys
import random
import requests
# from glob import glob
from bs4 import BeautifulSoup
# import os
from dotenv import load_dotenv

import config as cfg

client = None

sys.path.append(".")

# Run our client and env inititalization
def init():
    global client

    load_dotenv()
    client = discord.Client()

    print("--Finished initialization--")


# Pulls a random line out of our hilda quote file
def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline
    return line

# Retrieves the remaining time until lyn's stream
def lyndate():
    today = datetime.date.today()
    futdate = datetime.date(2071, 5, 21)

    now = datetime.datetime.now()
    mnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (mnight - now).seconds
    days = (futdate - today).days
    hms = str(datetime.timedelta(seconds=seconds))

    return ("%d days %s" % (days, hms))

# Retrieves the current market price
def getWrightSocks():

    # Identification Headers to pass to amazon
    HEADERS = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
    }

    # Retrieves the page specified in the config file
    page = requests.get(cfg.WRIGHT_SOCKS_PAGE, headers=HEADERS)
    # page = requests.get(cfg.WRIGHT_SOCKS_PAGE)

    # print(page)

    soup = BeautifulSoup(page.content, features="html5lib")

    # print(soup)


    # LOGGING WAS TAKING TOO MUCH HEADROOM SO WE WILL NOT LOG UNLESS THIS BECOMES AN ISSUE
    # Log page in file for debugging (THIS CONTAINS NO USER DATA)
    #with open("sock.html", 'w') as file:
    #    file.write(str(soup))

    # to prevent script from crashing when there isn't a price for the product
    try:
        # Fetch price off page
        price = soup.find(id='priceblock_ourprice').get_text()
    except:
        price = "ERROR RETRIEVING PRICE! HELP ME @VapidAnt#3577"

    # checking if there is "Out of stock" and if not, it means the product is available
    try:
        soup.select('#availability .a-color-state')[0].get_text().strip()
        inStock = False

    except:
        inStock = True

    if not inStock:
        return "**Oh no! Wright socks are sold out on Amazon!**"
    else:
        return "YOU CAN GET A PAIR OF WRIGHT SOCKS TODAY FOR ONLY " + "**" + price + "**"


# Creates a random tea recipe
def teaRecipe():
    # Possible tea ingredients
    ingredientsList = ["chamomile tea", "white tea", "green tea", "linden flowers", "black tea",
                       "oolong tea", "rose petals", "pu???erh tea", "candied pineapple", "Pai Mu Tan tea",
                       "rooibos tea", "shredded coconut"]

    # Selects a steep time between 3 and 30 minutes
    steepTime = "**" + str(random.randint(3, 30)) + " minutes!**"

    # pulls a sample of up to 5 ingredients (minimum 2)
    recommendedIngredients = random.sample(ingredientsList, random.randint(2, 5))


    recipe = ''
    percent = int(100)
    itterationCount = len(recommendedIngredients)
    for ingredient in recommendedIngredients:

        # guarentees we end up with 100% of the tea
        if itterationCount > 1:
            randPercent = random.randint(1, (int(percent * 0.9)))

            percent = percent - randPercent
        else:
            randPercent = percent

        recipe = recipe + " **" + str(randPercent) + "%** of **" + ingredient + "**"

        # only appends "and" if we have remaining ingredients
        if itterationCount > 1:
            recipe = recipe + " and"
            itterationCount = itterationCount - 1

    return "I recommend you add " + recipe + " and steep it for " + steepTime

def hildaQuote():

    # Fetches our hilda quotes
    with open("hildaadivse.csv", 'r') as file:
        #quote = random.choice(list(file.read()))

        quote = random_line(file)

    quote = quote[:-2]

    # Short term log the quote sent
    print(quote)

    return "As Aunt Hilda always says... **" + quote + "**"

# Main driver method
def main():

    # Start client and let us know it is up and running
    @client.event
    async def on_ready():
        print("Startup Complete")


    # Message event listener
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        lynmsg = "Lyn's 24h stream will start in: " + "**" + lyndate() + "**"

        # Store a log of messages in RAM for debugging
        # NEVER write messages out to hard drive so we never
        # Have a permanent log
        print(message.content)

        # Listens for teamtime command
        if message.content.lower() == cfg.PREFIX + "teatime":
            response = teaRecipe()
            await message.channel.send(response)
            print("Sent teatime Response")

        # Listens for hilda command
        elif message.content.lower() == cfg.PREFIX + "hilda":
            response = hildaQuote()
            await message.channel.send(response)
            print("Sent Hilda Response")

        # Listens for wynlyn command
        elif message.content.lower() == cfg.PREFIX + "wynlyn":
            response = lynmsg
            await message.channel.send(response)
            print("Sent Lyn Response")

        # Listens for wrightstonk command
        elif message.content.lower() == cfg.PREFIX + "wrightstonk":
            response = getWrightSocks()
            await message.channel.send(response)
            print("Sent Sock Response")

    # Runs the client responder
    client.run(cfg.TOKENS['DISCORD_TOKEN'])


if __name__ == '__main__':
    print("---Starting---")
    init()
    main()
    print("---Stopping---")
