import time

from bot.core.constants import ALT_VK, PADDING_IN_S, TAB_VK
from bot.core.worker import WorkerSignals
from bot.models import (
    Command,
    Keystroke,
    ModifierKey,
    Params,
    SleepCommand,
    SleepRandomCommand,
)
from bot.utils.logger import logger

alt_tab = Keystroke(key="Tab", vk=TAB_VK, modifier=ModifierKey(key="Alt", vk=ALT_VK))


def _build_command_list(params: Params) -> list[Command]:
    sleep = SleepRandomCommand(interval_range=params.interval_range)
    commands: list[Command] = [SleepCommand(milliseconds=PADDING_IN_S * 1000)]
    for _ in range(params.winNum):
        for cmd in params.commands:
            commands.extend([cmd, sleep])
        commands.append(alt_tab)
    return commands


def run(params: Params, signals: WorkerSignals) -> None:
    logger.info(f"Running with params:\n{params}")
    commands = _build_command_list(params)
    cmd_indices = {id(cmd): i for i, cmd in enumerate(params.commands)}
    end = time.time() + params.limit * 60

    while time.time() < end:
        for cmd in commands:
            params_idx = cmd_indices.get(id(cmd))
            if params_idx is not None and cmd.is_reportable:
                signals.current_command.emit(params_idx)
            try:
                logger.debug(f"Executing {cmd}")
                cmd.execute()
            except TypeError:
                logger.error(f"Command {cmd!r} not handled skipping")
