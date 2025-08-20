what's going on here till now? 
request is sent with a prompt (a meaning you wanna find). When app starts, it initializes an FAISS (in memory db - vector) instance with the embeddings whole quraan verses. It's pre-encoded already with `multi-qa-mpnet-base-dot-v1` embedding model. When request reaches, the prompt gets encoded with same model and run consine similiarity search thru the indexed in-memory vector db. 
 
there are changable parameters: 
- the model (but mostly its good as per said at the chatgpt conversation)
- the database (milvus will be the go-to when deploying)
- where to store the actual qura'an
- will the service be accessed directly or can we run multiple instances 

when adding the gemini layer, and a gaurdrails layer, how much will the backend be able to handle concurrently?  