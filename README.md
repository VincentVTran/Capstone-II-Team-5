# Capstone II - Final Project Team 5
The primary problem to be solved by this project is a lack of comprehensive drone tracking coupled with VR integrations. Computer vision has shown to be a powerful tool when integrated with other use cases. Still, all-inclusive computer vision technologies with added drone compatibility have had limited applications thus far. Users not physically present in a space may want to venture into it without going in person. These people do not have great, fully immersive options, let alone a cost-effective solution that allows them to explore a space in virtual reality. Our project aims to solve these problems. Our goal is to end up with a fully autonomous tracking system that can follow a guide through space and transmit the camera data and feature analysis to a user using an Oculus Quest 2 headset. This would allow for better controlled autonomous drone flight for filming, remote viewing of places, and providing more immersive digital tours. The approach designed to accomplish this is to program a Parrot AR.Drone 2.0 to remotely communicate with a host computer, which will analyze the video content, provide real-time feature analysis, and stream the video feedback to the Oculus.

## Contributors
#### Computer Vision Team
* [**Vincent Tran**](https://github.com/VincentVTran)
* [**Sam Lefforge**](https://github.com/slefforge)
#### Drone Motor Control Team
* [**Eli Helf**](https://github.com/EliAHelf)
* [**Natalie Friede**](https://github.com/NatalieTheGreatest)
#### VR Team
* [**Jan Bobda**](https://github.com/JBobda)

## Contents
1. [Environment Setup](#environment-setup)
2. [Demo](#demo)

## Environment setup

- Clone the repository
```
git clone https://github.com/VincentVTran/Capstone-II-Team5.git capstone && cd capstone
export capstone=$PWD
```
- Setup python environment.
- This project uses conda package manager. For details on how to install conda
visit https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html 
- If you're on Windows, make sure to use Anaconda Prompt instead of your default terminal.

```
conda create -n capstone python=3.10
conda activate capstone
pip install -r requirements.txt
```
## Demo
- [Setup](#environment-setup) your environment
- [To run automated drone navigation] Run `src/auto.py`
```
cd $capstone
python ./src/auto.py
```

- [To run automated drone navigation with a recorded demo] Run `src/auto-demo.py`
```
cd $capstone
python ./src/auto-demo.py
```

- [To run manual drone navigation] Run `src/manual.py`
```
cd $capstone
python ./src/manual.py
```

- [To test cv model locally with webcam] Run `src/webcam_cv_test.py`
```
cd $capstone
python ./src/webcam_cv_test.py
```

- [To test cv model locally with webcam and printed drone instructions] Run `src/print_movements.py`
```
cd $capstone
python ./src/print_movements.py
```

