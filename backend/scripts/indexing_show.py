import pickle

# with open("annoted_best.pickle", "rb") as f:
#     annoted_best = pickle.load(f)

# for i, x in enumerate(annoted_best):
#     x.save(f"annoted/{i:02d}.png")

with open("annoted_best_large.pickle", "rb") as f:
    annoted_best_large = pickle.load(f)

for i, x in enumerate(annoted_best_large):
    x.save(f"annoted_large/{i:02d}.png")
