# THAI MED BOT
Question-Answering chatbot about initial symptoms

## Inside this file
This chatbot contains some training data, the domain file for NLU dialogue in Rasa Core. In the section of actions folder is the main for deverlop, have some data for work control about medical conversation. The `THAI MED BOT` consists of the following files:
* __actions/actions.py__ contains actions for control QA Medical conversation. 
* __actions/semantic_search.py__ is the semantic search model for use symptoms to tell diseases.
* __data__ contains training data for NLU Dialogue.
* __domain.yml__ contains the domain of the assistant.
* __credentials.yml__ contains credentials for the channels like Meta Messengers.

## How to use
in initial we have `thaitokenizer.txt` file is the manual for install rasa and pythainlp's tokenizer to use (for pythainlp's dependencies we use python3.8 is component)
when you've already installed and followed in the `thaitokenizer.txt`. so do the next step:

1. Train a Rasa model containing the Rasa NLU and Rasa Core models by running:
``` 
rasa train
```

2. Open in the another terminal and open server with Action Server for can use `actions.py` and `semantic_search.py` file
```
rasa run actions
```
3. Now you can chat with my bot in the following command:
```
rasa shell
```

Or if you want to see how Assistant can get slots or how bot can interact each action step use command:
```
rasa interactive
```

for use in the Meta Messengers channel, using the following command (but you have to connect with the webhook and open sever like ngrok to get response before using this, see in the [Documentation](https://pages.github.com/](https://rasa.com/docs/rasa/connectors/facebook-messenger)https://rasa.com/docs/rasa/connectors/facebook-messenger)) :
```
rasa run --credentials credentials.yml
```
