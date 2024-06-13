async def run():
    import logging

    # Configure the logger
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger(__name__)

    # Define a custom exception class
    class CustomError(Exception):
        def __init__(self, message):
            self.message = message
            super().__init__(self.message)

    # Function that raises the custom exception
    def check_value(value):
        if value < 0:
            raise CustomError("Value cannot be negative!")
        else:
            print("Value is acceptable.")

    # Example usage
    try:
        check_value(-1)
    except CustomError as e:
        logger.error('Caught an exception', e)