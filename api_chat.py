import openai
import json

# Set your API key
openai.api_key = "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"

def generate_cfg():
    # Define the prompt for the CFG
    prompt = (
        "Create a Context-Free Grammar (CFG) for arithmetic expressions. "
        "The grammar should include rules for addition, subtraction, multiplication, division, "
        "parentheses, numbers, and identifiers while respecting operator precedence."
    )

    # Call the OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        cfg = response['choices'][0]['message']['content']
        
        # Compare the response with the expected CFG
        example_cfg = """
expr   → expr + term 
       | expr - term 
       | term

term   → term * factor 
       | term / factor 
       | factor

factor → ( expr ) 
       | number 
       | identifier
"""
        # Check if the response matches the example or save as is
        if cfg.strip() == example_cfg.strip():
            print("AI response matches the expected CFG example.")
        else:
            print("AI response differs. Saving response anyway.")

        # Save the prompt and result to a JSON file
        output_data = {
            "prompt": prompt,
            "generated_cfg": cfg
        }
        with open("cfg_output.json", "w") as json_file:
            json.dump(output_data, json_file, indent=4)
        
        print("CFG saved to cfg_output.json!")
    except Exception as e:
        print(f"Error: {e}")

# Run the function
generate_cfg()
