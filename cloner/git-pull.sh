USERNAME=$1
URL=$2
OUTPUT_DIR=$3

cd $OUTPUT_DIR
mkdir $USERNAME
cd $USERNAME
git init
git remote add -f origin $URL
git config core.sparseCheckout true
echo $OUTPUT >> .git/info/sparse-checkout

git pull origin master