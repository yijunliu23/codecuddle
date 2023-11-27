from aux import read_jsx_to_string, call_gpt4, call_gpt_with_retries_json, read_txt

function = "This webpage is used to find common avaliable times for people (aka scheduling app). " \
           "It contains a table and an input field. " \
           "Users can enter their names in the input field and mark their avalibale times on the table. " \
           "It also has a function to fnd the common avaliable times for all the users."

webpage = read_jsx_to_string('./webpage.jsx')

prompt_1 = "Based on the function " + \
           function + \
           ". I want to make the webpage more inclusive by avoiding socially akward situation. " \
           "Output in a JSON format like \"features\":[{\"feature\":\"feature name\", \"description\":\"feature description\", " \
                                    "\"location\": \"location on the main page, like left, right, center\"}]}"


feature = "Different time zones"
description = "Indicating the time zones "

prompt_2 = "I want to add this feature to my existing react.js code." \
           "This is my current webpage in jsx" + webpage + \
            "and here's the feature I want to add: " + feature + description + \
            "Output the complete react.js code implemented the function."