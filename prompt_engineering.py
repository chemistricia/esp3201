from openai import OpenAI
import json

OPENAI_API_KEY = ""
client = OpenAI(
    api_key = OPENAI_API_KEY, # Corrected this line
)
APImodel='gpt-4o'
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
   
#print(words)
#print(solutions)
# dataset = {"words": ["done", "supper", "leverage", "heyday", "milk", "culture", "copy", "up", "use", "through", "city", "sports", "exploit", "yogurt", "over", "hijinks"], "solution": {"groups": [{"words": ["done", "over", "through", "up"], "reason": "finished, as time"}, {"words": ["exploit", "leverage", "milk", "use"], "reason": "take advantage of"}, {"words": ["city", "copy", "culture", "sports"], "reason": "newspaper desks"}, {"words": ["heyday", "hijinks", "supper", "yogurt"], "reason": "words beginning with greetings"}]}}
# words = dataset["words"]
# solutions = dataset["solution"]


it = 3
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
                      +solutions+  
                      "Don't include any explict examples in the prompt, and only include the prompt."
                      ),
        },
    ],
    model=APImodel,) # Verify the correct model name
  
  #print(initial_prompt.choices[0].message.content)
  return initial_prompt.choices[0].message.content

def get_answer(prev_prompt):
  answer = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": (prev_prompt + "\n"
                        "The words given are" + words + ".\n"  # words2 = the whole set
                        "Give the answers to the word problem"),
        },
    ],
    model=APImodel,) # Verify the correct model name
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
    model=APImodel,) # Verify the correct model name
  return new_prompt.choices[0].message.content

def evaluate_answer(answer, solution):      #have some bug, always give "Error in parsing answer or solution. Skipping evaluation"
    try:
        answer_json = json.loads(answer)
        solution_json = json.loads(solution)

        answer_groups = answer_json['groups']
        solution_groups = solution_json['groups']

        exact_match_count = 0
        total_groups = len(solution_groups)
        
        cluster_purity_scores = []

        for answer_group, solution_group in zip(answer_groups, solution_groups):
            answer_words = set(answer_group['words'])
            solution_words = set(solution_group['words'])
            
            # Exact Match Accuracy
            if answer_words == solution_words:
                exact_match_count += 1
            
            # Cluster Purity Calculation
            correct_words = answer_words.intersection(solution_words)
            cluster_purity = len(correct_words) / len(answer_words)
            cluster_purity_scores.append(cluster_purity)

        exact_match_accuracy = (exact_match_count / total_groups) * 100
        average_cluster_purity = (sum(cluster_purity_scores) / total_groups) * 100

        print(f"Exact Match Accuracy: {exact_match_accuracy:.2f}%")
        print(f"Average Cluster Purity: {average_cluster_purity:.2f}%\n")
        
        return exact_match_accuracy, average_cluster_purity

    except json.JSONDecodeError:
        print("Error in parsing answer or solution. Skipping evaluation.\n")
        return 0, 0

def iterative_loop(iterations, check):
  for i in range(iterations):
    if check is False:
      prompt = run_initial_prompt() #gets initial prompt
      print("\n The initial prompt:\n")
      print(prompt)
      answer = get_answer(prompt) #runs initial prompt, get answer
      print("\n The answer from the initial prompt:\n")
      print(answer)
      check = True
    else:
      new_prompt = generate_new_prompt(prompt, response, solution) #gets new prompt
      print(f"\n iteration{i}:The new prompt: \n")
      print(new_prompt)
      answer = get_answer(new_prompt) #runs new prompt, get answer
      print(f"\n iteration{i}:The new answer:\n")
      print(answer)
      exact_match_accuracy, cluster_purity = evaluate_answer(answer, solutions)
      prompt = new_prompt #update previous prompt

iterative_loop(it, check)
