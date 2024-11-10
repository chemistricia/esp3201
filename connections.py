from openai import OpenAI
import json

OPENAI_API_KEY = ''

client = OpenAI(
    api_key = OPENAI_API_KEY, # Corrected this line
)

file_path = "connections_prompts_copy.jsonl"

def load_jsonl(file_path):
    jsondata = []
    with open(file_path, 'r') as file:
        for line in file:
            jsondata.append(json.loads(line))
    return jsondata

dataset = load_jsonl(file_path=file_path)
words = ''
solutions = ''
for data in dataset:
   words += str(data['words']) + "\n"
   solutions += str (data['solution']) + "\n"
   
print(words)
print(solutions)
# dataset = {"words": ["done", "supper", "leverage", "heyday", "milk", "culture", "copy", "up", "use", "through", "city", "sports", "exploit", "yogurt", "over", "hijinks"], "solution": {"groups": [{"words": ["done", "over", "through", "up"], "reason": "finished, as time"}, {"words": ["exploit", "leverage", "milk", "use"], "reason": "take advantage of"}, {"words": ["city", "copy", "culture", "sports"], "reason": "newspaper desks"}, {"words": ["heyday", "hijinks", "supper", "yogurt"], "reason": "words beginning with greetings"}]}}
# words = dataset["words"]
# solutions = dataset["solution"]


it = 10
check = False
prompt = ""
response = ""
solution = ""
def run_initial_prompt():
  initial_prompt = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": ("Imagine you are a prompt engineer trying to come up with prompts to solve this word puzzle.\n"
                        "The instructions of the word game are:\n"
                        "The word puzzle finds commonalities between words.\n"
                        "There are 16 words, which form 4 groups of 4 words. Each group has some common theme that links the words.\n"
                        "You must use each of the 16 words, and use each word only once.\n"
                        'You will be given a set of 16 words in a list, eg. ["word1", "word2", "word3", "word4"..."word16"]\n'
                        "The results from running the prompt should be in JSON format as follows:"
                        '{"reason": "reason why words are grouped", "words": ["word1", "word2", "word3", "word4"]}\n'
                        "As a prompt engineer, come up with a prompt to accurately solve this daily word puzzle.\n"
                        "Here are some examples, create a prompt such that when given the list of words, it is able to generate the solutions:"
                        +words+
                        "Don't include any explict examples in the prompt, and only include the prompt."
                        ),
        },
    ],
    model="gpt-4o",) # Verify the correct model name
  
  print(initial_prompt.choices[0].message.content)
  return initial_prompt.choices[0].message.content

def get_answer(prev_prompt):
  answer = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": (prev_prompt + "\n"
                        "The words given are" + words + ".\n"
                        "Give the answers to the word problem"),
        },
    ],
    model="gpt-4o",) # Verify the correct model name
  return answer.choices[0].message.content

def generate_new_prompt(prev_prompt, response, solution):
  new_prompt = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": ("Imagine you are a prompt engineer trying to come up with prompts to solve this word puzzle.\n"
                        "The previous prompt you generated to solve the word problem was " + prev_prompt + ".\n"
                        "The sets of words given are:\n"
                        +words+
                        "The answer from running the prompt was " + response + ".\n"
                        "However, the actual solution is " + solutions + ".\n"
                        "Learn from your mistakes and return only the next improved prompt so it can accurately classify other datasets.\n"
                        "Keep the format of the answers."),
        },
    ],
    model="gpt-4o",) # Verify the correct model name
  return new_prompt.choices[0].message.content

def iterative_loop(iterations, check):
  for i in range(iterations):
    if check is False:
      prompt = run_initial_prompt() #gets initial prompt
      print(prompt)
      answer = get_answer(prompt) #runs initial prompt, get answer
      print(answer)
      check = True
    else:
      new_prompt = generate_new_prompt(prompt, response, solution) #gets new prompt
      print(new_prompt)
      answer = get_answer(new_prompt) #runs new prompt, get answer
      print(answer)
      prompt = new_prompt #update previous prompt

iterative_loop(it, check)
