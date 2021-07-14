import discord
import os

import urllib.parse
from bs4 import BeautifulSoup
import requests
from discord.ext import commands
from keep_alive import keep_alive


client = commands.Bot(command_prefix=".")


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="LinkedIn Job Posts"
        ),
    )
    print("Bot's Ready")


@client.command()
async def jobs(ctx, skill, count=10):
    name = urllib.parse.quote_plus(skill)
    url = f"https://www.linkedin.com/jobs/search?keywords={name}&location=Kenya&geoId=100710459&trk=public_jobs_jobs-search-bar_search-submit&f_TPR=r604800&position=1&pageNum=0"

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")
    jobs = soup.find_all(
        "div",
        class_="base-card base-card--link base-search-card base-search-card--link job-search-card",
    )
    skill = skill.capitalize()
    for job in jobs:
        if count > 0:
            if job.find("h3", class_="base-search-card__title") is not None:
                job_title = (
                    job.find("h3", class_="base-search-card__title")
                    .text.replace("\n ", "")
                    .strip()
                )
            else:
                job_title = "None"

            if (
                job.find(
                    "img",
                    class_="artdeco-entity-image artdeco-entity-image--square-4 lazy-loaded",
                )
                is not None
            ):
                pic = job.find(
                    "img",
                    class_="artdeco-entity-image artdeco-entity-image--square-4 lazy-loaded",
                )["data-ghost-url"]
            else:
                pic = "https://static-exp1.licdn.com/sc/h/9a9u41thxt325ucfh5z8ga4m8"

            if job.find("h4", class_="base-search-card__subtitle").a is not None:
                company = (
                    job.find("h4", class_="base-search-card__subtitle")
                    .a.text.replace("\n ", "")
                    .strip()
                )
            else:
                company = "None"

            if job.find("span", class_="job-search-card__location") is not None:
                location = (
                    job.find("span", class_="job-search-card__location")
                    .text.replace("\n ", "")
                    .strip()
                )
            else:
                location = "None"

            if job.find("time", class_="job-search-card__listdate") is not None:
                posted = job.find("time", class_="job-search-card__listdate")[
                    "datetime"
                ]
            else:
                posted = "None"

            if job.find("a", class_="base-card__full-link") is not None:
                link = job.find("a", class_="base-card__full-link")["href"]
            else:
                link = "None"

            if job.find("p", class_="job-search-card__snippet") is not None:
                details = (
                    job.find("p", class_="job-search-card__snippet")
                    .text.replace("\n ", "")
                    .strip()
                )
            else:
                details = "None"

            embed = discord.Embed(
                title=job_title,
                description=f"Company Name - **{company}**",
                color=discord.Color.blue(),
            )
            embed.set_thumbnail(url=pic)
            embed.add_field(
                name="Details",
                value=details,
                inline=False,
            )
            embed.add_field(
                name="Date Posted",
                value=posted,
                inline=True,
            )
            embed.add_field(
                name="Location",
                value=location,
                inline=True,
            )
            embed.add_field(
                name="Link",
                value=link,
                inline=False,
            )
            embed.set_footer(text=f"{skill} Jobs on LinkedIn | Result No. {count}")

            await ctx.send(embed=embed)

            count = count - 1


keep_alive()
client.run(os.getenv("TOKEN"))
