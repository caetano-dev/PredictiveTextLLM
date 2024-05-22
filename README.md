# Local Quick Text Editor

MacOS only.

This project uses local LLMs to allow users to edit texts quickly with commands. 

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

Type some text, add a command and select it from start to finish. The command needs to be in between `!` and `.`.
The LLM will generate the text for you and add it to your clipboard automatically.

Example:

```
Today is a... !Complete the sentence.
```

should return 

```
...beautiful day!
```