import spacy
nlp = spacy.load('en_core_web_md')

# recommends movie with most similar desciption
def recommend(description):
    model_sentence = nlp(description)
    similarity_max = 0
    count_max = 0
    for count, descriptions in enumerate(movies_list):
        # determines similarity of model to descriptions in movies_list
        similarity = nlp(descriptions[1]).similarity(model_sentence)
        print(descriptions[0], similarity)
        print(descriptions)
        # if similarity is greater than the ones before, set similarity_max to similarity
        if similarity > similarity_max:
            similarity_max = similarity
            count_max = count  # remember the index

    print(f"\nYou should watch {movies_list[count_max][0]}.")


model_sentence = "Will he save their world or destroy it? When the Hulk becomes too dangerous for the Earth, the Illuminati trick Hulk into a shuttle and launch him into space to a planet where the Hulk can live in peace. Unfortunately, Hulk land on the planet Sakaar where he is sold into slavery and trained as a gladiator."

# read from file and append to list
movies_list = []
try:
    with open('movies.txt', 'r') as f:
        for line in f:
            # split into title and description
            line = line.strip()
            line = line.split(" :")
            movies_list.append(line)
    # prints recommendation
    recommend(model_sentence)
except FileNotFoundError:
    print("File could not be found")

# to be honest, I expected the recommendation to be B, the Superman one, so something may have gone wrong