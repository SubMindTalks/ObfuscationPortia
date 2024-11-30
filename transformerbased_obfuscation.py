from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class CodeObfuscator:
    def __init__(self, model_name="Salesforce/codet5-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def obfuscate_code(self, code):
        inputs = self.tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model.generate(inputs.input_ids, max_length=512, num_beams=4, early_stopping=True)
        obfuscated_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return obfuscated_code
