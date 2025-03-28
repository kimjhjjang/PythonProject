import argparse

from src.client.data_mocker import *
from src.client import DataMocker

setup_logging('build_dataset')

default_count = 1000

parser = argparse.ArgumentParser(
    prog='스팸 번호 데이터셋 생성기',
    description='랜덤 방식으로 생성된 KISA 스팸 번호 데이터셋',
    epilog='Copyright © 2024 Fourier Softwares. All rights reserved.')

parser.add_argument('-c', '--count', help=f"데이터셋 갯수를 지정합니다. (기본 {default_count}개 데이터)", default=default_count, type=int)

args = parser.parse_args()

total_count = args.count

#data = []
#for index, halt_num_data in enumerate(MessageHub.gen_spam_halt_num_data(total_count)):
#    logging.info('{}/{} DATA GENERATED'.format(index+1, total_count))
#    data.append(halt_num_data)


data = []
for index, halt_num_data in enumerate(DataMocker.gen_spam_halt_num_data(total_count)):
    logging.info('{}/{} DATA GENERATED'.format(index+1, total_count))
    data.append(halt_num_data)


#print(data)
write_list_to_csv('./storage/halt_num_{}.csv'.format(get_current_ymdhm()), data)
