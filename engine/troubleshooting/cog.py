import nextcord
import json
import logging
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
                description="❌ Пожалуйста, загрузите файл с решениями проблем одной из имеющихся категорий!\n"
                            "Файл должен иметь одно из четырех соответствующих имен: "
                            "*bugs.json*, *errors.json*, *role_problems.json*, *tech_advices.json*. "
                            "Внимательно проверьте имя загружаемого файла.",
                error=True))
        group_name = config.TROUBLESHOOTING_GROUPS[group]["name"]
        try:
            data = json.loads(content.decode("utf-8"))
        except json.JSONDecodeError as error:
            logging.warning(f"Попытка обновления содержимого раздела \"{group_name}\" отклонена из-за ошибки при "
                            f"раскодировке переданного файла с с данными.")
            return await interaction.followup.send(**messages.info(
                description=f"❌ При попытке чтения переданного файла JSON произошла следующая ошибка: **{error}**. "
                            f"Обновление не было завершено, пожалуйста, повторите попытку.",
                error=True))

        validation_json_structure_status = utils.validate_json_structure(data)
        if validation_json_structure_status[0] == 0:
            group_json = config.TROUBLESHOOTING_GROUPS[group]["json"]
            is_correct_writing = utils.json_safewrite(group_json, data)
            if is_correct_writing:
                config.TROUBLESHOOTING_GROUPS[group]["content"] = utils.json_safeload(group_json)
                logging.info(f"Содержимое раздела \"{group_name}\" успешно обновлено.")
                return await interaction.followup.send(**messages.info(
                    description=f"✅ Файл **{filename}** успешно загружен, и гайды "
                                f"в категории \"{group_name}\" обновлены!"))
            else:
                logging.error(f"Попытка обновления содержимого раздела \"{group_name}\" отклонена из-за непредвиденной "
                              f"ошибки при записи обновленного файла с данными.")
                return await interaction.followup.send(**messages.info(
                    description="❌ При попытке записи переданного файла JSON произошла непредвиденная ошибка."
                                "Обновление не было завершено, пожалуйста, повторите попытку.",
                    error=True))
        elif validation_json_structure_status[0] == 1:
            logging.warning(f"Попытка обновления содержимого раздела \"{group_name}\" отклонена из-за некорректной "
                            f"структуры переданного файла с данными.")
            return await interaction.followup.send(**messages.info(
                description=f"❌ Содержимое файла некорректно. Обновление невозможно!\n\n"
                            f"При валидации файла обнаружилась следующая проблема: \n"
                            f"__**{validation_json_structure_status[1]}**__\n Внимательно проверьте содержимое файла, "
                            f"и исправьте найденную ошибку в соответствии с полученной рекомендацией, после чего "
                            f"повторите попытку обновления, заново загрузив исправленный файл.",
                error=True))
        else:
            logging.error(f"Попытка обновления содержимого раздела \"{group_name}\" отклонена из-за непредвиденной "
                          f"ошибки при чтении переданного файла с данными.")
            return await interaction.followup.send(**messages.info(
                description="❌ При попытке чтения переданного файла JSON произошла непредвиденная ошибка. "
                            "Обновление не было завершено, пожалуйста, повторите попытку.",
                error=True))

    @nextcord.slash_command(description="Скачать JSON-файл с существующими решениями проблем")
    @application_checks.has_permissions(administrator=True)
    async def extract(
            self,
            interaction: nextcord.Interaction,
            group: str = nextcord.SlashOption(
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
        file = nextcord.File(fp=config.TROUBLESHOOTING_GROUPS[group]["json"], filename=f"{group}.json")
        await interaction.followup.send(file=file)
        await interaction.followup.send(**messages.info(
            description=f"📄 Вам отправлен файл **{group}.json**, "
                        f"содержащий гайды из категории *«{config.TROUBLESHOOTING_GROUPS[group]['name']}»*.\n"
                        f"Можно использовать его для редактирования имеющихся вопросов и добавления новых."))


def setup(client):
    client.add_cog(Troubleshooting(client))
