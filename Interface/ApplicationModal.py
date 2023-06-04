import discord

from discord import TextStyle
from discord.ui import Modal, TextInput

class ApplicationModal(Modal, title="Ravenguard PMC Application Form"):
    def __init__(self):
        super().__init__(timeout=None)
    
        self.question_one = TextInput(
            label="What server or member you joined from?",
            style=TextStyle.short,
            placeholder="e.g PlatinumFive, Developer X#0001, etc",
            required=True
        )

        self.question_two = TextInput(
            label="Desired Callsign?",
            style=TextStyle.short,
            placeholder="e.g Fox, Jay, Andy, Eclipse, etc",
            required=True
        )

        self.question_three = TextInput(
            label="Your Playstyle?",
            style=TextStyle.short,
            placeholder="e.g Marksman, Pilot, CQB, etc",
            required=True
        )

        self.question_four = TextInput(
            label="Timezone?",
            style=TextStyle.short,
            placeholder="e.g GMT, EST, PST, etc",
            required=True
        )

        self.add_item(self.question_one)
        self.add_item(self.question_two)
        self.add_item(self.question_three)
        self.add_item(self.question_four)

    async def on_submit(self, interaction: discord.Interaction):
        print()