import discord
import os
import time
from bs4 import BeautifulSoup
import requests
from discord.ext import commands
from keep_alive import keep_alive

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    # game = discord.Game("#HELP")
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="Fuzu Job Posts"))
    print("Bot's Ready")

    while True:
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

        time_wait = 10080
        embed.set_footer(text=f"This refreshes every 7 days")
        await dev_job_channel.send(embed=embed)
        
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)


keep_alive()
client.run(os.getenv('TOKEN'))
