from nextcord.ext import commands
from nextcord import Intents
from colorama import init, Fore
from github import Github


class SecretaryBot(commands.Bot, ):
    def __init__(self, bot_settings):
        self.bot_settings = bot_settings
        super().__init__(
            command_prefix=commands.when_mentioned_or(self.bot_settings['command']),
            intents=Intents.all())
        self.remove_command('help')
        self.cogs_to_load = self.bot_settings["cogs"]
        self.load_cogs()
        self.github = Github(login_or_token=self.bot_settings["githubToken"])

    def load_cogs(self):
        notification_str = Fore.LIGHTBLUE_EX + '+++++++++++++++++++++++++++++++++++++++ \n' \
                                               'LOADING \COGS....        \n'
        for c in self.cogs_to_load:
            try:
                self.load_extension(c)
                notification_str += Fore.LIGHTGREEN_EX + f'| {c} ... DONE \n'
            except Exception as error:
                notification_str += Fore.LIGHTRED_EX + f'| {c} --> {error}\n'
                raise
        notification_str += Fore.LIGHTBLUE_EX + 'COG loading COMPLETED.....\n+++++++++++++++++++++++++++++++++++++++'
        print(notification_str)

    def run(self):
        super().run(self.bot_settings['token'], reconnect=True)

    def get_command_str(self):
        return self.bot_settings['command']
