import asyncio
from src.states import StateManager
from datetime import datetime
def log(msg):
    print(f'+ {datetime.now().strftime("%H:%M:%S.%f")[:-3]}: {msg}')
    
async def run():
    state_manager = StateManager()
    
    match_id = "123"
    
    log("Adding run job")
    # Add a run job
    state_manager.add_run_job(match_id, "task_1", "Team A", "Team B", {"key": "value"})
    
    # Add a hook to killed state to print test
    def print_test(match_id):
        print(f"Run job for match_id: {match_id} has been killed.")
    
    log("Registering hook")
    state_manager.register_hook(match_id, "killed", print_test)
    
    log("waiting for 10 seconds")
    # Wait 10 seconds
    await asyncio.sleep(10)
    
    log("Updating state to fetching_images")
    # Change state to fetching_images
    await state_manager.update_state(match_id, "fetching_images")
    
    # Print the state
    log(state_manager.get_run_jobs_state(match_id)["status"])
    
    
    log("waiting for 5 seconds  to change state to running_server")
    # Create a task to change the state to running_server after 5 seconds
    async def change_to_running_server():
        await asyncio.sleep(5)
        await state_manager.update_state(match_id, "running_server")
    
    asyncio.create_task(change_to_running_server())
    
    log("waiting for event to change state to running_server")
    # Wait for event to change state to running_server
    event = state_manager.get_event(match_id, "running_server")
    await event.wait()
    
    
    # Print the state
    log(state_manager.get_run_jobs_state(match_id)["status"])
    
    log("kill the run job")
    # Kill the run job
    await state_manager.kill_run_job(match_id)
    
    # Print the state
    log(state_manager.get_run_jobs_state(match_id)["status"])
