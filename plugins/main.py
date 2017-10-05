# ██ ███    ███ ██████   ██████  ██████  ████████ ███████
# ██ ████  ████ ██   ██ ██    ██ ██   ██    ██    ██
# ██ ██ ████ ██ ██████  ██    ██ ██████     ██    ███████
# ██ ██  ██  ██ ██      ██    ██ ██   ██    ██         ██
# ██ ██      ██ ██       ██████  ██   ██    ██    ███████
from disco import cli
from disco.bot import Plugin
from disco.api.client import APIClient
from disco.types.channel import ChannelType
from disco.types import user

from json import loads as json

import requests as req
from bs4 import BeautifulSoup as bs

from random import randint, choice
from decimal import getcontext as setprec, Decimal as dec
from math import factorial
import re

from datetime import date
from time import localtime as lctime, gmtime
from dateutil.relativedelta import relativedelta as datedelta

import steam



class Main(Plugin):
   # ██    ██ ████████ ██ ██      ██ ████████ ██    ██
   # ██    ██    ██    ██ ██      ██    ██     ██  ██
   # ██    ██    ██    ██ ██      ██    ██      ████
   # ██    ██    ██    ██ ██      ██    ██       ██
   #  ██████     ██    ██ ███████ ██    ██       ██
   @Plugin.command("ping")
   def command_ping(self, event):
      """Ping/pongs the user
      """
      event.msg.reply("pong")

   @Plugin.command("bot")
   def command_bot(self, event):
      """Provides information about the bot
      """
      reply = ["__**About SteamBot (me!)**__"]
      [reply.append(f"**{k.title()}:** {botinfo[k]}") for k in botinfo]
      reply = ext_message(reply)
      event.msg.reply(reply)

   @Plugin.command("help", "[command:str]")
   def command_help(self, event, command="all"):
      """Display a list of available commands
      """
      command = command.lower()
      if(event.channel.type.value == ChannelType.DM.value):
         ext_print_help(event.msg.reply, command)
      else:
         dm = event.author.open_dm()
         ext_print_help(dm.send_message, command)
         event.msg.reply(f"{event.author.mention}, Sent you a DM with information.")

   @Plugin.command("announcement", "<time:str>, [title:str]")
   def command_anc(self, event, time, title="New Lobby"):
      """Makes a new announcement
      
      Arguments:
         time {str} --  The time of the event
      
      Keyword Arguments:
         title {str} -- The title of the announcement (default: {"New Lobby"})
      """
      ancChannel = self.state.channels.get(355006928314695680)
      ancGuild = self.state.guilds.get(355006927836676099)
      utc = lctime().tm_hour-gmtime().tm_hour
      if(355007107952803842 not in ancGuild.get_member(event.author).roles):
         event.author.open_dm().send_message("You don't have the right permissions to schedule an event")
         return 0
      ancChannel.send_message(ext_message([
         ":mega:   __**Announcement**__   :mega:",
         f"At **{time.replace('_', ' ')} (UTC{utc:+.0f})** there will be a **{title.replace('_', ' ')}**",
         "@everyone"
      ]))



   # ███    ███ ██ ███████  ██████
   # ████  ████ ██ ██      ██
   # ██ ████ ██ ██ ███████ ██
   # ██  ██  ██ ██      ██ ██
   # ██      ██ ██ ███████  ██████
   @Plugin.command("birthday", "<people:int>", aliases=["bday"])
   def command_birthday(self, event, people):
      """Calculates the birtday problem
      
      Arguments:
         people {int} -- The number of people
      """
      if(people > 365):
         perc = 1
      else:
         fracTop = dec(factorial(365))
         fracBot = dec((365**people)*factorial(365-people))
         perc = 1-dec(fracTop/fracBot)
      reply = f"In a room with {people} people, the percent that two of them share a birthday is {perc:.0%}"
      if(people >= 55 and people <= 322):
         reply += f"\n*Actually it's closer to {perc:.50%}*"
         
      event.msg.reply(reply)

   @Plugin.command("math", "<equation:str>")
   def command_math(self, event, equation):
      """Solves mathematical equations
      
      Arguments:
         equation {str} -- The equation to be solved
      """
      try:
         ans = eval(re.sub("[^0-9\\|\\>\\<\\/\\.\\-\\+\\*\\*\\*\\)\\(\\%]", "", equation))
         event.msg.reply(f"The answer is {ans:.2f}")
      except:
         event.msg.reply("That problem's too complicated for me. :sweat_smile:")



   # ██████   █████  ███    ██ ██████   ██████  ███    ███
   # ██   ██ ██   ██ ████   ██ ██   ██ ██    ██ ████  ████
   # ██████  ███████ ██ ██  ██ ██   ██ ██    ██ ██ ████ ██
   # ██   ██ ██   ██ ██  ██ ██ ██   ██ ██    ██ ██  ██  ██
   # ██   ██ ██   ██ ██   ████ ██████   ██████  ██      ██
   @Plugin.command("flip", "[coin:str")
   def command_flip(self, event, coin="quarter"):
      """Flips a coin, heads or tails

      Keyword Arguments:
         coin {str} -- The name of the coin (default: {"quarter"})
      """
      flip = randint(0, 1)
      val = "heads" if flip else "tails"
      event.msg.reply(f"The {coin} landed {val}.")

   @Plugin.command("random", "[minv:int], [maxv:int]", aliases=["rand"])
   def command_random(self, event, minv=1, maxv=10):
      """Generates a random number between minv and maxv

      Keyword Arguments:
         minv {int} -- Minumum random value (default: {1})
         maxv {int} -- Maximum random value (default: {10})
      """
      event.msg.reply(f"The random gods have spoken, and they say {randint(minv, maxv)}.")

   @Plugin.command("roll", "[die:int]")
   def command_roll(self, event, die=1):
      """Rolls any number of dice

      Keyword Arguments:
         die {int} -- The number of dice (default: {1})
      """
      event.msg.reply(f":game_die: rolled a {randint(1*die, 6*die)}.")



   # ███    ███  ██████  ███    ██ ███████ ██    ██
   # ████  ████ ██    ██ ████   ██ ██       ██  ██
   # ██ ████ ██ ██    ██ ██ ██  ██ █████     ████
   # ██  ██  ██ ██    ██ ██  ██ ██ ██         ██
   # ██      ██  ██████  ██   ████ ███████    ██
   @Plugin.command("inflation", "<amount:float>, <startyear:int>, [endyear:int]", aliases=["inflate", "infl"])
   def command_inflation(self, event, amount, startyear, endyear=(date.today()-datedelta(months=2)).year):
      """Calculates inflation in the US

      Arguments:
         amount {float} -- The amount of money to be inflated
         startyear {int} -- The year the amount is valued in

      Keyword Arguments:
         endyear {int} -- The year to be calculated          (default: {(date.today()-datedelta(months=2)).year})
      """
      ext_typing(event.channel.id)
      if(startyear < 1913):
         event.msg.reply(f"I can't go back that far, 1913 is my minumum.")
         return 0
      else:
         styr = f"{startyear}01"
      if(endyear > (date.today()-datedelta(months=2)).year):
         event.msg.reply(f"That hasn't happened yet!")
         return 0
      else:
         edyr = f"{endyear}01"
      amt = f"{amount:.2f}"
      try:
         res = req.get(f"https://data.bls.gov/cgi-bin/cpicalc.pl?cost1={amt}&year1={styr}&year2={edyr}")
         soup = bs(res.text, "html.parser")
         ans = soup.find(id="answer").string
         event.msg.reply(f"${amt} in {startyear} has the same buying power as {ans} in {endyear}.")
      except:
         event.msg.reply(f"I can't seem to talk to the government right now. :wink:")

   @Plugin.command("exchange",  "<amount:float>, <base:str>, <target:str>", aliases=["rate", "exch"])
   def command_exchange(self, event, amount,  base, target):
      """Foreign currency exchange rate calculator

      Arguments:
         amount {float} -- The amount of the base currency
         target {str} -- The target currency
      
      Keyword Arguments:
         base {str} -- The base currency                 (default: {"USD"})
      """
      target, base = target.upper(), base.upper()
      target = target.upper()
      base = base.upper()
      valid = ["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "GBP", "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB", "SEK", "SGD", "THB", "TRY", "ZAR", "EUR", "USD"]
      if(target not in valid or base not in valid):
         event.msg.reply("I'm sorry but I don't know that currency.")
         print(target, base)
         return 0
      try:
         dct = eval(req.get(f"http://api.fixer.io/latest?base={base}").text)['rates']
      except:
         event.msg.reply("I can't seem to connect to my exchange rate database.")
         return 0

      exc = amount*dct[target]
      event.msg.reply(f"{amount:.2f} {base} is equal to {exc:.2f} {target}")



   # ███████ ████████ ███████  █████  ███    ███
   # ██         ██    ██      ██   ██ ████  ████
   # ███████    ██    █████   ███████ ██ ████ ██
   #      ██    ██    ██      ██   ██ ██  ██  ██
   # ███████    ██    ███████ ██   ██ ██      ██
   @Plugin.command("steam", "<steamid:str>, [action:str]")
   def command_steam(self, event, steamid, action="info"):
      """Gets steam user information
      
      Arguments:
         steamid {str} -- The user's Steam64 address or custom address

      Keyword Arguments:
         action  {str} -- The action for steam       (default: {"info"})
      """
      ext_typing(event.channel.id)
      if(action not in ["info", "game", "status"]):
         event.msg.reply("I'm not sure I know what you mean.")
         return 0
      try:
         steamuser = steam.user(s64=steamid)
      except:
         try:
            steamuser = steam.user(sid=steamid)
         except:
            event.msg.reply("I can't seem to find that Steam user.")
            return 0
      if(steamuser.private):
         event.msg.reply("I'm really sorry, but that user is private.")
         return 0

      if(action == "info"):
         tot = 0
         for game in steamuser.games:
            tot += steamuser.games[game].hours
         tot = round(tot, 1)

         # Not sure on format :/
         # reply = ext_message(f"Summary of {steamuser.persona}", [
         #    f"{steamuser.counts['games']} Games, {round(tot, 1)} Hours",
         #    f"Level {steamuser.level}, {steamuser.counts['badges']} Badges",
         #    f"{steamuser.counts['friends']} Friends, {steamuser.counts['groups']} Groups"
         # ])
         reply = ext_message([
            f"__**Summary of {steamuser.persona}**__",
            f"**Name:** {steamuser.name}" if steamuser.name else None,
            f"**Location:** {steamuser.location['contents']}" if steamuser.location else None,
            f"**Account Date:**{steamuser.date}" if steamuser.date else None,
            f"**Status:** {steamuser.status['main'].title()}",
            f"**Games:** {steamuser.counts['games']}",
            f"**Hours:** {tot}",
            f"**Friends:** {steamuser.counts['friends']}",
            f"**Groups:** {steamuser.counts['groups']}"
         ])
         event.msg.reply(reply)
      elif(action == "status"):
         reply = f"{steamuser.persona} is currently {steamuser.status['main']}"
         reply += f", they're currently playing {steamuser.status['game']}." if steamuser.status["main"] == "in-game" else "."
         event.msg.reply(reply)
      elif(action == "game"):
         glist = [steamuser.games[g] for g in steamuser.games]
         game = choice(glist)

         reply = f"I pick {game.name}"
         if(game.hours == 0):
            reply += f", and {steamuser.persona} hasn't even played it!"
         else:
            tmad = f"{game.hours*60} minutes" if game.hours < 1 else f"{game.hours} hours"
            dt = date.fromtimestamp(game.last)
            reply += f", {steamuser.persona} has played for {tmad} and last played it on {dt.month}/{dt.day}/{dt.year}."
         event.msg.reply(reply)



#  ██████  ██       ██████  ██████   █████  ██      ███████
# ██       ██      ██    ██ ██   ██ ██   ██ ██      ██
# ██   ███ ██      ██    ██ ██████  ███████ ██      ███████
# ██    ██ ██      ██    ██ ██   ██ ██   ██ ██           ██
# ██████   ███████  ██████  ██████  ██   ██ ███████ ███████
with open("plugins/info.json", "r") as f:
   botinfo = json(f.read())
   commands = botinfo["commands"]
   cmdvalid = [cmd for key in commands for cmd in commands[key]]

botcli = cli.disco_main().client
apicli = APIClient(botcli.config.token)
# botcli.update_presence(user.Status.ONLINE, user.Game(user.GameType.DEFAULT, "Game", "http://www.steamcommunity.com/")) AttributeError: 'NoneType' object has no attribute 'send'

setprec().prec = 100
def ext_typing(ch):
   apicli.channels_typing(ch)
def ext_message(lines):
   reply = ""
   lines = [li for li in lines if li != None]
   for line in lines:
      reply += f"{line}\n"
   return reply
def ext_print_help(ctx, command):
      if(command == "all" or command not in cmdvalid):
         reply = "Use `help <command>` to view detailed information about a specific command."
         reply += "\nUse `help all` to view a list of all commands, not just available ones."
         reply += "\n\n__**Available Commands in British History**__\n"
         for key in commands:
            reply += f"\n__{key.title()}__"
            for comm in commands[key]:
               reply += f"\n**{comm}:** {commands[key][comm]['desc']}"
            reply += "\n"
      elif(command in cmdvalid):
         batch = [key for key in commands if command in commands[key]][0]
         reply = f"__**Information About {command.title()}**__\n"
         reply += f"\n**Category:** {batch.title()}"
         reply += f"\n**Description:** {commands[batch][command]['desc']}"
         reply += f"\n**Syntax:** `{commands[batch][command]['synt']}`"
         if('vars' in commands[batch][command]):
            for var in commands[batch][command]['vars']:
               reply += f"\n**{var}:** {commands[batch][command]['vars'][var]}"
      ctx(reply)