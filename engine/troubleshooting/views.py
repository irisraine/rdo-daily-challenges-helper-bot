import nextcord
import engine.troubleshooting.messages as messages
import engine.troubleshooting.config as config


class MainMenuView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        options = [
            nextcord.SelectOption(
                label=data['content']['title'],
                value=key,
                emoji=data['content']['emoji']
            )
            for key, data in config.TROUBLESHOOTING_GROUPS.items()
        ]
        select = nextcord.ui.Select(placeholder="Выберите категорию...", options=options)
        select.callback = self.select_group_callback
        self.add_item(select)

    async def select_group_callback(self, interaction: nextcord.Interaction):
        selected_group = interaction.data["values"][0]
        await interaction.response.defer()
        await interaction.followup.send(**messages.group_menu(selected_group),
                                        view=GroupMenuView(selected_group),
                                        ephemeral=True)
        await interaction.message.edit(view=MainMenuView())


class GroupMenuView(nextcord.ui.View):
    def __init__(self, group):
        super().__init__(timeout=None)
        self.group = group
        group_data = config.TROUBLESHOOTING_GROUPS[group]["content"]

        select = nextcord.ui.Select(
            placeholder=group_data["select_menu_placeholder"],
            options=[
                nextcord.SelectOption(
                    label=data['title'],
                    value=key,
                    emoji=data['category_emoji']
                )
                for key, data in group_data["categories"].items()
            ],
        )
        select.callback = self.select_category_callback
        self.add_item(select)

    async def select_category_callback(self, interaction: nextcord.Interaction):
        selected_category = interaction.data["values"][0]
        await interaction.response.defer()
        await interaction.edit_original_message(**messages.category_menu(self.group, selected_category),
                                                view=CategoryMenuView(self.group, selected_category))


class CategoryMenuView(nextcord.ui.View):
    def __init__(self, group, category):
        super().__init__(timeout=None)
        self.group = group
        self.category = category
        category_data = config.TROUBLESHOOTING_GROUPS[group]["content"]["categories"][category]
        select = nextcord.ui.Select(
            placeholder="Укажите вашу проблему",
            options=[
                nextcord.SelectOption(
                    label=data['name'][0] if self.group == "errors" else data['name'],
                    value=key,
                    description=data['name'][1] if self.group == "errors" else None,
                    emoji=category_data['category_emoji']
                )
                for key, data in (category_data["solutions"].items())
            ]
        )
        select.callback = self.select_solution_callback
        self.add_item(select)

        button = nextcord.ui.Button(label="◀️ Назад", style=nextcord.ButtonStyle.blurple)
        button.callback = self.button_back_callback
        self.add_item(button)

    async def select_solution_callback(self, interaction: nextcord.Interaction):
        selected_solution = interaction.data["values"][0]
        await interaction.response.defer()
        await interaction.edit_original_message(**messages.solution_guide(self.group, self.category, selected_solution),
                                                view=None)

    async def button_back_callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(**messages.group_menu(self.group),
                                                view=GroupMenuView(self.group))
