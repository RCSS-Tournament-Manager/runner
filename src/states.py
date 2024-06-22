import logging
import asyncio

logger = logging.getLogger("state")


class StateManager:
    run_jobs = None

    game_states = [
        "started",
        "fetching_images",
        "running_server",
        "server_started",
        "running_match",
        "match_started",
        "finished",
        "killed",
        "failed",
    ]

    def __init__(self):
        self.run_jobs = {}

    def add_run_job(self, match_id, task, team_left, team_right, data):
        """Add a run job to the state

        Args:
            match_id (str): ID of the match
            task (str): Task to be run
            team_left (str): Left team information
            team_right (str): Right team information
            data (dict): Additional data related to the job
        """
        self.run_jobs[match_id] = {
            "task": task,
            "status": "started",
            "team_left": team_left,
            "team_right": team_right,
            "data": data,
            "states": [],
            "events": {},
            "hooks": {state: [] for state in self.game_states}
        }
        for state in self.game_states:
            event = asyncio.Event()
            self.run_jobs[match_id]["events"][state] = event
        logger.info(f"Added run job for match_id: {match_id}")

    async def kill_run_job(self, match_id):
        """Kill a running job

        Args:
            match_id (str): ID of the match to kill
        """
        if match_id in self.run_jobs:
            self.run_jobs[match_id]["status"] = "killed"
            self.run_jobs[match_id]["states"].append("killed")
            self.run_jobs[match_id]["events"]["killed"].set()
            await self._execute_hooks(match_id, "killed")
            logger.info(f"Killed run job for match_id: {match_id}")
        else:
            logger.error(f"Run job for match_id: {match_id} not found")

    def get_run_jobs_state(self, match_id):
        """Get the state of a running job

        Args:
            match_id (str): ID of the match to get the state for
        
        Returns:
            dict: State of the run job if found, else None
        """
        if match_id in self.run_jobs:
            return self.run_jobs[match_id]
        else:
            logger.error(f"Run job for match_id: {match_id} not found")
            return None

    def get_event(self, match_id, state):
        """Get the event of a specific state for a run match

        Args:
            match_id (str): ID of the match
            state (str): State to get the event for

        Returns:
            asyncio.Event: Event associated with the state if found, else None
        """
        if match_id in self.run_jobs and state in self.run_jobs[match_id]["events"]:
            return self.run_jobs[match_id]["events"][state]
        else:
            logger.error(f"Event for state: {state} in match_id: {match_id} not found")
            return None
        
    async def update_state(self, match_id, new_state):
        """Update the state of a run job

        Args:
            match_id (str): ID of the match
            new_state (str): New state to update to

        Returns:
            bool: True if state updated successfully, else False
        """
        if match_id in self.run_jobs and new_state in self.game_states:
            self.run_jobs[match_id]["status"] = new_state
            self.run_jobs[match_id]["states"].append(new_state)
            self.run_jobs[match_id]["events"][new_state].set()
            await self._execute_hooks(match_id, new_state)
            logger.info(f"Updated state to {new_state} for match_id: {match_id}")
            return True
        else:
            logger.error(f"Failed to update state to {new_state} for match_id: {match_id}")
            return False

    def register_hook(self, match_id, state, hook_fn):
        """Register a hook for a specific state of a run job

        Args:
            match_id (str): ID of the match
            state (str): State to register the hook for
            hook_fn (callable): Function to call when the state is reached
        """
        if match_id in self.run_jobs and state in self.run_jobs[match_id]["hooks"]:
            self.run_jobs[match_id]["hooks"][state].append(hook_fn)
            logger.info(f"Registered hook for state: {state} for match_id: {match_id}")
        else:
            logger.error(f"State: {state} or match_id: {match_id} not found for hook registration")

    async def _execute_hooks(self, match_id, state):
        """Execute hooks for a specific state of a run job

        Args:
            match_id (str): ID of the match
            state (str): State to execute hooks for
        """
        if match_id in self.run_jobs and state in self.run_jobs[match_id]["hooks"]:
            for hook_fn in self.run_jobs[match_id]["hooks"][state]:
                if asyncio.iscoroutinefunction(hook_fn):
                    await hook_fn(match_id)
                else:
                    hook_fn(match_id)
            logger.info(f"Executed hooks for state: {state} for match_id: {match_id}")
        else:
            logger.error(f"State: {state} or match_id: {match_id} not found for hook execution")