#!/bin/sh

DATA_PATH_ROOT="data"
DATA_PATH_SMALL=$DATA_PATH_ROOT/small
DATA_PATH_BIG=$DATA_PATH_ROOT/big
DATA_URL_SMALL="https://drive.google.com/uc?export=download&id=1Cm_zOflSJ8v6DmqoFHl_YaA_yL5pMZCC"
DATA_URL_BIG="https://drive.google.com/uc?export=download&id=1nb1PiP0FOEng8BxY4CdfOA2SSGVX2O6j&confirm=t&uuid=7812b97d-821a-41c8-a90f-c02df72bd55e"
DATA_ARCHIVE_NAME_SMALL="small_test_data.zip"
DATA_ARCHIVE_NAME_BIG="big_test_case.zip"

# Download small data set
mkdir -p $DATA_PATH_SMALL
if [ ! -f "$DATA_PATH_SMALL/input.bin" ]; then
    wget -O $DATA_PATH_SMALL/$DATA_ARCHIVE_NAME_SMALL $DATA_URL_SMALL
    unzip -d $DATA_PATH_SMALL $DATA_PATH_SMALL/$DATA_ARCHIVE_NAME_SMALL
    rm $DATA_PATH_SMALL/$DATA_ARCHIVE_NAME_SMALL
fi

# Download big data set
mkdir -p $DATA_PATH_BIG
if [ ! -f "$DATA_PATH_BIG/input.bin" ]; then
    wget -O $DATA_PATH_BIG/$DATA_ARCHIVE_NAME_BIG $DATA_URL_BIG
    unzip -d $DATA_PATH_BIG $DATA_PATH_BIG/$DATA_ARCHIVE_NAME_BIG
    rm $DATA_PATH_BIG/$DATA_ARCHIVE_NAME_BIG
fi