1. 데이터 수집 파트
-프로그램 실행 전 설정해야할 것
receiver = Receiver()의 parameter로 블루투스를 통해 들어오는 모든 센서데이터들의 이름을 순서대로 지정
ex) receiver = Receiver("IMU_1", "IMU_2",...,"IMU_5", ,"IR_1", "IR_2")
특정 센서의 데이터만 사용하려면 using_sensor = [] 의 대괄호 안에 사용하고자 하는 센서명 입력 ( 위에 입력한 이름과 다른 이름을 입력시 데이터 수집이 이상하게 될 수 있음 )
모으려고 하는 데이터의 패턴을 pattern 값에 저장
receiver를 설정해줄때, parameter로 type="receiver"를 넣어줘야 함. Default값을 실시간 예측모델인 "realtime_classifier"

-프로그램 실행시
현재 들어오고 있는 데이터를 그래프를 통해 실시간으로 볼 수 있음
이 상태에서 '엔터'키를 누르면 현재 보고 있는 그래프의 데이터를 csv 파일로 저장함.
현재 있는 폴더에서 "patterns"라는 하위 폴더를 생성하고 그 안에 각 pattern의 이름으로 하위폴더를 생성한 후 pattern 폴더 속에 순서대로 저장 됨
ESC키를 누르면 데이터 수집이 종료됨
데이터 수집을 종료한 후 우측상단의 stop 버튼을 눌러 프로그램을 종료. ( Threading 종료 방법을 모름... )

주의할것! 

* 엔터키를 누르고 데이터가 저장되는데 약간의 latency가 발생할 수 있으므로 자신의 생각보다 0.1~0.2초 먼저 엔터를 누르면 더 정확하게 데이터를 수집할 수 있음. 
  만약 wide를 큰값으로 설정하면 별 문제가 되지는 않음 (extract.set_extract_option(wide = W) 입력) # W : timestep의 수 = 패턴을 인식하는데 필요하다고 생각하는 데이터의 숫자

* 키가 연속으로 눌리는 것을 방지하기 위해 한번 데이터를 저장하고 1초가 지나고 나야 새로운 데이터가 저장가능
  시간을 조정하고 싶으면 extract.set_extract_option(elapsed_time = T) 입력 # T : 단위 s(초)

* 이후에 동일패턴의 데이터를 추가적으로 수집할 시 extract.set_extract_option(index = N) 입력 # N : 동일패턴의 csv파일 번호 최댓값+1
  옵션을 설정해 주지 않으면 데이터가 덮어써지게 되어 기존에 저장한 데이터가 사라짐

* 새로운 패턴의 데이터를 수집하려고 한다면 extract.set_extract_options(patterns=PATTERN_NAME) 입력 # PATTERN_NAME : 패턴의 이름. string type

# set_extract_options(folder_path=path, pattern_name="pattern", beep_sound=1000, beep_length=300, index=1, elapsed_time=1) - Default 값 상황

2. 데이터 로드 및 모델 학습, 저장 파트
각 패턴데이터가 저장된 폴더의 이름(set_extract_options를 통해 바꾼 이름)을 제외하고 기본설정을 바꾸지 않았다면, 다른 입력값 없이 학습 및 모델 저장까지 자동으로 진행

3. 실시간 예측 및 테스트(by sound)


4. 추가학습
 


 


