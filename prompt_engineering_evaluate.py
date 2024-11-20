import json
file_path = "connections_prompts_copy.jsonl"
def load_jsonl(file_path):
    jsondata = []
    with open(file_path, 'r') as file:
        for line in file:
            jsondata.append(json.loads(line))
    return jsondata

dataset = load_jsonl(file_path=file_path)
solutions = []

for data in dataset:
   solutions.append(data['solution']['groups'])
answers =[{'reason': 'illuminating or bright', 'words': ['shine', 'radiate', 'beam', 'glow']}, {'reason': 'livestock animals', 'words': ['horse', 'buffalo', 'sheep', 'goat']}, {'reason': 'negative characteristics', 'words': ['seedy', 'floor', 'envy', 'cutie']}, {'reason': 'secure or store', 'words': ['vault', 'rings', 'excel', 'cow']}, {'reason': 'Charlie Brown characters', 'words': ['charlie', 'lucy', 'woodstock', 'peppermint patty']}, {'reason': 'game of chess', 'words': ['bishop', 'queen', 'gambit', 'mate']}, {'reason': 'pigs', 'words': ['pigpen', 'pig', 'wolf', 'princess']}, {'reason': 'New York references', 'words': ['new york', "rock 'n roll", 'giant', 'witch']}, {'reason': 'wealth or luxury', 'words': ['lavish', 'opulent', 'swank', 'grand']}, {'reason': 'unwell or sick', 'words': ['envious', 'unwell', 'fresh', 'foster']}, {'reason': 'fruits', 'words': ['grape', 'apricot', 'lime', 'fig']}, {'reason': 'naive or innocent', 'words': ['naive', 'berry', 'deluxe', 'stone']}, {'reason': 'Western themes', 'words': ['cowboy', 'drifter', 'lasso', 'sheriff']}, {'reason': 'energetic qualities', 'words': ['spirit', 'bright', 'smart', 'clever']}, {'reason': 'regions or locations', 'words': ['alaska', 'frontier', 'southwest', 'outlaw']}, {'reason': 'names with connotations', 'words': ['mars', 'rogers', 'quick', 'sharp']}, {'reason': 'formal dress', 'words': ['collar', 'cuff', 'tie', 'button']}, {'reason': 'binding or connection', 'words': ['bond', 'link', 'relation', 'pocket']}, {'reason': 'collection or grouping', 'words': ['dozen', 'history', 'laundry', 'martini']}, {'reason': 'small holding service', 'words': ['window', 'bookmark', 'joke', 'tab']}, {'reason': 'spare or extra', 'words': ['spare', 'backup', 'extra', 'copy']}, {'reason': 'container types', 'words': ['mug', 'tote', 'alley', 'pen']}, {'reason': 'sports and recreation', 'words': ['tee', 'ball', 'lane', 'pin']}, {'reason': 'winning or victorious', 'words': ['won', 'ate', 'too', 'for']}, {'reason': 'motor types', 'words': ['car', 'truck', 'bus', 'motorcycle']}, {'reason': 'service providers', 'words': ['chef', 'bartender', 'host', 'server']}, {'reason': 'gloves or mitts', 'words': ['mitt', 'digit', 'beaker', 'dog']}, {'reason': 'animal transportation', 'words': ['piggy', 'scooter', 'gonzo', 'animal']}, {'reason': 'solid or firm', 'words': ['solid', 'tangible', 'firm', 'concrete']}, {'reason': 'desserts', 'words': ['shake', 'split', 'sundae', 'malt']}, {'reason': 'quick movement', 'words': ['dash', 'float', 'hover', 'glass']}, {'reason': 'signs and symbols', 'words': ['signs', 'star', 'key', 'old']}, {'reason': 'sources of water', 'words': ['fountain', 'spring', 'well', 'drop']}, {'reason': 'health and fitness', 'words': ['fit', 'strong', 'sound', 'healthy']}, {'reason': 'seasons or times', 'words': ['fall', 'swift', 'summer', 'sink']}, {'reason': 'small indecent amount', 'words': ['nicks', 'tap', 'keys', 'dip']}, {'reason': 'kitchen tools', 'words': ['peeler', 'whisk', 'ladle', 'grater']}, {'reason': 'types of animals', 'words': ['bird', 'fish', 'mammal', 'reptile']}, {'reason': 'professions', 'words': ['bunker', 'cleaver', 'tanner', 'plumber']}, {'reason': 'small species', 'words': ['princess', 'bird', 'mushroom', 'partridge']}, {'reason': 'coverage', 'words': ['blanket', 'frost', 'veil', 'coat']}, {'reason': 'baking', 'words': ['crust', 'cake', 'tube', 'ring']}, {'reason': 'measurements or weights', 'words': ['gram', 'book', 'sparrow', 'black']}, {'reason': 'found in group', 'words': ['train', 'in', 'bouquet', 'ma']}, {'reason': 'tools', 'words': ['saw', 'hammer', 'wrench', 'level']}, {'reason': 'book characters', 'words': ['charlotte', 'willy', 'babe', 'jerk']}, {'reason': 'sports terms', 'words': ['file', 'yank', 'tug', 'save']}, {'reason': 'music', 'words': ['find', 'print', 'beethoven', 'copy']}, {'reason': 'weekdays', 'words': ['thursday', 'wednesday', 'tuesday', 'saturday']}, {'reason': 'decay or spoil', 'words': ['rot', 'spoil', 'fester', 'sour']}, {'reason': 'changes', 'words': ['turn', 'chance', 'lip', 'lurch']}, {'reason': 'sunday funday', 'words': ['sunday', 'cat', 'friday', 'thing']}, {'reason': 'sound effects or failures', 'words': ['flop', 'dud', 'bomb', 'lemon']}, {'reason': 'snubbing or ignoring', 'words': ['ignore', 'desert', 'jilt', 'jeer']}, {'reason': 'lighthearted taunts', 'words': ['raspberry', 'boo', 'hiss', 'candy']}, {'reason': 'gusts or breaths', 'words': ['gust', 'puff', 'breeze', 'draft']}, {'reason': 'forceful communication or interaction', 'words': ['bite', 'pant', 'kick', 'bore']}, {'reason': 'bite or pinching', 'words': ['tong', 'tang', 'drag', 'yawn']}, {'reason': 'boxing', 'words': ['boxer', 'snooze', 'goggle', 'zip']}, {'reason': 'things to fix or create', 'words': ['fix', 'fabricate', 'fashion', 'forge']}, {'reason': 'friendship or greetings', 'words': ['friend', 'fig', 'food', 'fleabag']}, {'reason': 'fire', 'words': ['firefly', 'fiddle', 'fargo', 'frick']}, {'reason': 'nonsense expressions', 'words': ['frick', 'fiddlesticks', 'fudge', 'fake']}, {'reason': 'home or shelter', 'words': ['net', 'den', 'equal', 'nest']}, {'reason': 'justice or fairness', 'words': ['just', 'fair', 'nothing', 'even']}, {'reason': 'web or digital', 'words': ['web', 'metaverse', 'impossible', 'warren']}, {'reason': 'container type', 'words': ['dish', 'strap', 'hook', 'wire']}, {'reason': 'architecture', 'words': ['crock', 'baloney', 'cup', 'spam']}, {'reason': 'round shapes', 'words': ['saucer', 'bowl', 'plate', 'laser']}, {'reason': 'baloney', 'words': ['scuba', 'tripe', 'bunk', 'radar']}, {'reason': 'musical or rhythmic', 'words': ['bop', 'lounge', 'scrape', 'hide']}, {'reason': 'tied together', 'words': ['bind', 'trifle', 'pickle', 'jam']}, {'reason': 'food styles', 'words': ['banger', 'loaf', 'mash', 'roast']}, {'reason': 'descriptive for being cool', 'words': ['groove', 'scone', 'chill', 'hang']}, {'reason': 'instruments or sound makers', 'words': ['ping', 'bing', 'chime', 'ding']}, {'reason': 'pilot language or fandoms', 'words': ['wing', 'faction', 'sing', 'rat']}, {'reason': 'edge or environment', 'words': ['edge', 'edge', 'corner', 'rim']}, {'reason': 'mobile or moving', 'words': ['word', 'ping', 'camp', 'criminal']}]


def evaluate_answer(answers, solutions):      #have some bug, always give "Error in parsing answer or solution. Skipping evaluation"
    try:
        answer_groups = []
        solution_groups = []
        for answer in answers:
            answer_groups.append(answer['words'])
        
        for solution_set in solutions:
            for solution in solution_set:
                solution_groups.append(solution['words'])
        
        # print(answer_groups)
        # print('\n')
        # print(solution_groups)

        exact_match_count = 0
        total_groups = len(answers)
        
        cluster_purity_scores = []

        for answer_group, solution_group in zip(answer_groups, solution_groups):
            answer_words = set(answer_group)
            solution_words = set(solution_group)
            
            # Exact Match Accuracy
            if answer_words == solution_words:
                exact_match_count += 1
                print(answer_words)
                print(solution_words)
            
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
    
evaluate_answer(answers, solutions)