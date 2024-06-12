from src.storage import MinioClient
from src.docker import Docker
from src.rabbitmq import RabbitMQ
from src.logger import get_logger
import copy

logger = get_logger(__name__)

def initialize_clients(data: dict, **kwargs):
    errors = []
    # deep clone 
    out = copy.deepcopy(data)
    client_types = {
        "minio": {
            "class": MinioClient,
            "default": kwargs.get("storage")
        },
        "docker": {
            "class": Docker,
            "default": kwargs.get("docker")
        },
        "rabbitmq": {
            "class": RabbitMQ,
            "default": kwargs.get("rabbitmq")
        }
    }
    
    def initialize_recursively(obj):
        if isinstance(obj, list):
            logger.debug("Processing a list")
            for i in range(len(obj)):
                obj[i] = initialize_recursively(obj[i])
                
        elif isinstance(obj, dict):
            if '_type' in obj:
                logger.debug(f"Found _type: {obj['_type']}")
                if obj['_type'] not in client_types:
                    error_msg = f"Invalid client type: {obj['_type']}"
                    logger.debug(error_msg)
                    errors.append(error_msg)
                elif "_config" not in obj or  obj['_config'] == 'default':
                    logger.debug(f"Using default client for type: {obj['_type']}")
                    obj['_client'] = client_types[obj['_type']]['default']
                else:
                    client_info = client_types[obj['_type']]
                    client_class = client_info['class']
                    config = obj.get('_config', None)
                    if config is not None:
                        try:
                            logger.debug(f"Initializing client for type: {obj['_type']} with config")
                            obj['_client'] = client_class(**config)
                        except Exception as e:
                            error_msg = f"Error initializing client for type [{obj['_type']}]: {e}"
                            obj['_client'] = client_info['default']
                            logger.debug(error_msg)
                            errors.append(error_msg)
                    else:
                        logger.debug(f"Using default client for type: {obj['_type']}")
                        obj['_client'] = client_info['default']
            for key, value in obj.items():
                if isinstance(value, dict):
                    obj[key] = initialize_recursively(value)
                elif isinstance(value, list):
                    for i in range(len(value)):
                        obj[key][i] = initialize_recursively(value[i])

        return obj
    # Start the recursion from the top level of the data structure
    logger.debug("Starting client initialization")
    out = initialize_recursively(out)
    logger.debug("Client initialization complete")
    
    if errors:
        logger.debug(f"Errors encountered during initialization: {errors}")
        
    return out, errors