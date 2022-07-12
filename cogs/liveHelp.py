"""
COG: Handles the settings for communities verification system from bot invasion
"""
import nextcord
from nextcord import Interaction, slash_command
from nextcord.channel import ChannelType
from nextcord.ext import commands
from colorama import init, Fore

init(autoreset=True)

MESSAGE_TO_LONG = "You message is to long. Allowed is maximum of 300 characters "


class Helpers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="help", description="Open help thread with Staff", dm_permission=False, guild_ids=[])
    @commands.has_permissions(create_public_threads=True)
    async def urgent_mng(self, interaction: Interaction, *, reason):
        thread = await interaction.channel.create_thread(name=f"@{interaction.user}-{interaction.user.id}",
                                                         reason='Help Wanted',
                                                         type=ChannelType.public_thread)

        animus = self.bot.get_user(360367188432912385)
        role = interaction.guild.get_role(785818459228995584)
        await thread.add_user(animus)
        await thread.add_user(self.bot.user)
        await thread.send(
            content=f"{interaction.user.mention} Please stay put. One of the X-Cash Staff or users with {role.mention} will be with"
                    f" you as soon as possible in order to resolve the issue at hand.\n"
                    f"Reason: ***{reason}***")
        await interaction.response.send_message(content=f'{interaction.user.mention} You have successfully opened '
                                                        f'up a thread. It can be access through link {thread.jump_url}',
                                                ephemeral=True, delete_after=360)
        print(
            Fore.LIGHTBLUE_EX + f'{interaction.user} Opened HELP on channel {interaction.channel} with topic: {reason}')

    @slash_command(name="discussion", description="Open up discussion (special-area)", dm_permission=False,
                   guild_ids=[])
    @commands.has_permissions(create_public_threads=True)
    async def help_mng(self, interaction: Interaction, topic):
        thread = await interaction.channel.create_thread(name=f"{topic}",
                                                         reason='Discussion topic',
                                                         type=ChannelType.public_thread)

        animus = self.bot.get_user(360367188432912385)
        role = interaction.guild.get_role(785818459228995584)
        await thread.add_user(animus)
        await thread.add_user(self.bot.user)
        await thread.send(
            content=f"{role.mention} {interaction.user.mention} has started a thread topic {topic}")
        await interaction.response.send_message(content=f'{interaction.user.mention} You have successfully opened '
                                                        f'up a thread. It can be access through link {thread.jump_url}',
                                                ephemeral=True, delete_after=360)
        print(
            Fore.LIGHTBLUE_EX + f'{interaction.user} Opened DISCUSSION on channel {interaction.channel} with topic: {topic}')

    @slash_command(name=f'close', description="Close the thread", dm_permission=False, guild_ids=[])
    async def close_thread(self, interaction: Interaction):
        if isinstance(interaction.channel, nextcord.Thread):
            thread = interaction.guild.get_thread(interaction.channel.id)

            # Get user ID from thread name
            thread_name = thread.name

            try:
                pos = thread_name.index("-")
                owner_user_id = thread_name[pos + 1:]
            except ValueError:
                owner_user_id = None

            guild = interaction.guild
            role = guild.get_role(785818459228995584)
            all_role_members = [x.id for x in role.members]

            if owner_user_id:
                # This breaks if its not a help thread
                if interaction.user.id == int(
                        owner_user_id) or interaction.user.id in all_role_members or interaction.user.id == 360367188432912385:
                    await thread.delete()
                else:
                    await interaction.response.send_message(
                        content=f'{interaction.user.mention} You are not allowed to '
                                f'close this thread. Only the user or members with role'
                                f' @contributors can do so', ephemeral=True,
                        delete_after=30)
            else:
                if interaction.user.id in all_role_members or interaction.user.id == 360367188432912385:
                    await thread.delete()
                else:
                    await interaction.response.send_message(
                        content=f'{interaction.user.mention} You are not allowed to '
                                f'close this thread. Only the user or members with role'
                                f' @contributors can do so', ephemeral=True,
                        delete_after=30)
        else:
            await interaction.response.send_message(content=f'This command works only in thread', ephemeral=True,
                                                    delete_after=30)


def setup(bot):
    bot.add_cog(Helpers(bot))
