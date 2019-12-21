# Jenkins application (single node)

Deploys an instance of Jenkins to AWS in your region of choice.

## Overview
![Overview](https://github.com/esn89/cfn-jenkins/blob/master/images/highleveldesign.png "Overview")

This deployment will span two availability zones.  Although the diagram doesn't show it, the Application Load Balancer resides in both public subnets.
The NAT Gateway is in the public subnet, and both private subnets have routes to it.  It's main use is to allow the Jenkins instance in the private subnet
to bootstrap itself.

After bootstrapping, it will prompt you for a `initialAdminPassword` which can be found encrypted, in the Systems Manager's Parameter Store under the key "jenkins-init-password".
There is an encrypted Elastic File Store deployed as well with mount points existing in each of the two private subnets.
No SSH is open, as there shouldn't be any need to go inside the instance to set anything up.

## Getting started

You will need [Sceptre](https://github.com/Sceptre/sceptre), a tool to deploy CloudFormation templates.  A virtualenv is highly recommended for this along with Python 3.6+

`virtualenv venv`

`. venv/bin/activate`

`pip install -e ami_resolver`

`pip install -r requirements`

Last but not least, you need to make sure that you have your AWS credentials set in your environment variables.

## Deploying the stacks:

Before the stack is created, we must specify the region you wish to deploy to.
In the main [config file](config/config.yaml), edit the `region` parameter to the one you want.

1. `sceptre create prod/vpc`

   First the networking stack (foundation) needs to be created.

   This will create:
   - VPC
   - internet gateway
   - a NAT gateway
   - elastic IP for the NAT gateway
   - 2 public subnets
   - 2 private subnets
   - public route table
   - private route table


2. `sceptre create prod/iamroles`

   Second comes the IAM Roles and InstanceProfiles as your Jenkins needs access to
   set a parameter in SSM.

   This will create:
   - an IAM Role
   - an Instance Profile


3. `sceptre --var "jenkins_allowed_ip=123.123.123.123/32" create prod/securitygroups`

   Third, is the security groups.  This will create security groups for your Jenkins' instance, EFS, and Elastic Loadbalancer.

   This will create:
   - security group for Jenkins
   - security group for the EFS to allow Jenkins access
   - security group for the load balancer


   The var "jenkins_allowed_ip" is optional.  It denotes the specific IP address, or range to which you want
   your ELB to opened to in terms of access.  I prefer to only open it to the IP address of my home since that
   is where I use my personal Jenkins for my own projects.

   By default, you can choose to not pass it anything, then the value will be `0.0.0.0/0` which open to the world:
   `sceptre create prod/securitygroups`


4. `sceptre create prod/efs`

   Fourth, we need the storage layer, in this case, I have chosen EFS since we would like our Jenkins to span at least 2 availability zones.

   This will create:
   - an elastic file system
   - 1 mount point in one AZ
   - another mount point in the second AZ


5.  `sceptre --var "hostedzonename=your.domain.here" create prod/jenkinsapplication.yaml`

   Finally, the application stack for Jenkins is ready to be deployed.
   You can provide your hosted zone name which you own in the parameter "hostedzonename".
   For example, "user.io".  The stack will create a record for your Jenkins with the record set of: "jenkins.user.io"

   Or you can run this command and fill in your default value for the hosted zone name in the configuration template.
   `sceptre create prod/jenkinsapplication.yaml`

   This includes:

   - Jenkins in an AutoScaling Group of 1
   - launch configuration
   - a load balancer
   - hosted zone
   - record set
   - an SSL certificate managed by Amazon Certificate Manager


## Domain validation:

During the step of creating the Jenkins application stack, CloudFormation will hang, waiting for you to validate the domain/record set.
This project uses "DNS" validation, therefore you should see output simlar to this:

![DNS Validation](https://github.com/esn89/cfn-jenkins/blob/master/images/dnsvalidation.png "DNS Validation")

You will need to go to Route 53, your hosted zone, and in there, create a record set of type "CNAME" with the above parameters.



## Accessing your Jenkins:

Jenkins can then be accessed via a stack output command to retrieve the record set's name, you can paste it in your browser to access.
