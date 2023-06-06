from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
import csv


llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name='gpt-3.5-turbo')
master_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<Analysis>'


# Import File

file_name = ''

file = open("", "r")
raw_data = list(csv.reader(file, delimiter=","))
file.close()

print("First Conversation ID: " + raw_data[0][0])
print("Last Conversation ID: " + raw_data[len(raw_data)-1][0])
print("Conversation Count: " + str(len(raw_data)-1

# Define Task
                                   
task = """ 

<Conversation>
  <Conversation_id> What is the Conversation ID? 
  <Intent> What is the Intent of the conversation? [Purchase Watch, Upgrade, Payg Offers, Add Airpods, End Contract, Bolt Ons, Add Line, Unknown, Join O2, My O2, Sim Card, Refund, Billing, Stock Enquiry, network Issue]
  <Sub_Intent> What is the Sub Intent?
  <Sale_Made> Was a sale made?
  <Reason_for_No_Sale> Why do you think a sale was made?
  <Product_or_Device> What product or device is the customer discussing?
  <Information_Asked> Summarise the information the agent asked for?
  <Query_Resolved> Was the customer query resolved?
  <Reason_for_Unresolved> Why do you think the sale was resolved?
  <Agent_Summary> Summarise what the agent did in this conversation?
</Conversation>

"""
                                   

for x in range(len(raw_data)):
  print("Executing: " + str(x + 1) + " of " + str(len(raw_data)-1) + " : " + str(round(((x)/len(raw_data))*100)) +"% Complete ")
  transcript = "Conversation ID: " + raw_data[x][0] + "\n" + raw_data[x][1]
  template = """
  % INSTRUCTIONS
   - You are an AI Bot that is very good at analysing conversation transcripts
   - Your goal is to find relevant information from the transcript
   - Do not go outside the transcript provided
   - Output in an xml format with the questions as the headers. Do not Output [<?xml version="1.0" encoding="UTF-8"?>]. Do not output a Root Node

  % Transcript for Analysis:
  {transcript}

  % YOUR TASK
  {task}

  """

                            
  prompt = PromptTemplate(
      input_variables=["transcript","task"],
      template=template,
  )

  final_prompt = prompt.format(transcript=transcript,task=task)
  
  try:
    data = llm.predict(final_prompt)
    master_xml = master_xml + '\n' + data
  except:
    print("Error From Open AI - Token Count too high")


# Output as XML

master_xml = master_xml + '\n</Analysis>'

print(master_xml)

text_file = open("Output_Master.xml", "w")

text_file.write(master_xml)

text_file.close()                                     
                                   
                                   
