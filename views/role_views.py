import constants as role_constants
import discord


PRONOUN_ROLES = {
    role_constants.he_him_role,
    role_constants.she_her_role,
    role_constants.they_them_role,
}
STAGE_ROLES = {
    role_constants.stage_1_role,
    role_constants.stage_2_role,
    role_constants.stage_3_role,
    role_constants.placement_role,
    role_constants.postgrad_role,
    role_constants.alumni_role,
}
COLOUR_ROLES = {
    role_constants.red,
    role_constants.orange,
    role_constants.yellow,
    role_constants.green,
    role_constants.blue,
    role_constants.purple,
    role_constants.pink,
}


class RoleSelect(discord.ui.Select):
    def __init__(
        self,
        custom_id: str,
        placeholder: str,
        options: list[tuple[str, int]],
        exclusive_group: set[int] | None = None,
        toggle: bool = False,
    ):
        select_options = [
            discord.SelectOption(label=label, value=str(role_id))
            for label, role_id in options
        ]
        super().__init__(
            custom_id=f"nucats:role_select:{custom_id}",
            placeholder=placeholder,
            min_values=1,
            max_values=len(select_options) if toggle else 1,
            options=select_options,
        )
        self.exclusive_group = exclusive_group
        self.toggle = toggle

    async def callback(self, interaction: discord.Interaction) -> None:
        if not isinstance(interaction.user, discord.Member) or interaction.guild is None:
            await interaction.response.send_message(
                "This menu can only be used in a server.", ephemeral=True
            )
            return

        selected_ids = {int(value) for value in self.values}
        roles = {
            role.id: role
            for role in interaction.guild.roles
            if role.id in selected_ids
        }
        if len(roles) != len(selected_ids):
            await interaction.response.send_message(
                "One of these roles is not configured in this server.", ephemeral=True
            )
            return

        try:
            if self.toggle:
                for role in roles.values():
                    if role in interaction.user.roles:
                        await interaction.user.remove_roles(
                            role, reason="Self-service role toggle"
                        )
                    else:
                        await interaction.user.add_roles(
                            role, reason="Self-service role toggle"
                        )
                message = "Your announcement roles were updated."
            else:
                selected_role = next(iter(roles.values()))
                existing_roles = [
                    role
                    for role in interaction.user.roles
                    if self.exclusive_group and role.id in self.exclusive_group
                ]
                if selected_role in interaction.user.roles:
                    await interaction.user.remove_roles(
                        selected_role, reason="Self-service role removal"
                    )
                    message = f"Removed the {selected_role.name} role."
                else:
                    if existing_roles:
                        await interaction.user.remove_roles(
                            *existing_roles, reason="Changing self-service role"
                        )
                    await interaction.user.add_roles(
                        selected_role, reason="Self-service role selection"
                    )
                    message = f"Added the {selected_role.name} role."
        except discord.Forbidden:
            message = "I cannot manage that role. Please contact a committee member."
        except discord.HTTPException:
            message = "Discord rejected that role update. Please try again shortly."

        await interaction.response.send_message(message, ephemeral=True)
        if interaction.message is not None:
            await interaction.message.edit(view=RolePanel())


class RolePanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(
            RoleSelect(
                "pronouns",
                "Pronouns: choose one",
                [
                    ("He/Him", role_constants.he_him_role),
                    ("She/Her", role_constants.she_her_role),
                    ("They/Them", role_constants.they_them_role),
                ],
                PRONOUN_ROLES,
            )
        )
        self.add_item(
            RoleSelect(
                "community",
                "Community: choose an option",
                [("External Student", role_constants.external_student_role)],
            )
        )
        self.add_item(
            RoleSelect(
                "announcements",
                "Announcements: select to toggle",
                [
                    ("University", role_constants.uni_announcements_role),
                    ("Events", role_constants.event_announcements_role),
                    ("Infrastructure", role_constants.infra_announcements_role),
                    ("General", role_constants.general_announcements_role),
                    ("IRL Updates", role_constants.irl_updates_role),
                ],
                toggle=True,
            )
        )
        self.add_item(
            RoleSelect(
                "stage",
                "Stage: choose one",
                [
                    ("Stage 1", role_constants.stage_1_role),
                    ("Stage 2", role_constants.stage_2_role),
                    ("Stage 3", role_constants.stage_3_role),
                    ("Placement", role_constants.placement_role),
                    ("Postgrad", role_constants.postgrad_role),
                    ("Alumni", role_constants.alumni_role),
                ],
                STAGE_ROLES,
            )
        )
        self.add_item(
            RoleSelect(
                "colours",
                "Colour: choose one",
                [
                    ("Red", role_constants.red),
                    ("Orange", role_constants.orange),
                    ("Yellow", role_constants.yellow),
                    ("Green", role_constants.green),
                    ("Blue", role_constants.blue),
                    ("Purple", role_constants.purple),
                    ("Pink", role_constants.pink),
                ],
                COLOUR_ROLES,
            )
        )
