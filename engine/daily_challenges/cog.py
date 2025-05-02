import nextcord
from nextcord.ext import commands, tasks, application_checks
import logging
import engine.config as global_config
import engine.daily_challenges.config as config
import engine.daily_challenges.messages as messages


class DailyChallenges(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduled_publish.start()

    async def daily_challenges_guide(self):
        channel = self.client.get_channel(global_config.DAILY_CHALLENGES_TUTORIALS_CHANNEL_ID)

        header_messages = messages.get_header_messages()
        tutorial_messages = messages.get_tutorial_messages()
        madam_nazar_location_message = messages.get_madam_nazar_location_message()

        if not tutorial_messages:
            logging.error("Данные о дейликах не могут быть отображены из-за ошибки")
            return

        await channel.send(
            embed=header_messages['cover'].embed,
            file=header_messages['cover'].image
        )
        for category in ('general', 'role'):
            embeds, images = [header_messages[category].embed], [header_messages[category].image]
            embeds.extend([msg.embed for msg in tutorial_messages[category]])
            images.extend([msg.image for msg in tutorial_messages[category]])
            await channel.send(embeds=embeds, files=images)

        await channel.send(
            embed=madam_nazar_location_message.embed,
            file=madam_nazar_location_message.image
        )
        logging.info("Данные о дейликах успешно отображены!")

    @tasks.loop(time=config.LAUNCH_TIME)
    async def scheduled_publish(self):
        await self.daily_challenges_guide()

    @nextcord.slash_command(description="Ручная публикация гайдов по дейликам")
    @application_checks.has_permissions(administrator=True)
    async def daily_challenges(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(
            embed=nextcord.Embed(
                description="✅ _Публикация дейликов в специальном канале начинается!_",
                colour=nextcord.Color.from_rgb(*global_config.BASIC_COLOR_CODE)
            ), ephemeral=True
        )
        await self.daily_challenges_guide()

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.scheduled_publish.is_running():
            self.scheduled_publish.start()


def setup(bot: commands.Bot):
    bot.add_cog(DailyChallenges(bot))
