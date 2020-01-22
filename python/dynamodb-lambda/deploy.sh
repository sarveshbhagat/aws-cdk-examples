#!/bin/bash
#  (c) 2019 Amazon Web Services, Inc. All Rights Reserved.
#  This AWS Content is subject to the terms of the Basic Ordering Agreement Contract No.
#  [2018-17120800001/Order No. BOA001.


now=$(date +"%T")
echo "Deployment Start time : $now"
echo "Installing dependencies"
#sudo npm install -g aws-cdk
#sudo npm install -g npm
echo "step up cdk environment"
source .env/bin/activate
pip install -r requirements.txt

cdk bootstrap
cdk ls

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Deploy stacks
echo "Delpoy producer"
cdk deploy producer --require-approval never

echo "Delpoy consumer"
cdk deploy consumer --require-approval never


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
now=$(date +"%T")
echo "Deployment Finsih Time : $now"




