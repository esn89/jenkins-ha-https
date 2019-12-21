from sceptre.resolvers import Resolver
from datetime import datetime
from sceptre.exceptions import SceptreException
import boto3.ec2

REGIONS = [
        "us-east-2",
        "us-east-1",
        "us-west-1",
        "us-west-2",
        "ap-east-1",
        "ap-south-1",
        "ap-northeast-3",
        "ap-northeast-2",
        "ap-southeast-1",
        "ap-southeast-2",
        "ap-northeast-1",
        "ca-central-1",
        "eu-central-1",
        "eu-west-1",
        "eu-west-2",
        "eu-west-3",
        "eu-north-1",
        "me-south-1",
        "sa-east-1"
        ]


class Ami_resolver(Resolver):

    def __init__(self, *args, **kwargs):
        super(Ami_resolver, self).__init__(*args, **kwargs)

    def resolve(self):
        """
        resolve is the method called by Sceptre. It should carry out the work
        intended by this resolver. It should return a string to become the
        final value.

        Returns
        -------
        str
            Resolved value
        """
        region = self.argument

        if region not in REGIONS:
            raise SceptreException(f"{region} is not a valid region.")
        client = boto3.client("ec2", region_name=region)

        response = client.describe_images(
                ExecutableUsers=[
                    "all"
                ],
                Filters=[
                    {
                        'Name': 'architecture',
                        'Values': ['x86_64']
                    },
                    {
                        'Name': 'name',
                        'Values': ['amzn2-ami-hvm-2*']
                    },
                ]
            )
        image_date_and_id = []
        for image in response['Images']:
            image_date_and_id.append((image['CreationDate'], image['ImageId']))

        sortedimagesbydate = sorted(
            image_date_and_id,
            key=lambda x: datetime.strptime(
                x[0], "%Y-%m-%dT%H:%M:%S.000Z"))

        # This returns the last item on the list which gives us the latest ami
        return sortedimagesbydate[-1][1]
