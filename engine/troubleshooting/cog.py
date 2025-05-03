import nextcord
import json
from nextcord.ext import commands, application_checks
import engine.troubleshooting.messages as messages
import engine.troubleshooting.views as views
import engine.config as global_config
import engine.troubleshooting.config as config
import engine.troubleshooting.utils as utils


class Troubleshooting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(description="Размещение гайдов с решениями проблем")
    @application_checks.has_permissions(administrator=True)
    async def troubleshooting(self, interaction: nextcord.Interaction):
        troubleshooting_guides_channel = self.client.get_channel(global_config.TROUBLESHOOTING_GUIDES_CHANNEL_ID)
        await interaction.response.send_message(
            embed=nextcord.Embed(
                description="✅ _Размещение гайдов по различным аспектам игры RDO и возникающим проблемам._",
                colour=nextcord.Color.from_rgb(*global_config.BASIC_COLOR_CODE)), ephemeral=True
        )
        await troubleshooting_guides_channel.send(**messages.main_menu(), view=views.MainMenuView())

    @nextcord.slash_command(description="Обновить решения проблем")
    @application_checks.has_permissions(administrator=True)
    async def update(
            self,
            interaction: nextcord.Interaction,
            file: nextcord.Attachment = nextcord.SlashOption(
                description="Файл JSON с обновленными решениями",
                required=True)
    ):
        await interaction.response.defer()
        content = await file.read()
        filename = file.filename
        if not filename.endswith(".json"):
            return await interaction.followup.send(**messages.info(
                description="Пожалуйста, загрузите файл с расширением .json.",
                error=True))
        group = filename.split(".")[0]
        if group not in config.TROUBLESHOOTING_GROUPS.keys():
            return await interaction.followup.send(**messages.info(
                description="❌ Пожалуйста, загрузите файл с решениями проблем одной из имеющихся групп!\n"
                            "Файл должен иметь одно из четырех соответствующих имен: "
                            "bugs.json, errors.json, role_problems.json, tech_advices.json. Внимательно проверьте имя "
                            "загружаемого файла.",
                error=True))
        try:
            data = json.loads(content.decode("utf-8"))
        except json.JSONDecodeError as error:
            return await interaction.followup.send(**messages.info(
                description=f"❌ При попытке чтения переданного файла JSON произошла следующая ошибка: {error}. "
                            f"Обновление не было завершено, пожалуйста, повторите попытку.",
                error=True))
        is_correct_structure = utils.validate_json_structure(data)
        if is_correct_structure:
            group_json = config.TROUBLESHOOTING_GROUPS[group]["json"]
            is_correct_writing = utils.json_safewrite(group_json, data)
            if is_correct_writing:
                config.TROUBLESHOOTING_GROUPS[group]["content"] = utils.json_safeload(group_json)
                return await interaction.followup.send(**messages.info(
                    description="✅ Файл **{filename}** успешно загружен, "
                                "и решения в соответствующей группе вопросов обновлены!"))
            else:
                return await interaction.followup.send(**messages.info(
                    description=f"❌ При попытке записи переданного файла JSON произошла непредвиденная ошибка."
                                f"Обновление не было завершено, пожалуйста, повторите попытку.",
                    error=True))
        else:
            return await interaction.followup.send(**messages.info(
                description="❌ Структура файла некорректна. Обновление невозможно!\n"
                            "Внимательно проверьте содержимое файла, и в особенности удостоверьтесь, "
                            "что число решений в одном разделе не превышает 25 штук.",
                error=True))

    @nextcord.slash_command(description="Скачать JSON-файл с существующими решениями проблем")
    @application_checks.has_permissions(administrator=True)
    async def extract(
            self,
            interaction: nextcord.Interaction,
            action: str = nextcord.SlashOption(
                name="group",
                description="Категория гайда",
                choices={
                    "Баги игры": "bugs",
                    "Ошибки": "errors",
                    "Проблемы с ролями": "role_problems",
                    "Общие технические вопросы и полезности": "tech_advices"
                }
            )
    ):
        await interaction.response.defer()
        file = nextcord.File(fp=config.TROUBLESHOOTING_GROUPS[action]["json"], filename=f"{action}.json")
        await interaction.followup.send(file=file)
        await interaction.followup.send(**messages.info(
            description=f"📄 Вам отправлен файл **{action}.json**, "
                        f"содержащий гайды из категории *«{config.TROUBLESHOOTING_GROUPS[action]['name']}»*.\n"
                        f"Можно использовать его для редактирования имеющихся вопросов и добавления новых."))


def setup(client):
    client.add_cog(Troubleshooting(client))
