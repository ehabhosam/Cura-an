what's going on here till now? 
request is sent with a prompt (a meaning you wanna find). When app starts, it initializes an FAISS (in memory db - vector) instance with the embeddings whole quraan verses. It's pre-encoded already with `multi-qa-mpnet-base-dot-v1` embedding model. When request reaches, the prompt gets encoded with same model and run consine similiarity search thru the indexed in-memory vector db. 

there are changable parameters: 
- the model (but mostly its good as per said at the chatgpt conversation)
- the database (milvus will be the go-to when deploying)
- where to store the actual qura'an
- will the service be accessed directly or can we run multiple instances 
**how about adding a step of {Decision making} that is an LLM choosing the returned output out of search results?**

when adding the gemini layer, and a gaurdrails layer, how much will the backend be able to handle concurrently? 

update::

added gemini to get a psychological meaning first
meaning is then looked up semantically in quraan
resulsts are returned
guardrails is integrated to validate inputs

we adding to launch?
- authentication 
- rate limiting 
- gemini giving multiple answers and semantic search done with all of them with k=1
*OR* just get a meaning out of quraan that is a suitable answer for user problem and perform semantic search with it.
- semantic caching (optional)

#### Bigger idea (more launchable):
Make the semantic search an mcp tool where the user goes in a chatbot flow
where he's talking to his spiritual therapist, that has all the wisdom 
from quraan and he can use it whenever he feels like he aquired the user's 
problem, so user feels a lot better. 

Even this can have a business model where user pay for more chats. 