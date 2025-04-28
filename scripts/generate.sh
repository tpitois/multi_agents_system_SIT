config_path="../_config/config.json"
init_path="../_config/init_mosquitoes.csv"
control_path="../_config/control.csv"

config_gen_path="$(realpath generate_config.py)"

generate_control_path="$(realpath generate_control.py)"
main_path="$(realpath $2)"

mkdir ../dataset/$1
cp -r config ../dataset/$1/_config
cd ../dataset/$1

echo TRAIN
mkdir train
cd train

for (( i=1 ; i<=$3 ; i++ ));
do
  echo $i
  mkdir $i
  python3 $generate_control_path $config_path ../_config/control.csv
  python3 $main_path $config_path $init_path $control_path $i
done

cd ..

echo TEST
mkdir test
cd test

for (( i=1 ; i<=$4 ; i++ ));
do
  echo $i
  mkdir $i
  python3 $generate_control_path $config_path ../_config/control.csv
  python3 $main_path $config_path $init_path $control_path $i
done
