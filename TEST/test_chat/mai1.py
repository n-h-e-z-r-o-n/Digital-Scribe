# Import the transformers library
import transformers

# Set the model name and tokenizer name
model_name = "microsoft/DialoGPT-medium" # You can change this to other pretrained models
tokenizer_name = model_name

# Load the model and tokenizer
model = transformers.AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = transformers.AutoTokenizer.from_pretrained(tokenizer_name)

# Define a function to generate a response given a user input
def generate_response(user_input):
  # Encode the user input and add end of string token
  input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
  # Generate a response using the model
  output_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
  # Decode the output and remove the end of string token
  output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
  # Return the output
  return output

# Start a chat with the bot
print("You: Hi")
print("Bot: " + generate_response("Hi"))
while True:
  # Take user input
  user_input = input("You: ")
  # Generate a response
  response = generate_response(user_input)
  # Print the response
  print("Bot: " + response)
