import streamlit as st
import pandas as pd
import json
from io import StringIO


st.title('Bot Extractor - JSON')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #string_data = stringio.read()
    #string_data.seek(0)
    data = json.load(stringio)
    #st.write(data)

    
    # Bot Extraction Script
    
    
    # Future Additions?
    
    # Responders (Integrations)
    #print('Responders \n')
    #for i in data['responder']:
    #    print(i)
    
    # Menus - (Unsure usage)
    #print('\n\n Menus \n')
    #for i in data['menus']:
    #    print(i)
    
    
    
    # Groups - (Dialogs)
    
    groupDict = {}
    #print('\n\n Groups \n')
    for i in data['groups']:
      # Get name / id / type / status
      groupDict[i['id']] = i['name']
      #print(i)
      #print(i['name'] + '/' + i['id'] + '/' + i['dialogType'] + '/' + i['status'])
    
    #print(groupDict)
    
    
    # Conversation Messages - (Engagements)
    #Message Dictionary
    messDict = {}
    for i in data['conversationMessage']:
      messDict[i['id']] = i['name']
    #print(messDict)

    
    # Associated Intents - NEW 
    #Intent Dictionary
    intentDict = {}
    try:
        for i in data['associatedIntents']:
          intentDict[i['id']] = i['name']
    except:
        intentDict = {}
        #print('No Associated intents')
      #print(i)
    #print(intentDict)



    
    
    
    # Initialize Data Table for Messages
    
    table = []
    
    # Populate Unsorted Messages Table
    
    #print('\n\n Conversation Messages \n')
    for i in data['conversationMessage']:
      row = []
      #print('\n')
      #print(i)
      # Group (Dialog) / Previous Message / Name / Next Message
      #print('Dialog: ' + groupDict[i['group']])
      dialog_name = groupDict[i['group']]
      row.append(dialog_name) #<--------
      #print('Name: ' + i['name'])
      engagement_name = i['name']
      row.append(engagement_name) #<--------
    
    
      try:
        #print('Prev Engagement: ' + messDict[i['prevMessageId']])
        prev_message = messDict[i['prevMessageId']]
      except:
        #print('No Prev Engagement')
        prev_message = 'No Prev Engagement'
        
      row.append(prev_message) #<--------
    
    
      # NEXT MESSAGE APPENDED LATER
    
      try:
        #print('Next Message: ' + messDict[i['nextMessageId']])
        next_message = messDict[i['nextMessageId']]
      except:
        #print('No Next Message')
        next_message = 'No Next Engagement'
    
    
    
    
      #print('\n')
    
      # Content sub level
      #print(i['content'])
    
      content = i['content']
    
      try:
        results = content['results']
      except:
        results = []
        #print('No Results')
    
      if results:
        #print('Results: ')
        #print(results)
        #print('Type: ' + results['type']) 
        engagement_type = results['type']
        row.append(engagement_type) #<-------- Engagement Type
    
        text = 'Blank' # reset text

          
        # DIALOG_STARTER ENGAGEMENT
        if results['type'] == 'DIALOG_STARTER':
          pattern = ''
    
          try:
            patternList = i['pattern']
            for each in patternList:
              pattern = pattern + " " + each
          except:
            pattern = 'No Pattern'
          try:
            intentId = i['intentId']
          except:
            intentId = 'No Intent'
          try:
            intentName = intentDict[intentId]
          except:
            intentName = 'No Intent'
          text = "Pattern: " + pattern + "\nIntent: " + intentName

          
        # TEXT ENGAGEMENT
        if results['type'] == 'TEXT':
          tile = results['tile']
          #print('Tile: ')
          #print(tile)
          tileData = tile['tileData']
          try:
            text = tileData[0]['text']
          except:
            text = 'Blank'
          #print('Engagement Text: ' + text)
    
    
        # TEXT_QUESTION ENGAGEMENT
        if results['type'] == 'TEXT_QUESTION':
    
          tile = results['tile']
          #print('Tile: ')
          #print(tile)
          tileData = tile['tileData']
          try:
            text = tileData[0]['text']
          except:
            text = 'Blank'
          #print('Engagement Text: ' + text)


          
        ####### BUTTONS SECTION
        buttons = ''

        # MULTIPLE CHOICE QUESTION ENGAGEMENT
        if results['type'] == 'MULTIPLE_CHOICE_QUESTION':
    
          tile = results['tile']
          tileData = tile['tileData']
          try:
            text = tileData[0]['text']
          except:
            text = 'Blank'
          #print('Engagement Text: ' + text)
          try:
            mcq_buttons = tileData[0]['multipleChoice']['multipleChoices']
            buttons = str(mcq_buttons)
          except:
            buttons = 'Blank'

          
         # QUICK REPLY ENGAGEMENT
        if results['type'] == 'QUICK_REPLY':
    
          tile = results['tile']
          tileData = tile['tileData']
    
          try:
            text = tileData[0]['text']
          except:
            text = 'Blank'
          try:
            qr_buttons = content = i['quickReplies']
    
            qr_list = []
            for each in qr_buttons:
              qr_list.append(each['title'])
          
            buttons = str(qr_list)
          except:
            buttons = 'Blank'


        # BUTTON ENGAGEMENT 
        if results['type'] == 'BUTTON':
    
          tile = results['tile']
          tileData = tile['tileData']
    
          try:
            text = tileData[0]['text']
          except:
            text = 'Blank'
          try:
            b_buttons = tileData[0]['buttons']
            b_list = []
            for each in b_buttons:
              b_list.append(each['name'])
            buttons = str(b_list)
          except:
            buttons = 'Blank'

        # STRUCTURED ENGAGEMENT 
        if results['type'] == 'STRUCTURED':
    
          tile = results['tile']
          tileData = tile['tileData']
    
          try:
            title = tileData[0]['title']
          except:
            title = 'Blank'
          try:
            subTitle = tileData[0]['subTitle']
          except:
            subTitle = 'Blank'
          try:
            image = tileData[0]['image']
          except:
            image = 'Blank'
          
          text = "Title: " + title + "\n" + "Subtitle: " + subTitle + "\n" + "Image: " + image
    
          try:
            s_buttons = tileData[0]['buttons']
            s_list = []
            for each in s_buttons:
              s_list.append(each['name'])
            buttons = str(s_list)
          except:
            buttons = 'Blank'

          
        row.append(text) #<-------- Text
        row.append(buttons) #<-------- Buttons
    
    
      else:
        
        row.append('Dynamic') #<-------- Engagement Type
        row.append('N/A') #<-------- Text
        row.append('N/A') #<-------- Buttons
    
    
      row.append(next_message) #<--------
      dialog_engagement_name = dialog_name + ' / ' + engagement_name
      row.append(dialog_engagement_name) #<--------
      table.append(row)
    
    
    #print(table)
    
    # Sort Table by Dialog Name Pandas <---- Sorted by list Lower down
    
    #import pandas as pd
    #df = pd.DataFrame(table, columns=('dialog_name', 'engagement_name', 'prev_engagement', 'engagement_type', 'engagement_text', 'buttons', 'next_engagement'))
    
    #df2 = df.sort_values('dialog_name')
    
    #print(df2)
    #df2.to_csv('UN_Sorted_Bot.csv')
    
    
    
    
    # Sort Table by Dialog Name List
    
    # Sort Table by engagement name where prev / Engagement / Next
    
    #print(table)
    
    dialog = ''
    
    
    new_list = []
    new_temp_list_clean = []
    
    for i in groupDict:
      new_temp_list = []
      #print('next dialog' + i)
    
    
      for j in range(len(table)):
        #print(table[j][0])
        #print(groupDict[i])
    
        if table[j][0] == groupDict[i]:
          new_temp_list.append(table[j])
    
      
      # FIND INITIAL Enagaement
    
      for k in range(len(new_temp_list)):
        if new_temp_list[k][2] == 'No Prev Engagement':
          new_temp_list_clean.append(new_temp_list[k])
    
    
      for l in range(len(new_temp_list)):
        for m in range(len(new_temp_list)):
          if new_temp_list[m][1] == new_temp_list_clean[len(new_temp_list_clean)-1][6]:
            #print('next engagement found')
            #print(new_temp_list[m][1])
            #print(new_temp_list_clean[len(new_temp_list_clean)-1][6])
            new_temp_list_clean.append(new_temp_list[m])
      
    import pandas as pd
    df3 = pd.DataFrame(new_temp_list_clean, columns=('dialog_name', 'engagement_name','prev_engagement', 'engagement_type', 'engagement_text', 'buttons', 'next_engagement', 'dialog_engagement_name'))
    
    #print(df3)  
    st.write('Extraction Completed')
    


    # Download the Result
    data_as_csv = df3.to_csv(index=False).encode("utf-8")
    
    strip_file_name = uploaded_file.name[:-5]
    export_file_name = "EXP - " + strip_file_name + ".csv"
    
    st.download_button('Download Output', data=data_as_csv, file_name=export_file_name)
