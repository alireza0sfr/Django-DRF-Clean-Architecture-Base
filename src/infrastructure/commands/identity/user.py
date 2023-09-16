from application.dtos.identity.user import UserDto
from infrastructure.commands.base import BaseCommand
from infrastructure.handlers.identity.user import UserHandler

class UserCommand(BaseCommand):
    handler = UserHandler
    Dto = UserDto