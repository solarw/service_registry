# Notes on implementation

## Intro
This will be funny they said, it will be interesting they said...
Actually I got a lot of fun during this task implementation.
Would be nice to get some your comments about it.


## How did I understand the task
For me this tasks looks like: do a service however you decide but it should pass behave
tests defined.
The first moment: I kept `features` unchanged. Let say it's a customer requirement
and I should implement solution right as defined, without changing definitions or some
logic.
The second: I did not applied any optimizations. Just working code as is.
The third: actually no documentation. why? well. nobody will read it. so I prefer to
omit the documentation.


## How to check it works?
there is a docker-compose config so you can install docker-compose and run
`docker-compose up test`
this will call behave tests.


## How to deploy it?
Do you really want to use it?)
if yes:
you can install it as generic python module and use `serviceregistry.py` as start command
or can start with docker-compose by `docker-compose up service`


## And more...
I confused with `Given there is an empty ServiceRegistry` cause other Scenarios assume
there is some data already in service (find, update, delete cases). So actually it
does nothing) If you can describe how it can be implemented better way - please tell
me asap!
