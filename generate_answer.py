from google.generativeai import GenerativeModel

def generate_answer(query, context_chunks):
    # Join top matching chunks into a single context block
    context = "\n\n".join(context_chunks)

    # Format the final prompt
    final_prompt = f"""Use the following context to answer the question below.

Context:
{context}

Question:
{query}

Answer:"""

    # Define the Gemini model
    model = GenerativeModel("gemini-1.5-flash")

    # Generate answer
    try:
        response = model.generate_content(final_prompt)
        return response.text  # Return only the generated text
    except Exception as e:
        return f"❌ Error generating answer: {e}"
