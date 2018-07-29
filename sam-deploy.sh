rm -rf ./build
mkdir ./build
cp -p -r ./cloudperception ./build/cloudperception
pip install -r cloudperception/requirements.txt -t ./build

aws cloudformation package --template-file cloudperception/samTemplate.yaml --output-template-file build/template-out.yaml --s3-bucket cloudperception-sam-templates

aws cloudformation deploy --template-file build/template-out.yaml --stack-name sam-dev-$USER --capabilities CAPABILITY_IAM
