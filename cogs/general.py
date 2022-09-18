
import platform
import random
import datetime

import aiohttp
import discord
import requests
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot
    @commands.hybrid_command(
        name="help",
        aliases=["h","hel"], 
        description="List all commands the bot has loaded."
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(title="Help", description="List of available commands:", color=0x32DAAA)
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition('\n')[0]
                data.append(f"<a:Ax:1020899073726889985>**{prefix}{command.name}** \n {description} - {command.aliases}")
            help_text = "\n".join(data)
            embed.add_field(name=f'<a:ar:1020898563305263124>{i.capitalize()}', value=f'{help_text}', inline=True)
        await context.send(embed=embed)
      
    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    @checks.not_blacklisted()
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.
        
        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="About me <:thinkx:1019277696787816509>",
            color=0xDA004E
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="<a:shinybadge:1019274975317852230> Owner:",
            value="**`@✓ƘɑӀɑí✘ 𖠌#2007`**",
            inline=True
        )
        embed.add_field(
            name="<:python:1019275141684940872> Python Version:",
            value=f" `{platform.python_version()}`",
            inline=True
        )
        embed.add_field(
            name="<:Support:1019275319556976742> Prefix:",
            value=f"` / (Slash Commands) or {self.bot.config['prefix']} for normal commands`",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {context.author}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        aliases=["si"], 
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, context: Context) -> None:
        own=context.guild.owner
        roles = [role.mention for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{context.guild}",
            color=0xDA004E
        )
        if context.guild.icon is not None:            
            embed.set_thumbnail(
                url=context.guild.icon.url
            )
        embed.add_field(
          name="Server Owner",
          value=f"{own}"
        ) 
        embed.add_field(
            name="Server ID",
            value=context.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=context.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {context.guild.created_at}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.
        
        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="<:zxtng_pepePing:1019273564886679592> Pong!",
            description=f"The bot latency is **{round(self.bot.latency * 1000)}ms.**",
            color=0xDA004E
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    @checks.not_blacklisted()
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.
        
        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={self.bot.config['application_id']}&scope=bot+applications.commands&permissions={self.bot.config['permissions']}).",
            color=0xD75BF4
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="server",
        description="Get the invite link of the discord server of the bot for some support.",
    )
    @checks.not_blacklisted()
    async def server(self, context: Context) -> None:
        embed = discord.Embed(
            description=f"Join the support server for the bot by clicking [here](https://discord.gg/4RpR86WasS).",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    @checks.not_blacklisted()
    @app_commands.describe(question="The question you want to ask.")
    async def eight_ball(self, context: Context, *, question: str) -> None:
        """
        Ask any question to the bot.
        
        :param context: The hybrid command context.
        :param question: The question that should be asked by the user.
        """
        answers = ["It is certain.", "It is decidedly so.", "You may rely on it.", "Without a doubt.",
                   "Yes - definitely.", "As I see, yes.", "Most likely.", "Outlook good.", "Yes.",
                   "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                   "Cannot predict now.", "Concentrate and ask again later.", "Don't count on it.", "My reply is no.",
                   "My sources say no.", "Outlook not so good.", "Very doubtful."]
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0xDA004E
        )
        embed.set_footer(
            text=f"The question was: {question}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="bitcoin",
        description="Get the current price of bitcoin.",
    )
    @checks.not_blacklisted()
    async def bitcoin(self, context: Context) -> None:
        """
        Get the current price of bitcoin.
        
        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript")  # For some reason the returned content is of type JavaScript
                    embed = discord.Embed(
                        title="Bitcoin price",
                        description=f"The current price is **${data['bpi']['USD']['rate']} :dollar:**",
                        color=0xDA004E
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)
    @commands.hybrid_command(
        name="whois",
        aliases=["ui", "who"], 
        description="who Get some information about the user.",
    )
    @checks.not_blacklisted()
    async def whois(self, context: Context, user: discord.User) -> None:      

        embed = discord.Embed(
            color=0xDA004E
        )
        embed.set_author(
            name=f"{user.name}'s information"
        ) 
        embed.set_thumbnail(
          url=str(user.avatar.url)
        )
        embed.add_field(
            name="User name",
            value=user.name,
            inline=True
        )
        embed.add_field(
            name="tag",
            value=f"{user.discriminator}",
            inline=True
        )
        embed.add_field(
            name="Bot? ",
            value=user.bot,
        )
        embed.add_field(
            name="User ID",
            value=user.id,
            inline=False
        )
        embed.add_field(
            name="Account created",    
        value=user.created_at.strftime(
"%d/%m/%Y, %H:%M:%S"
        ), 
            inline=True
        ) 
        embed.add_field(
            name="Joined the server",
      value=user.joined_at.strftime(
              "%d/%m/%Y, %H:%M:%S"
        ),
            inline=True
        ) 
        embed.add_field(
            name="Highest Role",
            value=f"{user.top_role.mention}",
        )
        embed.set_footer(
              text=f"Requested by {context.author}"
            ) 
        await context.send(embed=embed)
      
    @commands.hybrid_command(
        name="emoji",
        description="Detail of the emoji.",
     ) 
    @checks.not_blacklisted()
    async def emoji(self, context: Context, emoji: discord.PartialEmoji) -> None:      

        embed = discord.Embed(
            color=0xDA004E
        )
        embed.set_author(
            name="Emoji Info"
        ) 
        embed.set_thumbnail(
            url=str(emoji.url)
        )
        embed.add_field(
            name="Name",
            value=emoji.name,
            inline=True
       )
        embed.add_field(
            name="ID",
            value=emoji.id,
            inline=True
       )   
        embed.add_field(
            name="Animated? ",
            value=emoji.animated,
            inline=True
       )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="avatar",
        aliases=["av", "pfp"], 
        description="Get avatar of the user.",
        )
    @checks.not_blacklisted()
    async def avatar(self, ctx: Context, user: discord.User = None):
       if user == None:
            embed = discord.Embed(
            color=0xDA004E
          ) 
            embed=discord.Embed(
      description='<a:error:1020525852670296134> Please specify a user',
            color=0xE50B0B
            ) 
            await ctx.send(embed=embed)
       else:
            embed = discord.Embed(
              color=0xDA004E
            ) 
            embed.set_author(
              name=f"{user.name}'s avatar"
            )
            embed.set_image(
              url=user.avatar
            ) 
           
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))