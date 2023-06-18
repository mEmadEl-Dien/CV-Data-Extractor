import re
import os
import sys
import pandas as pd
import pdf2txt

# For (NLP) Natural Language Processing
import spacy

# Our resultant Dictionary
resultDict = {'names': [], 'phones': [], 'emails': [], 'skills': []}
names = []
phones = []
emails = []
skills = []
# gpas = []

# Loading the English Language model
nlp = spacy.load('en_core_web_sm')

def convert_pdf_to_txt(fileName):
    parent_dir = os.path.dirname(args[1])

    output_dir = os.path.join(parent_dir, 'output')

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    txt_dir = os.path.join(output_dir, 'txt')

    # Create the txt directory if it doesn't exist
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)

    outputFileName = os.path.basename(os.path.splitext(fileName)[0]) + '.txt'
    outputFilePath = os.path.join(txt_dir, outputFileName)

    # Converting the PDF file to TXT and save it in the given path (outputFilePath)
    pdf2txt.main(args=[fileName, '--outfile', outputFilePath])

    # Returning the content of the converted pdf
    return open(outputFilePath).read()

def parse_txt_content(text):
    # Processing the pdf text using the English Language Model
    content = nlp(text)

    # Retrieve the skills from sys.argv
    skillsArgs = sys.argv[2:]
    skillsPattern = '|'.join(skillsArgs)

    # Made by the help of chat gpt
    phonePattern = re.compile('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    skillsetPattern = re.compile(skillsPattern)
    # gpaPattern = r"\bGPA\s+(\d+(?:\.\d+)?)\b"


    name = [entity.text for entity in content.ents if entity.label_ == 'PERSON'][0]
    email = [word for word in content if word.like_email == True][0]
    phone = str(re.findall(phonePattern, text.lower()))
    skillsList = re.findall(skillsetPattern, text.lower())
    # gpa = str(re.findall(gpaPattern, text))

    # To get only unique skills
    uniqueSkillsList = str(set(skillsList))

    names.append(name)
    emails.append(email)
    phones.append(phone)
    skills.append(uniqueSkillsList)
    # gpas.append(gpa)


#Starting the main program by taken the user input arguments
args = sys.argv

if len(args) < 3:
    raise Exception("Just Give me two paths, 1) The Script path, 2) The Directory path which contains the CVs, 3) The list of skills you want to search for")

for file in os.listdir(args[1]):
    if file.endswith('.pdf'):
        txt = convert_pdf_to_txt(os.path.join(args[1], file))
        parse_txt_content(txt)

# Assigning our values (names, phones, emails, skills, and gpas to our resultDict)
resultDict['names'] = names
resultDict['phones'] = phones
resultDict['emails'] = emails
resultDict['skills'] = skills
# resultDict['gpas'] = gpas

resultDict['names'][0] = resultDict['names'][0].rstrip()

df = pd.DataFrame(resultDict)

# Getting the parent directory
parent_dir = os.path.dirname(args[1])

csvPath = os.path.join(parent_dir, 'output', 'csv')

# Create the output directory if it doesn't exist
if not os.path.exists(csvPath):
    os.makedirs(csvPath)

csvPath = os.path.join(csvPath, 'output.csv')

df.to_csv(csvPath, index=False)