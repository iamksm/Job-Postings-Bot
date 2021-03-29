import discord
import os
import time
from bs4 import BeautifulSoup
import requests
from discord.ext import commands
from keep_alive import keep_alive
import lxml

client = commands.Bot(command_prefix=".")

# try:
#   import lxml
# except:
#   os.system('pip install lxml')

@client.event
async def on_ready():
    # game = discord.Game("#HELP")
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="Fuzu Job Posts"))
    print("Bot's Ready")

@client.command()
async def jobs(ctx):
    # os.system('pip install lxml')
    dev_job_channel = discord.utils.get(client.get_all_channels(), name="💼-dev-job-opportunities")

    html_text = requests.get('https://www.fuzu.com/categories/it-software').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('div', class_='slim-card mb-2 job-card-padding')

    embed = discord.Embed(
                title='FUZU JOBS',
                description='ICT and Software Category',
                color=discord.Color.green())
    for job in jobs:
        title = job.find('h3', class_='font-18 slim-titles job-titles').text
        more_info = "https://www.fuzu.com" + job.find('a', class_='jobs-button continue-job desktop')['href']

        embed.add_field(name=title, value=more_info, inline=False)

    embed.set_footer(text="This message appears on command")
    await dev_job_channel.send(embed=embed)


keep_alive()
client.run(os.getenv('TOKEN'))
