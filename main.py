from secretaryBot import SecretaryBot
from utils.tools import Helpers

if __name__ == "__main__":
    helpers = Helpers()

    # Loading json settings
    bot_settings = helpers.read_json_file(file_name="botSetup.json")

    # Initiate bot instance
    secretary = SecretaryBot(bot_settings=bot_settings)

    secretary.run()
