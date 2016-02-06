#HW1

HW Description: http://www.comp.nus.edu.sg/~kanmy/courses/3245_2016/hw1-lang.html

To build and test the language models:
$ python build_test_LM.py -b input.train.txt -t input.test.txt -o input.predict.txt

To evaluate the accuracy of the predictions:
$ python eval.py input.predict.txt input.correct.txt
