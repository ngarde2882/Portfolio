from ast import alias
import nextcord
import config
ROLE_VIEW = "ROLE_VIEW"
def custom_id(view:str, id:int) -> str:
    """return View w custom ID"""
    return f"{config.BOT_NAME}:{view}:{id}"
class RoleView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    async def handleclick(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        roleid = int(button.custom_id.split(':')[-1])
        role = interaction.guild.get_role(roleid)
        assert isinstance(role, nextcord.Role)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"your {role.name} has been removed", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"your {role.name} has been added", ephemeral=True)

    @nextcord.ui.button(label="Button2", emoji="🧑‍🍳", style=nextcord.ButtonStyle.blurple, custom_id=custom_id(ROLE_VIEW, config.GOOBER_ID))
    async def fun3(self, button, interaction):
        await self.handleclick(button, interaction)