import lamini
lamini.api_key = "0cfda3d014bb341b4028278c035b2a8d9eb17475e3d4ae94712d310c541b696a"


llm = lamini.Lamini(
    model_name="meta-llama/Llama-2-7b-hf",
)
response = llm.generate("Tell me how to train my dog to sit.")


#print(response['output'] if isinstance(response, dict) else response)

#if isinstance(response, dict):
#    print('dictionary output - {}'.format(response['output']))
#else:
#    print('non dictionary output - {}'.format(response))



print('non dictionary output - {}'.format(response))