# state_manager.py

import json
import os

from config import STATE_FILE


class StateManager:

    def __init__(self, filepath=STATE_FILE):
        self.filepath = filepath

    def load(self):

        if not os.path.exists(self.filepath):
            return {}

        try:
            with open(
                self.filepath,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read().strip()

                if not content:
                    return {}

                return json.loads(content)

        except (
            json.JSONDecodeError,
            FileNotFoundError
        ):
            return {}

    def save(self, state):

        directory = os.path.dirname(
            self.filepath
        )

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

        with open(
            self.filepath,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                state,
                f,
                indent=4
            )

    def already_processed(
        self,
        username,
        timestamp
    ):

        state = self.load()

        username = username.lower().strip()

        return (
            state.get(username)
            == timestamp
        )

    def mark_processed(
        self,
        username,
        timestamp
    ):

        state = self.load()

        username = username.lower().strip()

        state[username] = timestamp

        self.save(state)
