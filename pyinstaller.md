# pyinstaller: http://www.pyinstaller.org/

PyInstaller는, 여러플랫폼에 대해 Python 프로그램을 단일 실행파일로 변환시켜주는 프로그램이다.

# 설치


export LD_LIBRARY_PATH=`locate libpython2.7.so.1.0`


mkdir ~/opt && cd ~/opt
git clone -b develop git://github.com/pyinstaller/pyinstaller.git
cd pyinstaller/bootloader
python ./waf configure build install

# ?
[coding pythong script] -> [analyze script] -> [collect files] -> [put single folder] -> [put single file]

# anlayze script
* 분석가능
 - import구문
 - egg
 - 주요 packages(qt, django등등)

* 분석 불가
 - `__import__()`
 - `sys.path`변경

* 해결
 - PyInstaller에 추가 옵션을 줘야함.
  - file, import path
 - spec수정

myscript.py에 PyInstaller를 적용시키면, myscript/myscript.exe란 실행파일이 생길꺼임.

bundle된 프로그램은 PyInstaller bootloader에서 실행이 시작될꺼임.

* 프로그램을 실행시키면,
 - bootloader가 실행되고,
 - Python interpreter와 같은 임시 Python environment가 만들어지며,
 - import된 myscript폴더에 있는 모든 모듈과 라이브러리를 찾을꺼임.


bundle된 app는 source코드를 포함하고 있지는 않지만,
PyInstaller는 컴파일된 Python script(.pyc)들을 bundle한다.
디컴파일을 막으려면, Cython으로 모듈을 만들어라.

# bootloader
1. bootloader 시작.
 - one-file모드라면, `_MEI`xxxx라는 임시장소에 bundle된 파일을 뽑아낸다.
 - LD_LIBRARY_PATH등 환경 변수를 설정한다.
 - 두 process를 위해, signal핸들을 설정한다.
 - child process를 돌린다.
 - child process가 종료될때까지 기다린다.
 - one-file모드라면, `_MEI`xxxx라는 임시장소를 지운다.
2. child processs로 시작된 bootloader자체
 - Window에선, activate context를 설정함.
 - Python dynamic library로드. (dynamic library의 이름은 실행파일에 내장되어있음)
 - Python 인터프리터 초기화.(PYTHONPATH, PYTHONHOME)
 - python코드 실행.


# spec?
