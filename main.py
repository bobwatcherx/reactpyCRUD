# INSTALL FASTAPI IN YOU PC WITH pip install fastapi
# and install uvicorn
from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component,html,use_state
import reactpy as rp

@component
def MyCrud():
	# NOW I CREATE STATE
	alltodo = use_state([])
	name,set_name = use_state("")
	age,set_age = use_state(0)

	is_edit = use_state(False)
	nameedit,set_nameedit = use_state("")
	ageedit,set_ageedit = use_state(0)

	id_edit = use_state(0)
	# AND NOW PREVENT IF YOU CLICK BUTTON DISABLE RELOAD
	@rp.event(prevent_default=True)
	def mysubmit(event):
		newtodo = {
		"name":name,
		"age":age
		}

		# AND PUSH TO alltodo
		alltodo.set_value(alltodo.value + [newtodo])



	def deletebtn(b):
		print("you select",b)
		update_todos = [item for index,item in enumerate(alltodo.value) if index != b]
		alltodo.set_value(update_todos)		


	def editbtn(b):
		is_edit.set_value(True)
		# AND SET YOU DATA FROM BUTTON TO TEXTFIELD
		for i,x in enumerate(alltodo.value):
			if i == b:
				set_nameedit(x['name'])
				set_ageedit(x['age'])
				id_edit.set_value(b)


	def savedata(event):
		# AND I FIND id if equal THEN UPDATE
		for i,x in enumerate(alltodo.value):
			if i == id_edit.value:
				x['name'] = nameedit
				x['age'] = ageedit
		is_edit.set_value(False)
		# AND CLEAR INPUT
		set_nameedit("")
		set_ageedit("")
		id_edit.set_value(0)


	# AND NOW I LOOPING DATA FROM alltodo
	# AND SHOW IN WEB

	list = [html.li({
		"key":b
		},
		f"{b} - {i['name']} - {i['age']}",
		# NOW I WILL CREATE BUTTON
		html.button({
			"on_click":lambda event,b=b:deletebtn(b)
			},"delete"),
		html.button({
			"on_click":lambda event,b=b:editbtn(b)
			},"edit"),


		) for b,i in enumerate(alltodo.value)]





	return html.div({
		"style":{"padding":"10px"}
		},
		# NOW i create form for submit button
		html.form(
			{"on_submit":mysubmit},
			# AND CREATE TEXT INPUT
			html.input({
				"type":"text",
				"placeholder":"name",
				"on_change":lambda event:set_name(event['target']['value'])

				}),
			html.input({
				"type":"text",
				"placeholder":"age",
				"on_change":lambda event:set_age(event['target']['value'])

				}),
			# AND CREATE BUTTON SUBMIT
			html.button({
				"type":"submit"
				},"add new you todo")
			),

		# AND NOW I WILL CREATE TEXTINPUT FOR EDIT AND UPDATE
		html.div(
			# THIS WILL SHOW IF is_edit == True
			# and HIDE IF is_edit == False
			{
			"style":{"display":"none" if is_edit.value == False else "block" }
			},
			html.input({
			"type":"text",
			"value":nameedit,
			"placeholder":"name",
			"on_change":lambda event:set_nameedit(event['target']['value'])

			}),
		html.input({
			"type":"text",
			"value":ageedit,
			"placeholder":"age",
			"on_change":lambda event:set_ageedit(event['target']['value'])

			}),
		html.button({
				"on_click":savedata
				},"Update Guys"),
			),


		html.ul(list)
		)	

app = FastAPI()
configure(app,MyCrud)
