#!/usr/bin/env python3
import iterm2, sys

# main command to be executed (NOTE: it will run in fresh iterm session, i.e. - home directory)
main_command = "./monitor_app.sh"

# The commands to run
commands = [main_command + " "  + x for x in sys.argv[1:]]
# dummy_commands = ["one", "two", "three", "four", "five", "six", "seven", "eight"]

async def main(connection):
    app = await iterm2.async_get_app(connection)
    window = app.current_terminal_window

    if window is not None:
        all_panes = []
        # Start a new tab
        tab = await window.async_create_tab()
        left = tab.current_session
        # Split into half
        right = await left.async_split_pane(vertical=True, before=False)
        all_panes.append(left)
        all_panes.append(right)

        # Start splitting on the left side
        pane_to_split = left
        for cmd in commands[2:]:
            newTab = await pane_to_split.async_split_pane(vertical=False, before=False)
            # Next to split is the last pane that was appended to all_panes
            pane_to_split = all_panes[-1]
            all_panes.append(newTab)

        for pane, cmd in zip(all_panes, commands):
            await pane.async_send_text(cmd)

    else:
        print("No current window, please open iterm2 and enable python API in settings")

iterm2.run_until_complete(main)
