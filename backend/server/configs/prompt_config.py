

TEMPLATES={
    "llama":"""[INST]
    Use the following pieces ofcontext to answer the question.If no context provided, answer like a AI assistant. 
    
    {context} 
    Question: {question}
    [/INST]
""",
"chatGLM":""" <指令>根据已知信息，简洁和专业的来回答问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题”，
            不允许在答案中添加编造成分，答案请使用中文。 </指令>\n
            <已知信息>{{context}}</已知信息>\n
            <问题>{{question}}</问题>\n
"""

}