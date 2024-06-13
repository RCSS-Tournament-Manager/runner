
```
message format :
{
    "command": "start_match",
    "body": {
        "match_id": "1234",
        
        "team_right": {
            "_type": "docker",
            "_config" :{
                
            },
            "image_name": "teamA",
            "tag": "latest",
            "team_name": "teamA",
            "config": {
                core_start: 0,
                core_end: 11,
            }
        },
        
        "team_left": {
            "_type": "docker",
            "_config" :{
                
            },
            "image_name": "teamB",
            "tag": "latest",
            "team_name": "teamB",
            "config": {
                core_start: 0,
                core_end: 11,
            }
        },
        
        
        "rcssserver": {
            "_type": "docker",
            "image_name": "teamB",
            "tag": "latest",
            "config": {
                core_start: 0,
                core_end: 11,
            },
            "rcssserver_config": {
                ...
            },
            
        },
        
        
        
        "log": {
            "level": "info",
            
            "s3":{
                "config": {
                    "type": "minio",
                    "endpoint": "http://minio:9000",
                    "access_key": "access_key",
                    "secret_key": "secret_key",
                    "bucket": "bucket",
                },
                "right_team_log" : true,
                "left_team_log" : true,
                "server_log" : true,
                "rcg" : true,
                "rcl" : true,
            },
            
            "stream": {
                "config": {
                    "type": "rabbitmq",
                    "host": "rabbitmq",
                    "port": 5672,
                    "username": "username",
                    "password": "password",
                    "exchange": "exchange",
                    "queue": "queue",                    
                },
                "right_team_log" : true or {
                    "queue": "queue",    
                },
                "left_team_log" : {
                    "type": "rabbitmq",
                    "host": "rabbitmq",
                    "port": 5672,
                    "queue": "queue",
                }
                "server_log" : true,
                "rcg" : true,
                "rcl" : true,
                "score" : true,
            }
        }
        
        
        
    }
}
```