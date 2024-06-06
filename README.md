# runner
The program that runs the games and sends the results to the manager backend.

## Runner model

### MessageBroker
- MessageQueue
- message-handle
- MessageBusId
- ConnectionStatus [Array] [Up, Down, non-responsive]

### RunnerManager - Master
- > Runner [Array]
- link to MessageBroker
- GameHandler
- lastHeartBeat
- > Groups [Array]
- > Match [Array]

### Runner - Slave
- id
- name
- Runnerstatus [running, waiting, stopped]
- tags [Array]
- > RunnerServer

### RunnerServer
- id
- ip
- status [Up, Down, non-responsive]

### Group
- id
- name
- type [group, steplader, ...]
- > Teams [Array]
- > RCSSServerConfig
- stepLadderState 
- status [noStatus, running, ended, stopped]


### Team - S3
- id
- name

### RCSSServerConfig - S3
- id
- name

### Match
- id
- leftTeam > Team
- rightTeam > Team
- > ServerConfig
- > Runner
- > Group
- leftTeamScore
- rightTeamScore
- leftTeamPenaltyScore
- rightTeamPenaltyScore
- status [noStatus,error , inQueue, running, ended, stopped]
- priority
- ScheluedTime [timestamp]
- StartTime [timestamp]
- EndTime [timestamp]
- gameLog > FileUpload - S3
- teamsLog > FileUpload - S3
