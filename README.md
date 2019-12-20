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

This will create:
- VPC
- internet gateway
- a NAT gateway
- elastic IP for the NAT gateway
- 2 public subnets
- 2 private subnets
- public route table
- private route table

`sceptre create prod/vpc`

Second comes the IAM Roles and InstanceProfiles as your Jenkins needs access to
set a parameter in SSM.

This will create:
- an IAM Role
- an Instance Profile

`sceptre create prod/iamroles`

Third, is the security groups.  This will create security groups for your Jenkins' instance, EFS, and Elastic Loadbalancer.

This will create:
- security group for Jenkins
- security group for the EFS to allow Jenkins access
- security group for the load balancer

`sceptre --var "jenkins_allowed_ip=123.123.123.123/32" create prod/securitygroups`

The var "jenkins_allowed_ip" is optional.  It denotes the specific IP address, or range to which you want
your ELB to opened to in terms of access.  I prefer to only open it to the IP address of my home since that
is where I use my personal Jenkins for my own projects.

By default, if you do not pass it anything, it is `0.0.0.0/0` which open to the world.

`sceptre create prod/securitygroups`

Fourth, we need the storage layer, in this case, I have chosen EFS since we would like our Jenkins to span at least 2 availability zones.

`sceptre create prod/efs`

Finally, the application stack for Jenkins is ready to be deployed.  This includes:

- Jenkins in an AutoScaling Group of 1
- launch configuration
- a load balancer
- hosted zone
- record set
- an SSL certificate managed by Amazon Certificate Manager

You can provide your hosted zone name which you own in the parameter "hostedzonename".
For example, "user.io".  The stack will create a record for your Jenkins with the record set of: "jenkins.user.io"
`sceptre --var "hostedzonename=your.domain.here" create prod/jenkinsapplication.yaml`

Or you can run this command and fill in your default value for the hosted zone name in the configuration template.
`sceptre create prod/jenkinsapplication.yaml`


## Accessing your Jenkins:

Jenkins can then be accessed via a stack output command to retrieve the record set's name, you can paste it in your browser to access.
