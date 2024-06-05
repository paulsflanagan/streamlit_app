ificimport streamlit as st
from io import StringIO
import requests
import json
import csv
import ast
import zipfile
import os

st.title('Lucid Generator')


l_cid = st.secrets["l_cid"]
l_cs = st.secrets["l_cs"]
l_ruri = st.secrets["l_ruri"]

st.write(' Visit: https://lucid.app/oauth2/authorize?client_id=P9FbSFWxRxWyQyP_qXaeZI6t1f2OFu9FJhRb1mbi&redirect_uri=https://lucid.app/oauth2/clients/P9FbSFWxRxWyQyP_qXaeZI6t1f2OFu9FJhRb1mbi/redirect&scope=lucidchart.document.content%20offline_access%20user.profile')

code = st.text_input("Enter Verification Code", "")

uploaded_file = st.file_uploader("Choose a file (Bot Export CSV)")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    
    if st.button("Generate Lucid"):
        
        # Create oAuth token
        url = 'https://api.lucid.co/oauth2/token'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "code": code,
            "client_id": l_cid,
            "client_secret": l_cs,
            "grant_type": "authorization_code",
            "redirect_uri": l_ruri
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        tokenHolder = json.loads(response.text)
        oAuth = tokenHolder['access_token']
        #st.write(oAuth)

        
        ##################################################################
        # Lucid Json Generator Functions
        ##################################################################

        
        # https://developer.lucid.co/standard-import/#overview
        
        import json
        from string import Template
        
        
        g_page = ''
        g_shapes = []
        g_lines = []
        
        
        # Define Global Settings
        
        g_id = "Page1"
        g_title = "My Lucid"
        
        g_style_rectangle = '{"fill": {"type": "color","color": "#ffffff"},"stroke": {"color": "#C3CFD9","width": 3,"style": "solid"},"rounding": 0}'
        g_style_dialog = '{"fill": {"type": "color","color": "#ffffff"},"stroke": {"color": "#5E5E5E","width": 3,"style": "solid"},"rounding": 10}'
        
        # Define Global Counters
        g_shape_counter = 0
        g_dialog_starter_counter = 0
        g_dialog_counter = 0
        g_text_counter = 0
        g_option_counter = 0
        g_manual_input_counter = 0
        g_title_counter = 0
        g_escalation_counter = 0
        g_dynamic_counter = 0
        g_line_counter = 0
        
        # Define Global Co-ordinates
        g_bounding_box_x = 100
        g_bounding_box_y = 100
        g_bounding_box_r = 0
        
        # Define Engagement ID Buffers
        g_current_eng_id = ''
        g_prev_eng_id = ''
        
        # Text Formatting future itteration = <p style=\"font-size: 5pt;text-align: left;color: green\">A paragraph with HTML formatting.</p>
        
        #color
        #font-family
        #font-size
        #font-style
        #font-weight
        #text-align
        #text-decoration
        #vertical-align
        
        
        
        
        ### Initialization Functions ###
        
        def initializePage():
          global g_page, g_shapes, g_lines, g_shape_counter, g_dialog_starter_counter,g_dialog_counter, g_line_counter, g_bounding_box_x, g_bounding_box_y, g_bounding_box_r, g_current_eng_id, g_prev_eng_id, g_text_counter, g_title_counter, g_escalation_counter, g_dynamic_counter, g_manual_input_counter, g_option_counter
          g_page = ''
          g_shapes = []
          g_lines = []
          g_shape_counter = 0
          g_dialog_starter_counter = 0
          g_dialog_counter = 0
          g_text_counter = 0
          g_option_counter = 0
          g_manual_input_counter = 0
          g_title_counter = 0
          g_escalation_counter = 0
          g_dynamic_counter = 0
          g_line_counter = 0
          g_bounding_box_x = 100
          g_bounding_box_y = 100
          g_bounding_box_r = 0
          g_current_eng_id = ''
          g_prev_eng_id = ''
        
        
        
        ### Mobility Functions ###
        
        def setPosition(x,y):
          global g_bounding_box_x, g_bounding_box_y
          g_bounding_box_x = x
          g_bounding_box_y = y
        
        def getPositionX():
          global g_bounding_box_x
          return g_bounding_box_x
        
        def getPositionY():
          global g_bounding_box_y
          return g_bounding_box_y
        
        def shiftNewLine():
          global g_bounding_box_x, g_bounding_box_y
          g_bounding_box_x += 800
          g_bounding_box_y = 100
          
        
        
        ### Engagement ID Buffer Functions ###
        
        def updateCurrentEngagement(current_eng_id):
          global g_prev_eng_id, g_current_eng_id
          g_prev_eng_id = g_current_eng_id
          g_current_eng_id = current_eng_id
          #print("___")
          #print("Prev: " + g_prev_eng_id)
          #print("Current: " + g_current_eng_id)
          #print("___")
        
        def resetEngagementBuffer():
          global g_prev_eng_id, g_current_eng_id
          g_prev_eng_id = ''
          g_current_eng_id = ''
        
        def checkEngagementBuffer():
          global g_prev_eng_id, g_current_eng_id
          if g_prev_eng_id == '':
            return False
          else:
            return True
        
        ### Block Functions ###
        
        def addDialogBlock(dialog_name):
          # Dialog Unq ID from dialog_name
          bounding_box_w = 150
          bounding_box_h = 100
          global g_dialog_counter, g_bounding_box_x, g_bounding_box_y, g_bounding_box_r
          g_bounding_box_x += 62.5
          #shape = Template('{"id": "dl_$dialog_counter","type": "predefinedProcess","boundingBox": {"x": $bounding_box_x, "y": $bounding_box_y, "w": $bounding_box_w, "h": $bounding_box_h, "rotation": $bounding_box_r},"style": $style,"text": "$dialog_name","sideWidth": 0.1,"customData": [{"key":"Num","value":"$shape_counter"},{"key":"Prev","value":"=upstream.Num"}],"opacity": 100}')
          
          current_engagement_id = "dl_" + str(g_dialog_counter)
          updateCurrentEngagement(current_engagement_id)
        
          dialog_name = dialog_name.replace("'", "")
        
          shape = Template('{"id": "$current_engagement_id","type": "predefinedProcess","boundingBox": {"x": $bounding_box_x, "y": $bounding_box_y, "w": $bounding_box_w, "h": $bounding_box_h, "rotation": $bounding_box_r},"style": $style,"text": "$dialog_name","sideWidth": 0.1,"opacity": 100}')
          g_shapes.append(shape.substitute(current_engagement_id=current_engagement_id, bounding_box_x=g_bounding_box_x, bounding_box_y=g_bounding_box_y, bounding_box_w=bounding_box_w, bounding_box_h=bounding_box_h, bounding_box_r=g_bounding_box_r, dialog_name=dialog_name, style=g_style_dialog))
          #updateCurrentEngagement("")
          g_dialog_counter += 1
          g_bounding_box_y += bounding_box_h
          g_bounding_box_x -= 62.5
          #lines?
        
        
        def addTitleBlock(engagement_name):
          # id = titleX? Shape counter becomes title counter ##### ACTUALLY COULD BE title_ +ENGAGEMENT NAME!!! UNIQUE ID
          bounding_box_w = 275
          bounding_box_h = 40
          global g_title_counter, g_bounding_box_x, g_bounding_box_y, g_bounding_box_r
        
          current_engagement_id = "ttl_" + str(g_title_counter)
          updateCurrentEngagement(current_engagement_id)
        
          engagement_name = engagement_name.replace("'", "")
        
          shape = Template('{"id": "$current_engagement_id","type": "rectangle","boundingBox": {"x": $bounding_box_x, "y": $bounding_box_y, "w": $bounding_box_w, "h": $bounding_box_h, "rotation": $bounding_box_r},"style": $style,"text": "$engagement_name","opacity": 100}')
          g_shapes.append(shape.substitute(current_engagement_id=current_engagement_id, bounding_box_x=g_bounding_box_x, bounding_box_y=g_bounding_box_y, bounding_box_w=bounding_box_w, bounding_box_h=bounding_box_h, bounding_box_r=g_bounding_box_r, engagement_name=engagement_name, style=g_style_rectangle))
          g_title_counter += 1
          g_bounding_box_y += bounding_box_h
          #lines?
        
        
        def addTextBlock(text):
          # id = textX? Shape counter becomes text counter ##### ACTUALLY COULD BE text_ +ENGAGEMENT NAME!!! UNIQUE ID
          bounding_box_w = 275
          bounding_box_h = 125
          global g_text_counter, g_bounding_box_x, g_bounding_box_y, g_bounding_box_r
        
          current_engagement_id = "tx_" + str(g_text_counter)
          updateCurrentEngagement(current_engagement_id)
        
          text = text.replace("'", "")
        
          shape = Template('{"id": "$current_engagement_id","type": "rectangle","boundingBox": {"x": $bounding_box_x, "y": $bounding_box_y, "w": $bounding_box_w, "h": $bounding_box_h, "rotation": $bounding_box_r},"style": $style,"text": "$text","opacity": 100}')
          g_shapes.append(shape.substitute(current_engagement_id=current_engagement_id, bounding_box_x=g_bounding_box_x, bounding_box_y=g_bounding_box_y, bounding_box_w=bounding_box_w, bounding_box_h=bounding_box_h, bounding_box_r=g_bounding_box_r, text=text, style=g_style_rectangle))
          g_text_counter += 1
          g_bounding_box_y += bounding_box_h
          #lines?
        
        
        def addOptionBlock(text):
          bounding_box_w = 275
          bounding_box_h = 75
          global g_option_counter, g_bounding_box_x, g_bounding_box_y, g_bounding_box_r
        
          current_engagement_id = "op_" + str(g_option_counter)
          updateCurrentEngagement(current_engagement_id)
        
          text = text.replace("'", "")
        
          shape = Template('{"id": "$current_engagement_id","type": "rectangle","boundingBox": {"x": $bounding_box_x, "y": $bounding_box_y, "w": $bounding_box_w, "h": $bounding_box_h, "rotation": $bounding_box_r},"style": $style,"text": "$text","opacity": 100}')
          g_shapes.append(shape.substitute(current_engagement_id=current_engagement_id, bounding_box_x=g_bounding_box_x, bounding_box_y=g_bounding_box_y, bounding_box_w=bounding_box_w, bounding_box_h=bounding_box_h, bounding_box_r=g_bounding_box_r, text=text, style=g_style_rectangle))
          g_option_counter += 1
          g_bounding_box_y += bounding_box_h
        
        
        
        def addDynamicBlock(engagement_name):
          bounding_box_w = 275
          bounding_box_h = 150
          global g_dynamic_counter, g_bounding_box_x, g_bounding_box_y, g_bounding_box_r
        
          current_engagement_id = "dy_" + str(g_dynamic_counter)
          updateCurrentEngagement(current_engagement_id)
        
          engagement_name = engagement_name.replace("'", "")
        
          shape = Template('{"id": "$current_engagement_id","type": "directAccessStorage","boundingBox": {"x": $bounding_box_x, "y": $bounding_box_y, "w": $bounding_box_w, "h": $bounding_box_h, "rotation": $bounding_box_r},"style": $style,"text": "$engagement_name","opacity": 100}')
          g_shapes.append(shape.substitute(current_engagement_id=current_engagement_id, bounding_box_x=g_bounding_box_x, bounding_box_y=g_bounding_box_y, bounding_box_w=bounding_box_w, bounding_box_h=bounding_box_h, bounding_box_r=g_bounding_box_r, engagement_name=engagement_name, style=g_style_rectangle))
          g_dynamic_counter += 1
          g_bounding_box_y += bounding_box_h
          #lines?
        
        
        def addDialogStarterBlock(engagement_name, text):
          bounding_box_w = 275
          bounding_box_h = 125
          global g_dialog_starter_counter, g_bounding_box_x, g_bounding_box_y, g_bounding_box_r
        
          current_engagement_id = "ds_" + str(g_dialog_starter_counter)
          updateCurrentEngagement(current_engagement_id)
        
          engagement_name = engagement_name.replace("'", "")
          text = text.replace("'", "")
        
          engagement_text = engagement_name + text
        
          #shape = Template('{"id": "ds_$engagement_name","type": "manualInput","boundingBox": {"x": $bounding_box_x, "y": $bounding_box_y, "w": $bounding_box_w, "h": $bounding_box_h, "rotation": $bounding_box_r},"style": $style,"text": "$engagement_name","customData": [{"key":"Num","value":"$shape_counter"},{"key":"Prev","value":"=upstream.Num"}],"opacity": 100}')
          shape = Template('{"id": "$current_engagement_id","type": "manualInput","boundingBox": {"x": $bounding_box_x, "y": $bounding_box_y, "w": $bounding_box_w, "h": $bounding_box_h, "rotation": $bounding_box_r},"style": $style,"text": "$engagement_text","opacity": 100}')
          g_shapes.append(shape.substitute(current_engagement_id=current_engagement_id, bounding_box_x=g_bounding_box_x, bounding_box_y=g_bounding_box_y, bounding_box_w=bounding_box_w, bounding_box_h=bounding_box_h, bounding_box_r=g_bounding_box_r, engagement_text=engagement_text, style=g_style_rectangle))
          
          g_dialog_starter_counter += 1
          g_bounding_box_y += bounding_box_h
        
        
        def addManualInputBlock(engagement_name):
          bounding_box_w = 150
          bounding_box_h = 100
          global g_manual_input_counter, g_bounding_box_x, g_bounding_box_y, g_bounding_box_r
          g_bounding_box_x += 62.5
         
          current_engagement_id = "mi_" + str(g_manual_input_counter)
          updateCurrentEngagement(current_engagement_id)
        
          engagement_name = engagement_name.replace("'", "")
        
          #shape = Template('{"id": "ds_$engagement_name","type": "manualInput","boundingBox": {"x": $bounding_box_x, "y": $bounding_box_y, "w": $bounding_box_w, "h": $bounding_box_h, "rotation": $bounding_box_r},"style": $style,"text": "$engagement_name","customData": [{"key":"Num","value":"$shape_counter"},{"key":"Prev","value":"=upstream.Num"}],"opacity": 100}')
          shape = Template('{"id": "$current_engagement_id","type": "manualInput","boundingBox": {"x": $bounding_box_x, "y": $bounding_box_y, "w": $bounding_box_w, "h": $bounding_box_h, "rotation": $bounding_box_r},"style": $style,"text": "$engagement_name","opacity": 100}')
          g_shapes.append(shape.substitute(current_engagement_id=current_engagement_id, bounding_box_x=g_bounding_box_x, bounding_box_y=g_bounding_box_y, bounding_box_w=bounding_box_w, bounding_box_h=bounding_box_h, bounding_box_r=g_bounding_box_r, engagement_name=engagement_name, style=g_style_rectangle))
          
          g_manual_input_counter += 1
          g_bounding_box_y += bounding_box_h
          g_bounding_box_x -= 62.5
        
        
        def addEscalationBlock(dialog_name):
          # Dialog Unq ID from dialog_name
          bounding_box_w = 150
          bounding_box_h = 100
          global g_escalation_counter, g_bounding_box_x, g_bounding_box_y, g_bounding_box_r
          g_bounding_box_x += 62.5
          #shape = Template('{"id": "dl_$dialog_counter","type": "predefinedProcess","boundingBox": {"x": $bounding_box_x, "y": $bounding_box_y, "w": $bounding_box_w, "h": $bounding_box_h, "rotation": $bounding_box_r},"style": $style,"text": "$dialog_name","sideWidth": 0.1,"customData": [{"key":"Num","value":"$shape_counter"},{"key":"Prev","value":"=upstream.Num"}],"opacity": 100}')
          
          current_engagement_id = "esc_" + str(g_escalation_counter)
          updateCurrentEngagement(current_engagement_id)
        
          dialog_name = dialog_name.replace("'", "")
        
          shape = Template('{"id": "$current_engagement_id","type": "predefinedProcess","boundingBox": {"x": $bounding_box_x, "y": $bounding_box_y, "w": $bounding_box_w, "h": $bounding_box_h, "rotation": $bounding_box_r},"style": $style,"text": "$dialog_name","sideWidth": 0.1,"opacity": 100}')
          g_shapes.append(shape.substitute(current_engagement_id=current_engagement_id, bounding_box_x=g_bounding_box_x, bounding_box_y=g_bounding_box_y, bounding_box_w=bounding_box_w, bounding_box_h=bounding_box_h, bounding_box_r=g_bounding_box_r, dialog_name=dialog_name, style=g_style_dialog))
          #updateCurrentEngagement("")
          g_escalation_counter += 1
          g_bounding_box_y += bounding_box_h
          g_bounding_box_x -= 62.5
          #lines?
        
        
        
        
        ### Add Line
        
        def addLineRight():
          global g_line_counter, g_current_eng_id, g_prev_eng_id
          line = Template('{"id":"line$line_counter","lineType":"elbow","endpoint1":{"type":"shapeEndpoint","style":"none","shapeId":"$prev_eng_id","position":{"x":1,"y":0.5}},"endpoint2":{"type":"shapeEndpoint","style":"arrow","shapeId":"$current_eng_id","position":{"x":0,"y":0.5}}}')
          g_lines.append(line.substitute(line_counter=g_line_counter, current_eng_id=g_current_eng_id, prev_eng_id=g_prev_eng_id))
          #{"id":"line0","lineType":"elbow""position":0.5,"side":"middle"}],"endpoint1":{"type":"shapeEndpoint","style":"none","shapeId":"block0","position":{"x":1,"y":0.5}},"endpoint2":{"type":"shapeEndpoint","style":"arrow","shapeId":"block1","position":{"x":0,"y":0.5}}}
          #print("**ADDING LINE RIGHT**")
          g_line_counter += 1
        
        
        def addLineBottom():
          global g_line_counter, g_current_eng_id, g_prev_eng_id
          line = Template('{"id":"line$line_counter","lineType":"elbow","endpoint1":{"type":"shapeEndpoint","style":"none","shapeId":"$prev_eng_id","position":{"x":0.5,"y":1}},"endpoint2":{"type":"shapeEndpoint","style":"arrow","shapeId":"$current_eng_id","position":{"x":0.5,"y":0}}}')
          g_lines.append(line.substitute(line_counter=g_line_counter, current_eng_id=g_current_eng_id, prev_eng_id=g_prev_eng_id))
          #{"id":"line0","lineType":"elbow","endpoint1":{"type":"shapeEndpoint","style":"none","shapeId":"block0","position":{"x":1,"y":0.5}},"endpoint2":{"type":"shapeEndpoint","style":"arrow","shapeId":"block1","position":{"x":0,"y":0.5}}}
          #print("**ADDING LINE BOTTOM**")
          g_line_counter += 1
        
        
        
        ### Engagement Functions ###
        
        def addDialogStarterEngagement(engagement_name,dialog_name,text):
          global g_bounding_box_y, g_bounding_box_x, g_line_counter, g_dialog_starter_counter, g_dialog_counter, g_lines
          addDialogStarterBlock(engagement_name,text)
          g_bounding_box_y -= 112.5
          g_bounding_box_x += 350
          addDialogBlock(dialog_name)
          g_bounding_box_y += 112.5
          g_bounding_box_x -= 350
          g_bounding_box_y -= 50
          addLineRight()
        
        def addDialogEngagement(dialog_name):
          global g_bounding_box_y
          addDialogBlock(dialog_name)
          g_bounding_box_y += 125
        
        def addTextEngagement(engagement_name,engagement_text):
          global g_bounding_box_y
          addTitleBlock(engagement_name)
          addLineBottom()
          resetEngagementBuffer()
          addTextBlock(engagement_text)
          g_bounding_box_y += 125
        
        
        
        def addTextQuestionEngagement(engagement_name,engagement_text):
          global g_bounding_box_y
          addTitleBlock(engagement_name)
          addLineBottom()
          resetEngagementBuffer()
          addTextBlock(engagement_text)
          g_bounding_box_y += 50
          addManualInputBlock('Manual Input')
          addLineBottom()
          g_bounding_box_y += 125
        
        
        
        
        def addOptionsEngagement(engagement_name,engagement_text,options): ### NOT YET UPDATED
          global g_bounding_box_y
          addTitleBlock(engagement_name)
          addLineBottom()
          resetEngagementBuffer()
          addTextBlock(engagement_text)
          for each in options:
            text = each.replace("'", "")
            addOptionBlock(text)
          g_bounding_box_y += 125
        
        def addDynamicEngagement(engagement_name):
          global g_bounding_box_y
          addDynamicBlock(engagement_name)
          g_bounding_box_y += 125
        
        def addEscalationEngagement(dialog_name):
          global g_bounding_box_y
          addEscalationBlock(dialog_name)
          g_bounding_box_y += 125
        
        
        
        ### Finalization Functions ###
        
        def buildPage():
          global g_page, g_id, g_title, g_shapes
          #gj_shapes = json.dumps(g_shapes)
          
          #page = Template('{"id": "$id","title": "$title","shapes": $shapes}')
          #g_page = page.substitute(id=g_id, title=g_title, shapes=g_shapes)
        
          page = Template('{"id": "$id","title": "$title","shapes": $shapes,"lines": $lines}')
          g_page = page.substitute(id=g_id, title=g_title, shapes=g_shapes, lines=g_lines)
        
        def buildDocument():
          global g_page
          document = Template('{"version":1,"pages":[$page]}')
          x = document.substitute(page=g_page).replace("'", "")
          return x

        
        ##################################################################
        # Generate from Bot Export
        ##################################################################

        raw_data = list(csv.reader(stringio, delimiter=","))

        st.write("Line Count: " + str(len(raw_data)-1))


        ### Inititalize Page
        
        initializePage()
        
        
        ### Generate Dialog Starters
        
        for row in raw_data:
          if "DIALOG_STARTER" in row[3]:
            text = row[4].replace("'", "")
            addDialogStarterEngagement(row[1],row[0],text)
        
        resetEngagementBuffer()
        
        
        
        
        ### Generate Dialogs
        
        preDialog = 'dialog_name'
        
        
        # Generate Dialog Engagement
        
        for line in raw_data:
        
          enableLine = True
        
          if line[0] not in preDialog:
            preDialog = line[0]
            shiftNewLine()
            resetEngagementBuffer()
            addDialogEngagement(line[0])
        
        
        # Generate Text Engagements
        
          if line[3] == "TEXT":
            addTextEngagement(line[1],line[4])
        
        
        # Generate Text Questions Engagements ###### Visual Output Optimisation needed to add manual input 
          if line[3] == "TEXT_QUESTION":
            addTextQuestionEngagement(line[1],line[4])
        
        
        # Generate Multiple Choice Question Engagements
          if line[3] == "MULTIPLE_CHOICE_QUESTION":
            options = ast.literal_eval(line[5])
            addOptionsEngagement(line[1],line[4],options)
            enableLine = False
        
        
        # Generate Quick Reply Engagements
          if line[3] == "QUICK_REPLY":
            options = ast.literal_eval(line[5])
            addOptionsEngagement(line[1],line[4],options)
            enableLine = False
        
        
        # Generate Button Engagements
          if line[3] == "BUTTON":
            options = ast.literal_eval(line[5])
            addOptionsEngagement(line[1],line[4],options)
            enableLine = False
        
        
        # Generate Dynamic Engagements
          if line[3] == "Dynamic":
            addDynamicEngagement(line[1])
        
        
        # Generate Structured Engagements
        
          if line[3] == "STRUCTURED":
            options = ast.literal_eval(line[5])
            addOptionsEngagement(line[1],line[4],options)
            enableLine = False
        
        
        # Generate Escalation Engagements
        
          if line[3] == "ESCALATION":
            addEscalationEngagement("Escalation: " + line[1])
        
        # Add a line if needed
          if checkEngagementBuffer():
            if enableLine:
              addLineBottom()
        
        
        
        
        ### Build Page
        
        buildPage()
        
        
        ### Build Document / Save to document.json
        
        file1 = open('document.json', 'w')
        file1.write(buildDocument())
        file1.close()
        st.write("Export Complete")  

        
        # Create a new ZIP file
        with zipfile.ZipFile('import.lucid', 'w') as zipf:
            # Add the document.json file to the ZIP file
            zipf.write('document.json')
        

        file_name = "Extraction: " + uploaded_file.name
        
        # Create Chart
        url = 'https://api.lucid.co/documents'
        headers = {
            'Authorization': 'Bearer '+ oAuth,
            'Lucid-Api-Version': '1'
        }
        files = {
            'file': ('import.lucid', open('import.lucid', 'rb'), 'x-application/vnd.lucid.standardImport')
        }
        data = {
            'title': file_name,
            'product': 'lucidchart',
            #'parent': '1234'
        }
        response = requests.post(url, headers=headers, files=files, data=data)
        responseDict = json.loads(response.text)
        st.write("Here is your Lucid: " + responseDict['editUrl'])
