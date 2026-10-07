import os
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

TOKEN = os.getenv("CLIENT_TOKEN")

COLORS: Dict[str, str] = {"red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m", "blue": "\033[34m", "default": "\033[37m"}

TICKET_CATEGORY_ID: int = 0  # Replace with your actual ticket category ID

COLOUR_MAIN = 0x43a1e8
COLOUR_NEUTRAL = 0xFCAE1E
COLOUR_GOOD = 0x03C04A

smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT")) # type: ignore
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
smtp_from = os.getenv("SMTP_FROM")

# Ids for server channels and roles
server_id = 1011277165872021504

bot_testing_channel = 1106202485661630565

# Committee
committee_channel = 1378367863630598227
draft_announcements_channel = 1011280318336073748
event_planning_channel = 1011280355887689799
server_updates_channel = 1011283526345293836
bot_log_channel = 1011294949679059015
the_senate_voice_channel = 1011279865808424960
ticket_log_channel = 1154401081237966959

committee_group = [
    committee_channel,
    draft_announcements_channel,
    event_planning_channel,
    server_updates_channel,
    bot_log_channel,
    the_senate_voice_channel,
]

# Information
information_channel = 1047520126620160041
auth_channel = 1550464391156342865
welcome_channel = 1011277166371156059
announcements_channel = 1011277166371156061

# Text Channels
general_channel = 1011277166371156064
advice_channel = 1011279500119646229
memes_channel = 1011281465515974738
suggestions_channel = 1012746964514918410

# Tech
tech_chat_channel = 1011281713885888512
coding_hell_channel = 1011281844387463259
opportunities_channel = 1011281780147499028

# Codewars
codewars_announcements_channel = 1026461371359043644
codewars_chat_channel = 1026461290429943878
codewars_log_channel = 1025810861111124049

codewars_group = [
    codewars_announcements_channel,
    codewars_chat_channel,
    codewars_log_channel,
]

# Gaming
gaming_channel = 1011281140319010848
gaming_suggestions_channel = 1012746853181292605

# Your Stage
stage_1_channel = 1011280576541630585
stage_2_channel = 1011280622695747616
stage_3_channel = 1011280656774483980
placement_channel = 1011280725934342235
masters_and_postgrad_channel = 1011280691847237682

# Voice Channels
luthers_channel = 1011282947246145546
five_swans_voice_channel = 1011277166371156068
quayside_voice_channel = 1011282891151507536
keel_row_voice_channel = 1011277166794788865
mile_castle_voice_channel = 1011277166794788866

# Roles
committee_role = 1011277576230154260
bots_role = 1011283814418497637
verified_role = 1011283236497932318
member_role = 1015604503715786906

stage_1_role = 1011278798995591238
stage_2_role = 1011278845825003602
stage_3_role = 1011278888841777222
stage_4_role = 1011278996291465378
placement_role = 1011279029443244062
postgrad_role = 1011279081263861791
alumni_role = 1011279128445587556

he_him_role = 1012485842691969116
she_her_role = 1012486225745154068
they_them_role = 1012486431421247508

testing_role = 1032271882529021963
northumbria_student_role = 1061275573017641060

#Colour roles