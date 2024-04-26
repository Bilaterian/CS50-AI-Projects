import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages = dict()
    keyLinks = corpus[page]

    if len(keyLinks) > 0:
        for key in corpus:
            pages[key] = (1 - damping_factor) / len(corpus)
        
        for key in corpus[page]:
            pages[key] += damping_factor / len(keyLinks)

    else:
        for key in corpus:
            pages[key] = 1.0 / len(corpus)

    return pages


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = dict()
    for key in corpus:
        pages[key] = 0
    
    page = random.choice(list(corpus.keys()))

    for i in range(1, n):
        current_distribution = transition_model(corpus, page, damping_factor)
        for key in pages:
            pages[key] = ((i - 1) * pages[key] + current_distribution[key]) / i
        
        page = random.choices(list(pages.keys()), list(pages.values()), k = 1)[0]

    return pages


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = dict()
    for key in corpus:
        pages[key] = 1.0 / len(corpus)

    count = 0

    while count != len(corpus):
        count = 0
        for key in corpus:
            rank = (1 - damping_factor) / len(corpus)
            sum = 0
            for page in corpus:
                #how many times a link shows up
                if key in corpus[page]:
                    numLink = len(corpus[page])
                    sum = sum + pages[page] / numLink
            sum = sum * damping_factor
            rank = rank + sum
            if(abs(pages[key] - rank)) < 0.001:
                count = count + 1
            
            pages[key] = rank

    return pages


if __name__ == "__main__":
    main()
