import voyageai
import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) 

def main():
    w1 = input()
    w2 = input()
    
    vo = voyageai.Client()
    e1 = np.array(vo.embed(w1, model="voyage-3.5", input_type="query").embeddings).reshape(-1)
    e2 = np.array(vo.embed(w2, model="voyage-3.5", input_type="query").embeddings).reshape(-1)

    print(cosine_similarity(e1, e2))

if __name__ == '__main__':
    main()
