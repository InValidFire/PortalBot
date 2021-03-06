import discord
from discord.ext import commands
from datetime import datetime
import random
import threading

#Counts current lines in a file.
def LineCount():
  file = open("DailyQuestions.txt", "r")
  line_count = 0
  for line in file:
    if line != "\n":
      line_count += 1
  file.close()
  print(line_count)


class DailyCMD(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  #Waits for either the approval or denial on a question suggestion
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.user_id != 777361919211732993:
      if payload.channel_id == 787803726168588318:
        if str(payload.emoji) == "✅":
          channel = self.bot.get_channel(payload.channel_id)
          msg = await channel.fetch_message(payload.message_id)
          embed = msg.embeds[0]
          contentval = embed.fields[2].value
          linec, question = contentval.split(" | ")
          file = open("DailyQuestions.txt", "r")
          line_count = 0
          for line in file:
            if line != "\n":
              line_count += 1
          file.close()
          lc = line_count + 1

          embed = discord.Embed(title = "Suggestion Approved", description = "<@" + str(payload.user_id) + "> has approved a suggestion! ", color = 0x31f505)
          embed.add_field(name = "Question Approved", value = str(question))
          await channel.send(embed = embed)

          f = open("DailyQuestions.txt", "a")
          f.write(str(lc) + " - " + question + "\n")
          f.close()
          reactions = ['✅', '❌']
          for emoji in reactions: 
            await msg.clear_reaction(emoji)
        
        

        
        elif str(payload.emoji) == "❌":
          embed = msg.embeds[0]
          contentval = embed.fields[2].value
          channel = self.bot.get_channel(payload.channel_id)
          linec, question = contentval.split(" | ")
          embed2 = discord.Embed(title = "Suggestion Approved", description = "<@" + str(payload.user_id) + "> has approved a suggestion! ", color = 0xf50505)
          embed.add_field(name = "Question Approved", value = "Question Approved: " + str(question))
          await channel.send(embed = embed2)
          reactions = ['✅', '❌']
          for emoji in reactions: 
            await msg.clear_reaction(emoji)
        else:
          return
      else:
        return
    else:
      return


  #Lists all current questions in the textfile. 
  @commands.command()
  async def listq(self, ctx):
    with open('DailyQuestions.txt', 'r') as file:
      author = ctx.message.author
      msg = file.read(984).strip()
      while len(msg) > 0:
        em = discord.Embed(title = "Current Recorded Questions", description = "Requested by: " + author.mention, color = 0xb10d9f)
        em.add_field(name = "Questions:", value = msg)
        await ctx.send(embed = em)
        msg = file.read(1024).strip()

  #Sends a random question.
  @commands.command()
  async def dailyq(self, ctx):
    await ctx.channel.purge(limit = 1)
    author = ctx.message.author
    rew = open('DailyQuestionsC.txt', "r")
    copy = open("DailyQuestions.txt", "a")
    for line in rew:
      if line != "\n":
        copy.write(line)
    rew.close()
    copy.close()
    file = open("DailyQuestions.txt", "r")
    line_count = 0
    for line in file:
      if line != "\n":
        line_count += 1
    lc = line_count + 1
    file.close()
    A = random.randint(0 , int(lc))

    with open("DailyQuestions.txt", "r") as myFile:
      for num, line in enumerate(myFile, 1):
        if num == A:
          Numberl, Q = line.split(" - ")
          fullLine = line
    
    with open("DailyQuestions.txt", "r") as f:
      lines = f.readlines()
    with open("DailyQuestions.txt", "w") as f:
      for line in lines:
        if line.strip("\n") != fullLine:
          f.write(line)
        

    Dailyq = discord.Embed(title = "❓ QUESTION OF THE DAY ❓", description = "**" + Q + "**", color = 0xb10d9f)
    Dailyq.set_footer(text="Got a question? Use the suggest command! \n*Usage:* >suggestq (Your Question Here)")
    await ctx.send(embed = Dailyq)

      
   
  
  #Add's a question to the database
  @commands.command()
  async def addq(self, ctx, * , reason):
      file = open("DailyQuestions.txt", "r")
      line_count = 0
      for line in file:
        if line != "\n":
          line_count += 1
      LC = line_count + 1
      file.close()
      file = open("DailyQuestions.txt", "a")
      file.write(str(LC) + " - " + reason + "\n")
      file.close()
      file = open("DailyQuestionsC.txt", "r")
      line_count = 0
      for line in file:
        if line != "\n":
          line_count += 1
      LC = line_count + 1
      file.close()
      file = open("DailyQuestionsC.txt", "a")
      file.write(str(LC) + " - " + reason + "\n")
      file.close()
      await ctx.send("Question added to the list! \n**Added:** " + reason + "\n**Line Number:** " + str(LC))
  
  @addq.error
  async def addq_error(self,ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("You didn't include a question!")

  #Removes a question from the database. [BROKEN]
  @commands.command()
  async def removeq(self, ctx, *, reason):
    file = open("DailyQuestions.txt", "r")
    for line in file:
      Num, Q = line.split(" - ")
      if reason == Num:
        question = line
      file.close()
    with open("DailyQuestions.txt", "r") as f:
      lines = f.readlines()
    with open("DailyQuestions.txt", "w") as f:
      for line in lines:
        if line.strip("\n") != question:
          f.write(line)

    file = open("DailyQuestionsC.txt", "r")
    for line in file:
      Num, Q = line.split(" - ")
      if reason == Num:
        question = line
      file.close()
    with open("DailyQuestionsC.txt", "r") as f:
      lines = f.readlines()
    with open("DailyQuestionsC.txt", "w") as f:
      for line in lines:
        if line.strip("\n") != question:
          f.write(line)
    await ctx.send("**REMOVED:** " + line)
  
  @removeq.error
  async def removeq_error(self,ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("You didn't include a number! Please refer to `>listq` for a question number!")

  #Forces a certain question. 
  @commands.command()
  async def forceq(self, ctx, *, reason):
    await ctx.channel.purge(limit = 1)
    author = ctx.message.author
    file = open("DailyQuestions.txt", "r")
    for line in file:
      Num, Q = line.split(" - ")
      if reason == Num:
        question = line
    file.close()
    Dailyq = discord.Embed(title = "❓ QUESTION OF THE DAY ❓", description = "**" + Q + "**", color = 0xb10d9f)
    await ctx.send(embed = Dailyq)

  
  @forceq.error
  async def forceq_error(self,ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("You didn't include a number! Please refer to `>listq` for a question number!")
  
  #Suggests a question and sends it to the moderators. 
  @commands.command()
  async def suggestq(self, ctx, *, question):
    author = ctx.message.author
    channel = ctx.message.channel
    guild = ctx.message.guild
    DMChannel = await ctx.author.create_dm()
    if channel.name == "bot-spam":
      print(channel)
      def check(m):
        return m.content is not None and m.channel == channel and m.author is not self.bot.user

      await channel.send("Are you sure you want to submit this question for approval? \n**Warning:** You will be subjected to a warn/mute if your suggestion is deemed inappropriate! \n*Please respond with either `YES` or `NO`*")
      msg2 = await self.bot.wait_for('message', check=check)
      if "YES" in msg2.content:
        msga = await ctx.send("Standby, sending your suggestion. ")
        channels = await self.bot.fetch_channel(787803726168588318)
        embed = discord.Embed(title = "Daily Question Suggestion", description = str(author.name) + " suggested a question in <#" + str(channel.id) + ">", color = 0xfcba03)
        embed.add_field(name = "Suggestion:", value = str(question))
        #QuestionSuggestQ.txt
        file = open("QuestionSuggestQ.txt", "r")
        line_count = 0
        for line in file:
          if line != "\n":
            line_count += 1
        file.close()
        lc = line_count + 1
        embed.add_field(name = "Approving/Denial Command", value = "\n✅ - Approve \n❌ - Reject")
        embed.add_field(name = "Developer Payload", value = str(lc) + " | " + str(question))
        timestamp = datetime.now()
        embed.set_footer(text=guild.name + " | Date: " + str(timestamp.strftime(r"%x")))
        msg = await channels.send(embed = embed)
        with open("QuestionSuggestQ.txt", "a") as f:
          f.write(str(lc) + " - " + question + "\n")
        reactions = ['✅', '❌']
        for emoji in reactions: 
          await msg.add_reaction(emoji)
        await msga.edit(content = "I have sent your question! \nPlease wait for an admin to approve it. ")
      else:
        print("invalid")
    else:
      await ctx.channel.purge(limit = 1)
      embed = discord.Embed(title = "Woah Slow Down!", description = "This command is locked to <#588728994661138494>!\nI also sent your command in your DM's so all you have to do is just copy it and send it in the right channel!", color = 0xb10d9f)
      msg = await ctx.send(embed = embed, delete_after = 6)
      await DMChannel.send("Here is your command! \nPlease send it in #bot-spam!")
      await DMChannel.send(">suggestq " + str(question))
      

      



#Inactive as @client.event is being used

'''
  @commands.command()
  async def confirmq(self, ctx, number):
    file = open("QuestionSuggestQ.txt", "r")
    for line in file:
      Num, Q = line.split(" - ")
      if number == Num:
        question = line

    #Removing Question
    with open("QuestionSuggestQ.txt", "r") as f:
      lines = f.readlines()

    with open("QuestionSuggestQ.txt", "w") as f:
      for line in lines:
        if line.strip("\n") != question:
          f.write(line)
    file.close()


    ---

else:
        file = open("DailyQuestions.txt", "r")
        line_count = 0
        for line in file:
          if line != "\n":
            line_count += 1
        lc = line_count + 1
        file.close()
        A = random.randint(0 , int(lc))

        with open("DailyQuestions.txt", "r") as myFile:
          for num, line in enumerate(myFile, 1):
            if num == A:
              Numberl, Q = line.split(" - ")
              fullLine = line
    
        with open("DailyQuestions.txt", "r") as f:
          lines = f.readlines()
        with open("DailyQuestions.txt", "w") as f:
          for line in lines:
            if line.strip("\n") != fullLine:
              f.write(line)
        

        Dailyq = discord.Embed(title = "❓ QUESTION OF THE DAY ❓", description = "**" + Q + "**", color = 0xb10d9f)
        Dailyq.set_footer(text="Got a question you want to add? Use the suggest command! \nUsage: >suggestq (Your Question Here)")
        await ctx.send(embed = Dailyq)
'''






def setup(bot):
  bot.add_cog(DailyCMD(bot))
