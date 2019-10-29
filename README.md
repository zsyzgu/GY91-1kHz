# Ring Text Entry

A word-level text entry using an IMUring worn on the middle phalanx of the index finger.

## Prerequisites

You need a IMU ring, which is an accelerometer GY-91 attached to a regular finger ring. The ring is connected to an Arduino Uno R3 with Dupont lines. The ring collects 6-axis motion data including acceleration and angular velocity. The raw acceleration data is fused with gravity. We use Madgwick Filter to split the raw acceleration into true acceleration and gravity.

Hardware platform:

1. Arduino Uno R3

2. GY91 (including MPU9250)

3. Ring

Software environment:

1. python 2.7.15

2. numpy, pygame, keyboard and some other dependencies

## Running

### Arduino

You should connect GY-91 to Arduino as below.

```
NCS - 5V
SDO/SAO - Ground
SDA - A5
SCL - A4
```

Then you can compile the code in **./arduino/** and upload it to the arduino with arduino IDE.

### Typing

You can run **./main.py** with python 2.7.15 like this.

```
python main.py your_name session_number
```

Then there will be a keyboard on your displayer and you can touch your desk wearing the ring. The program will detect the contact and give out its prediction. You can press your index finger on the desk for seconds to enter the selection mode. In this mode, you can slide your finger left or right to select the word you want to input and lift up. If you make a mistake, you can use left slide to delete the last thing you input.

When you input a sentence, you can press 'Y' on your physical keyboard to type the next sentence. Besides, you can press 'N' to re-type the sentence. The program will end when you enter 10 sentences.

### Training

You can run **./person_model.py** like this.

```
python person_model.py your_name
```

It will generate your personal touch model.

You can run **./person_simulation.py** to find out the advantage of personal touch model.

```
python person_simulation.py your_name
```

To use your personal touch model instead of general model, you can change line 13 in **./main.py**

```
entry = entry.Entry(5000, entry.LanguageModel.USE_TRIGRAMS)
```

to

```
entry = entry.Entry(5000, entry.LanguageModel.USE_TRIGRAMS, person='your_name')
```

In this way, you can type with your personal touch model.

The first param of Entry class is the dictonary size of language model. What is more, the Entry class supports Unigram, Bigram and Trigram. You can change the second param to use different language model.

### Analysis

To find how fast you have typed, you can run **./analze_main.py**.

```
python analyze_main.py your_name session_number
```

It will print the analysis in terminal with WPM, CER and UER.

## File Introduction

```
./arduino/ : arduino code that transmit IMU data from GY-91 with 1kHz
./analyze_main.py : analyze typing data and calculate WPM, CER and UER
./analyze_model.py : analyze Exp2 data and train general touch model
./contact.py : detect contact event using IMU data
./corpus.txt : corpus used by language model
./entry.py : QWERTY entry using touch model and language model
./event.py : detect touch event
./log.py : log data during experiment
./madgwickahrs.py : madgwickahrs algorithm to remove gravity in IMU data
./main.py : main typing program
./oscilloscope.py : drawing data
./panel.py : typing entry UI
./person_model.py : train personal touch model
./person_simulation.py : simulate typing progress and analyze predict ranking
./phrases-main.txt : phrases used in main.py
./phrases.txt : phrases used in Exp2
./prompt.mp3 : video that implies typing used in Exp2
./quaternion.py : implement basic quaternion arithmetic
./read_serial.py : read IMU data from serial
./sample-contact.py : collect contact data to train contact model
./sample-model.py : collect typing data to train touch model
./simulation.py : simulate Exp2 progress to analyze touch model and language model
./train.py : train contact model
./utils.py : tool code to get users' name
```