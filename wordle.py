from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts
import nltk


file = "sample"
data = open(file).read()

tokens = nltk.word_tokenize(data)
#print tokens[:50]

fdist = nltk.FreqDist(tokens)
print fdist.items()[:100]
top_words = [w for w in fdist.keys()[:100] if w.isalpha()]
#print top_words

text = " ".join(top_words)

print get_tag_counts(text)

tags = make_tags(fdist.items()[:100], maxsize=50)
create_tag_image(tags, 'sample_word_cloud.png', size=(900, 600), background=(0, 0, 0))
