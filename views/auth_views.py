from email.message import EmailMessage

import discord, string, random, smtplib
from discord.ui import Button, Modal, TextInput, View

from utils import check_student_number
from constants import verified_role, smtp_server, smtp_port, smtp_username, smtp_password, smtp_from

class AuthModal(Modal):
    def __init__(self):
        super().__init__(title="Verify your Student Status", timeout=None)

        self.name = TextInput(label="Please enter your name..", 
                         placeholder="As it appears on your student ID card. (e.g. Alan Turing)", 
                         required=True, 
                         max_length=128)
        self.add_item(self.name)

        self.student_id = TextInput(label="Please enter your student ID number.", 
                         placeholder="Full number please. (e.g. 123456789)", 
                         required=True, 
                         max_length=9)
        self.add_item(self.student_id)

    async def on_submit(self, interaction: discord.Interaction):
        if not self.name.value or not self.student_id.value:
            return

        if not check_student_number(self.student_id.value):
            await interaction.response.send_message("The student ID number you entered is invalid. Please try again.", ephemeral=True)
            return

        # derive email from id
        email = "c" + self.student_id.value[1 : -1]
        verification_code = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        try:
            msg = EmailMessage()
            if smtp_username is None or smtp_password is None:
                raise RuntimeError("SMTP credentials are not configured")
            with smtplib.SMTP(smtp_server, smtp_port) as server:  # type: ignore
                server.starttls()
                server.login(smtp_username, smtp_password)  # type: ignore
                msg['From'] = smtp_from
                msg['To'] = f"{email}@ncl.ac.uk"
                msg['Subject'] = "NUCATS Discord Verification Code"
                msg.set_content(f"Hello {self.name.value},\n\nThank you for starting your verification steps on the NUCATS Discord server.\n\nTo complete your verification, enter the following code in the verification modal in Discord:\n\n{verification_code}\n\nPlease do not share this code with anyone else.\n\nIf you did not request this code, please ignore this email.\n\nThis inbox does accept emails, however replies to this email will be ignored and discarded.\nIf you have any questions, please create a ticket in the server.\n\nKind Regards,\n\nNUCATS Committee.")
                server.send_message(msg)
                print(f"Sent verification email to {email}@ncl.ac.uk")
        except Exception as error:  # noqa: BLE001
            print(f"Error sending email: {error}")
            await interaction.response.send_message("We're very sorry, but we couldn't send you a verification email. Please create a ticket to be verified manually.", ephemeral=True)
            return

        verification_view = VerificationPromptView(verification_code)
        await interaction.response.send_message("We've sent a verification code to your university email. Click the button below to enter it.", ephemeral=True, view=verification_view)


class VerificationModal(Modal):
    verification_code_input = TextInput(
        label="Verification code",
        placeholder="Enter the 8-character code from your university email.",
        required=True,
        min_length=8,
        max_length=8
    )

    def __init__(self, verification_code: str):
        super().__init__(title="Enter your verification code", timeout=300)
        self.verification_code = verification_code

    async def on_submit(self, interaction: discord.Interaction):
        if not self.verification_code_input.value:
            return
        
        if self.verification_code_input.value != self.verification_code:
            await interaction.response.send_message(
                "The verification code you entered is incorrect. Please try again.",
                ephemeral=True,
            )
            return

        role = interaction.guild.get_role(verified_role) # type: ignore
        if not role:
            await interaction.response.send_message(
                "The 'Verified' role does not exist in this server. Please contact a comittee member.",
                ephemeral=True,
            )
            return
        
        await interaction.user.add_roles(role) # type: ignore

        await interaction.response.send_message(
            f"Thank you {interaction.user.mention}! You have been verified. Please check your roles to ensure you have the 'Verified' role.",
            ephemeral=True)
        

class VerificationPromptView(View):
    def __init__(self, verification_code: str):
        super().__init__(timeout=300)
        self.verification_code = verification_code

    @discord.ui.button(label="Enter verification code", style=discord.ButtonStyle.primary)
    async def enter_code(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(VerificationModal(self.verification_code))

class AuthView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify yourself", style=discord.ButtonStyle.primary, custom_id="nucats:auth")
    async def auth_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(AuthModal())