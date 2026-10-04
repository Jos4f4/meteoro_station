"""
Unit tests for the main entry point and asynchronous task scheduling.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.main import main, watchdog_task


@pytest.mark.asyncio
async def test_watchdog_task_feeds_wdt():
    """
    Tests if the watchdog task periodically feeds the hardware timer.
    """
    mock_wdt = MagicMock()

    task = asyncio.create_task(watchdog_task(mock_wdt, interval=0.01))
    await asyncio.sleep(0.05)
    task.cancel()

    assert mock_wdt.feed.call_count >= 1


@pytest.mark.asyncio
@patch("src.main.asyncio.gather", new_callable=AsyncMock)
async def test_main_schedules_all_tasks(mock_gather):
    """
    Ensures that main() correctly schedules the acquisition, watchdog, and server tasks.
    """
    await main()

    assert mock_gather.called

    args, _ = mock_gather.call_args
    assert len(args) == 3

    # Limpeza: cancela as tarefas pendentes para eliminar os alertas do console
    for task in args:
        task.cancel()
