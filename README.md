Local Predictive Text

This project uses local large language models to allow users to type faster by allowing them to omit longer words inside their sentences.

## Installation

This project uses Python. To run it, first install the necessary packages inside the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

You will also need to have a local language model running. I personally use Ollama. 

## Usage


```bash
python __main__.py
```

Start typing between an exclamation mark followed by an uppercase lett. To end the sentence, you can type period and wait for the LLM to complete the text for you.

Example:

```
!Ths is an exprmntl pjct, pls be ptint.
```

should return 

```
This is an experimental project, please be patient.
```