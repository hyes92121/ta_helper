USERNAME=$1
URL=$2
FOLDER=$3
OUTPUT_DIR=$4

cd $OUTPUT_DIR
mkdir $USERNAME
cd $USERNAME
git init
git remote add -f origin $URL
git config core.sparseCheckout true
echo "$FOLDER/*" >> .git/info/sparse-checkout

git pull origin master
