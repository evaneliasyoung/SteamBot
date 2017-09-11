from disco.bot import Plugin
from disco.api import client
from disco.types.channel import ChannelType
from yaml import load as yaml
from json import loads as json
from random import randint, choice
from datetime import date
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
      coin = "heads" if flip else "tails"
      event.msg.reply(f"The {coin} landed {coin}")

   @Plugin.command("random", "[minv:int], [maxv:int]", aliases=["rand"])
   def command_random(self, event, minv=1, maxv=10):
      """Generates a random number between minv and maxv

      Keyword Arguments:
         minv {int} -- Minumum random value (default: {1})
         maxv {int} -- Maximum random value (default: {10})
      """
      event.msg.reply(f"The random gods have spoken, and they say {randint(minv, maxv)}")

   @Plugin.command("roll", "[die:int]")
   def command_roll(self, event, die=1):
      """Rolls any number of dice

      Keyword Arguments:
         die {int} -- The number of dice (default: {1})
      """
      event.msg.reply(f":game_die: rolled a {randint(1*die, 6*die)}")



   # ███████ ████████ ███████  █████  ███    ███
   # ██         ██    ██      ██   ██ ████  ████
   # ███████    ██    █████   ███████ ██ ████ ██
   #      ██    ██    ██      ██   ██ ██  ██  ██
   # ███████    ██    ███████ ██   ██ ██      ██
   @Plugin.command("steam", "<steamid:str> [action:str]")
   def command_steam(self, event, steamid, action="info"):
      """Gets steam user information
      
      Arguments:
         steamid {str} -- The user's Steam64 address or custom address

      Keyword Arguments:
         action  {str} -- The action for steam       (default: {"info"})
      """
      apicli.channels_typing(event.channel.id)
      if(action not in ["info", "game", "status"]):
         event.msg.reply("I'm not sure I know what you mean")
         return 0
      try:
         steamuser = steam.user(s64=steamid)
      except:
         try:
            steamuser = steam.user(sid=steamid)
         except:
            event.msg.reply("I can't seem to find that Steam user")
            return 0
      if(steamuser.private):
         event.msg.reply("I'm really sorry, but that user is private")
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
         reply = ext_message(f"Summary of {steamuser.persona}", [
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
with open("config.yaml", "r") as f:
   config = yaml(f)
apicli = client.APIClient(config["token"])
with open("plugins/commands.json", "r") as f:
   commands = json(f.read())
   cmdvalid = [cmd for key in commands for cmd in commands[key]]

def ext_message(title, lines):
   reply = f"__**{title}**__\n"
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