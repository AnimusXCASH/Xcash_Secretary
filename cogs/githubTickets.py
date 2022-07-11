"""
COG: Handles the settings for communities verification system from bot invasion
"""

from nextcord import Interaction, SlashOption, slash_command, TextChannel, Embed, Colour, TextInput
from nextcord.ext import commands
from datetime import datetime
from uuid import uuid4
from colorama import Fore, init

init(autoreset=True)

MESSAGE_TO_LONG = "You message is to long. Allowed is maximum of 300 characters "


class GithubTicketing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def open_ticket(self, title, repo_addr, body, label, ticket_id):
        """
        Return address and link to repo issue
        """
        r = self.bot.github.get_repo(repo_addr)
        l = r.get_label(label)
        try:
            issue = r.create_issue(title=f'[DSC]{title} ({ticket_id})', body=body, labels=[l])
            return f"https://github.com/{repo_addr}/issues/{issue.number}"
        except Exception as e:
            print(Fore.LIGHTRED_EX + f'{e}')
            return 1

    def get_github_repo(self, repo):
        """
        Get github repo
        """
        if repo == "xpayment":
            return "X-CASH-official/X-Payment"
        elif repo == "androidWallet":
            return "X-CASH-official/android-wallet"
        elif repo == "desktopWallet":
            return "X-CASH-official/desktop-wallet"

    def get_tag(self, repo, tag_selection):
        """
        Get available tags
        """
        if repo == "xpayment":
            if tag_selection == "buggy":
                return "◼ Type: Bug"
            elif tag_selection == "question":
                return "◼ Type: Question"
            elif tag_selection == "featureNew":
                return "◼ Type: Enhancement"

    @slash_command(name="ticket", description="Open issue to Github repo", dm_permission=False)
    async def ticket_mng(self, interaction: Interaction,
                         repo=SlashOption(
                             name='repo',
                             choices={"X-Payment": "xpayment",
                                      "Desktop Wallet": "desktopWallet",
                                      "Android Wallet": "androidWallet",
                                      "X-Bank": "xbank",
                                      "Web-page": "webpage"},
                             description='Help commands for X-Payment system'),
                         tcks=SlashOption(
                             name='type',
                             choices={"Bug": "buggy",
                                      "Feature": "featureNew",
                                      "Question": "question"},
                             description='Type of ticket'),
                         *, title: str, ticket_text: str
                         ):
        ticket_id = uuid4()

        body_text = f"Discord Channel: {interaction.channel}\n" \
                    f"Discord Username: {interaction.user} (ID: {interaction.user.id})\n" \
                    f"Ticket ID: {ticket_id}\n\n"
        body_text += ticket_text

        if repo == 'xpayment':
            tag = self.get_tag(repo=repo, tag_selection=tcks)
            repo_addr = self.get_github_repo(repo)
            issue_link = self.open_ticket(title=title, repo_addr=repo_addr, body=body_text, label=tag,
                                          ticket_id=ticket_id)
            ecosystem = "X-Payment"

        elif repo == "desktopWallet":
            tag = self.get_tag(repo=repo, tag_selection=tcks)
            repo_addr = self.get_github_repo(repo)
            issue_link = self.open_ticket(title=title, repo_addr=repo_addr, body=body_text, label=tag,
                                          ticket_id=ticket_id)
            ecosystem = "Desktop Wallet"

        elif repo == "androidWallet":
            tag = self.get_tag(repo=repo, tag_selection=tcks)
            repo_addr = self.get_github_repo(repo)
            issue_link = self.open_ticket(title=title, repo_addr=repo_addr, body=body_text, label=tag,
                                          ticket_id=ticket_id)
            ecosystem = "Android Wallet"

        elif repo == "xbank":
            tag = self.get_tag(repo=repo, tag_selection=tcks)
            repo_addr = self.get_github_repo(repo)
            issue_link = self.open_ticket(title=title, repo_addr=repo_addr, body=body_text, label=tag,
                                          ticket_id=ticket_id)
            ecosystem = "X-Bankt"
        elif repo == "webpage":
            pass

        if isinstance(issue_link, str):
            info_user = Embed(title=f":new: {ecosystem} {tag}",
                              description=f"You have successfully opened ticket to X-CASH-official {repo_addr} repo.",
                              timestamp=datetime.utcnow())
            info_user.add_field(name=f':ID: Ticket ID',
                                value=f"{ticket_id}",
                                inline=False)
            info_user.add_field(name=f':ID: Link to Issue on Github',
                                value=f"[Issue]({issue_link})",
                                inline=False)
            await interaction.response.send_message(content=f'{ticket_id}', embed=info_user, ephemeral=True)

        else:
            print("There has been error")


def setup(bot):
    bot.add_cog(GithubTicketing(bot))
