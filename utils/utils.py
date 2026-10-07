import re, random
from discord.ext import commands
from constants import COLORS, committee_role

def color_message(message: str, color: str = COLORS["default"]):
    color = COLORS.get(color, COLORS["default"])
    return color + message + "\033[0m"

def check_student_number(student_number: str) -> bool:
    print(f"Checking student number: {student_number}")
    if len(student_number) != 9:
        return False
    return bool(re.match(r"^\d{9}$", student_number))

def is_committee_member(ctx: commands.Context) -> bool:
    return committee_role in [role.id for role in ctx.author.roles] # type: ignore

def random_status_code() -> int:
        return random.choice([
            100, 101, 102, 200, 201, 202, 203, 204, 206, 207, 300, 301, 302, 303,
            304, 305, 307, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410,
            411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425,
            426, 429, 431, 444, 450, 451, 497, 498, 499,
        ])