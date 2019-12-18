# Jenkins application (single node)

Deploys an instance of Jenkins to AWS in your region of choice.

## Getting started

You will need Sceptre, a tool to deploy CloudFormation templates.  A virtualenv is highly recommended for this along with Python 3.6+

`virtualenv venv`
`. venv/bin/activate`
`pip install -r requirements`

Last but not least, you need to make sure that you have your AWS credentials set in your environment variables.


## Deploying the stacks:

First the networking stack (foundation) needs to be laid out, this includes a VPC, some gateways, subnets, elastic IPs, routing tables and routes.

`sceptre create prod/vpc.yaml`

Finally, the application stack (Jenkins) is ready to be deployed.  This includes Jenkins in an AutoScaling Group of 1, launch configuration, elastic load balancer, an elastic file system (for a persistent $JENKINS_HOME across restarts and terminations) and some security groups.

Before you running the below command, you must edit the [jenkinsapplication.yaml](config/prod/jenkinsapplication.yaml) file to specify the IP range you wish to grant access to.

On line 17, the variable `JenkinsELBAllowedIP` is where you should specify a CIDR range.

For example: `123.123.123.123/24`.  By default, it is 0.0.0.0/0 which is open to the world.  If you use it as your personal CI/CD or build server, I would pass in my own IP address like so:

`sceptre --var "JenkinsELBAllowedIP=123.123.123.123/32" create prod/jenkinsapplication.yaml` where "123.123.123.123/32" is your own IP address.

`sceptre create prod/jenkinsapplication.yaml`

## Accessing your Jenkins:

Jenkins can then be accessed via a stack output command to retrieve the load balancer's CNAME.  With that, you can paste it in your browser to access.
