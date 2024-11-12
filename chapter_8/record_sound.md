# prerequisits

Install [Python 3.10](https://www.python.org/downloads/)



# requirements

```python
pip install sounddevice==0.4.6
pip install scipy==1.10.1
```

# spech to text

```sh
$ pip install -U openai-whisper
```


# text to speech

```sh
$ pip install gtts playsound
```

execution time

```sh
$ time python text_to_speech_google_refatored.py

python text_to_speech_google_refatored.py  0.21s user 0.06s system 5% cpu 4.692 total
```

say

```sh
$ time python text_to_speech.py

python text_to_speech.py  0.23s user 0.06s system 10% cpu 2.597 total
```

* interaction with user


```sh
(...)
Epoch 197/200
3/3 [==============================] - 0s 463us/step - loss: 0.1315 - accuracy: 1.0000
Epoch 198/200
3/3 [==============================] - 0s 481us/step - loss: 0.0915 - accuracy: 1.0000
Epoch 199/200
3/3 [==============================] - 0s 481us/step - loss: 0.1208 - accuracy: 1.0000
Epoch 200/200
3/3 [==============================] - 0s 463us/step - loss: 0.0790 - accuracy: 1.0000

2023-05-10 17:07:03,653 Start talking
2023-05-08 17:07:08,774 Write output
2023-05-08 17:07:08,777 Analyze text
2023-05-08 17:07:10,145 Translated text:  Hey speaker!
2023-05-08 17:07:12,673 Start talking
2023-05-08 17:07:17,794 Write output
2023-05-08 17:07:17,797 Analyze text
2023-05-08 17:07:18,333 Translated text:  What time is it?
1/1 [==============================] - 0s 38ms/step
```
