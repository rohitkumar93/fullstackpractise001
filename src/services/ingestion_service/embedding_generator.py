import torch
from transformers import AutoModel, AutoTokenizer

class EmbeddingGenerator:
    """
    Converts text into embeddings using a pre-trained transformer model.
    """

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Loads a pre-trained model and tokenizer for embedding generation.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def generate_embedding(self, text: str):
        """
        Generates an embedding vector from input text.
        """
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            output = self.model(**inputs).last_hidden_state.mean(dim=1)
        return output.squeeze().tolist()  # Convert tensor to list

# Example usage:
if __name__ == "__main__":
    generator = EmbeddingGenerator()
    text = "Artificial Intelligence is transforming industries."
    embedding = generator.generate_embedding(text)
    print("Embedding Vector:", embedding[:5])  # Print first 5 values for preview
