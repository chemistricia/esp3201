from openai import OpenAI
import json
import random
import time
import csv
import os

OPENAI_API_KEY = ""

client = OpenAI(
    api_key = OPENAI_API_KEY, # Corrected this line
)

file_path = "connections_prompts.jsonl"

SLEEP_TIME = 0.2

class args:
    model: str = "gpt-4o-mini"
    weave_project: str = "connections_refactor"
    file_path: str = "connections_prompts.jsonl"
    max_retries: int = 4
    max_tokens: int = 128
    temperature: float = 0.7
    num_samples: int = 3
    system_prompt: str
    user_prompt: str
    shuffle_words: bool = False
    stuck = 0

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def call_openai(messages, model=args.model, max_tokens=args.max_tokens, temperature=args.temperature):
    # print(messages)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        response_format={ "type": "json_object" }
        )
    extracted = response.choices[0].message.content
    if extracted is None:
        raise ValueError("No response from model")
    return extracted

def generate_solution(messages):
    res = call_openai(messages)
    try:
        generation = json.loads(res)
    except:
        generation = {}
    return generation

def check_one_solution(solution, model_output):
    gen_reason= model_output["reason"]
    gen_words = model_output["words"]
    for sol_dict in solution["groups"]:
        sol_words = sol_dict["words"]
        sol_reason = sol_dict["reason"]
        if set(gen_words) == set(sol_words):
            print(f"{gen_reason} ~ {sol_reason}: {gen_words} == {sol_words}")
            return {"match": 4}
        elif len(set(gen_words).intersection(set(sol_words))) == 3:
            return {"match": 3}
    else: 
        return {"match": 0}

system_prompt = (
    "You are an expert puzzle solver. You understand literature and you are well versed on word play. "
    "I want you to solve a daily word puzzle that finds commonalities between words.\n"
    )

user_prompt = (
    "Here it's the puzzle:\n"
    "- There are 16 words, which form 4 groups of 4 words. Each group has some common theme that links the words.\n"
    "- You must use each of the 16 words, and use each word only once.\n"
    "- Each group of 4 words are linked together in some way. \n"
    "The connection between words can be simple.\n"
    """- An example of a simple connection would be {"reason":'types of fish', "words":["Bass", "Flounder", "Salmon", "Trout"]}. \n"""
    """- Categories can also be more complex, and require abstract or lateral thinking. An example of this type of connection would be {"reason": 'things that start with FIRE', "words": ['Ant', 'Drill', 'Island', 'Opal']}\n"""
    "Be careful of red herrings and make sure all groups of 4 make sense. \n"
    "Provide the one group you are most sure of as your final answer. I will enter this into the puzzle and give you feedback. I will tell you whether it is correct, incorrect or if you got 3 out of 4. "
    "Then we will continue until the puzzle is solved, or you lose.\n"
    """The results should be in JSON format as following: {"reason":"reason why words are grouped", "words":["word1", "word2", "word3", "word4"]}\n"""
)

def create_incorrect_prompt(words: list[str], solution: dict, score: str):
    if score["match"] and args.stuck <= 2:
        args.stuck += 1
        incorrect_prompt = f"This solution is wrong: {solution} " + f"but you got 3/4 words that belong to a category. Try changing one word to get a 4/4. But don't repeat the same previous wrong answers"
    else:
        incorrect_prompt = " "
    incorrect_prompt += (
        "\nDon't repeat any previous wrong solutions. Let's try again. "
        "Let's continue with the rest of the words. "
        f"Here are the remaining {len(words)} words: {words} \n"
        "Guess another group of 4 words. Think outside the box and don't repeat the same previous wrong answer please. "
        "Do not add any additional text to your final answer, just the category name and the 4 words."
    )
    return incorrect_prompt

def create_correct_prompt(words: list[str], solution: dict):
        args.stuck = 0
        if args.shuffle_words:
            random.shuffle(words)
        correct_prompt = (
            f"Great work, {solution} is a correct solution. "
            "Let's continue with the rest of the words. "
            f"Here are the remaining {len(words)} words:\n{words} \n"
            "Guess another group of 4 words. "
            "Do not add any additional text to your final answer, just the category name and the 4 words."
        )
        return correct_prompt

def initial_messages(words):
        return [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt + f"Here are the starting 16 words: {words}\nDo not add any additional text to your final answer, just the group name and the 4 words."
            }
        ]

def predict(words, solution):
        retries = 0
        correct_guesses = []
        remaining_words = [w for w in words]  # listify

        # initial prompt
        messages = initial_messages(words)
        exact_match_count = 0
        while len(remaining_words) > 4 and retries<args.max_retries:
            # generate a solution for the current group
            generation = generate_solution(messages)
            time.sleep(SLEEP_TIME)
            scores = check_one_solution(solution, generation)
            print(f"Current generation {generation} -> score: {scores}")
            time.sleep(SLEEP_TIME)
            if scores["match"] == 4:
                print(" > Great, we have a match")
                exact_match_count += 1
                correct_guesses.append(generation)
                remaining_words = [w for w in remaining_words if w not in generation["words"]]
                user_prompt = create_correct_prompt(remaining_words, generation)
            else:
                print(f" > Not a match, let's try again: retries={retries}")
                user_prompt = create_incorrect_prompt(remaining_words, generation, scores)
                retries+=1
            # we append to the messages list
            messages += [
                {
                    "role": "assistant",
                    "content": str(generation)
                },
                {
                    "role": "user",
                    "content": str(user_prompt)
                }
            ]
        # we have the last group in here!
        if len(remaining_words) == 4: 
            print("We have the last group in here!")
            correct_guesses.append({"reason": "last_group", "words": remaining_words})
            exact_match_count += 1
        return correct_guesses, exact_match_count


def save_group_details_to_csv(group_details, output_path='group_details.csv'):
    """
    Save group details including index, words, solutions, guesses, and accuracy to a CSV file.

    Args:
        group_details (list): A list of dictionaries with 'index', 'words', 'solution', 'guesses', and 'accuracy' keys.
        output_path (str): The path to save the CSV file.
    """
    fieldnames = ['index', 'words', 'solution', 'guesses', 'accuracy']
    with open(output_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in group_details:
            writer.writerow(row)

# Integration with your existing code
sum_exact_match_accuracy = 0
group_details = []

# Assuming `load_jsonl` and `predict` functions are already defined in your code
data = load_jsonl(args.file_path)
for i, entry in enumerate(data):
    words = entry["words"]
    solution = entry["solution"]
    args.stuck = 0

    print(f"\nRunning predict on puzzle {i + 1}...")
    correct_guesses, exact_match_count = predict(words, solution)
    accuracy = exact_match_count / 4
    sum_exact_match_accuracy += accuracy

    # Store group details for CSV
    group_details.append({
        'index': i + 1,
        'words': json.dumps(words),  # Serialize list of words into a JSON-compatible string
        'solution': json.dumps(solution),  # Serialize solution to avoid issues with special characters
        'guesses': json.dumps(correct_guesses),  # Serialize guesses as well
        'accuracy': accuracy
    })

    # Print results for each puzzle
    print(f"Correct guesses for puzzle {i + 1}:", correct_guesses)
    print(f"Exact match accuracy for puzzle {i + 1}:", accuracy)

# Save group details to CSV
save_group_details_to_csv(group_details, 'group_details_stuck.csv')
print("Group details saved to group_details.csv")

print(f"After running on {len(data)} sets of data,")
print(f"Average exact match accuracy:", sum_exact_match_accuracy / len(data))