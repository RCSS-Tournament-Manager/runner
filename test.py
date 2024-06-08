import os
import asyncio
import sys
import importlib


async def main():
    # get the function name from the argument and call it
    module_name = sys.argv[1]
    module_name = 'test.' + module_name
    
    module = importlib.import_module(module_name)
    
    if hasattr(module, 'run'):
            await module.run()
    else:
        print(f"No function 'test_fn' in module {module_name}")
    

if __name__ == "__main__":
    asyncio.run(main())
