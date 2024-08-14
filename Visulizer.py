from tkinter import *
import tkinter.messagebox
import re
from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter
from PIL import Image,ImageTk

class MyFirstGUI: #class definition

    def __init__(self, root):
        self.master = root
        self.master.title("Lexical Analyzer for TinyPie")

        #tokenlist
        self.ListOutput = []

        #LineCounter
        self.lineCounter = 1.0
        self.lineOutputIndex=1.0

        #Label for code input
        self.codeInputLabel = Label(self.master,text="Code Input: ")
        self.codeInputLabel.grid(row=0, column=0, sticky=W, padx=10)

        #Label for code output
        self.codeOutputLabel = Label(self.master, text="Lexical Analyzed Result: ")
        self.codeOutputLabel.grid(row=0, column=2, sticky=W, padx=10)

        #Textbox for code input
        self.codeInputText = Text(self.master, width=55, height=15)
        self.codeInputText.grid(row=1, column=0, sticky=W, padx=10)

        #Textbox for code output
        self.codeOutputText = Text(self.master, width=55, height=15) #width=55, height=15
        self.codeOutputText.grid(row=1, column=2, sticky=W, padx=10)

        #Current Processing Line Label
        self.LineLabel = Label(self.master, text="Currently Processing Line:")
        self.LineLabel.grid(row=2, column=0, sticky=W, padx=10)

        #Line number label
        self.label =Text(self.master,width=10,height=1) #Entry(self.master, text="0")
        self.label.grid(row=2, column=0, sticky=E, padx=10, pady=10)
        self.label.insert('1.0',0)

        #Next line button
        self.LineButton = Button(self.master, text = "Next Line", borderwidth=4, relief=GROOVE, command=self.readNextLine)
        self.LineButton.grid(row=3, column=0, sticky=E, padx=10)

        #Exit Button
        self.exitButton = Button(self.master, text = "Quit", borderwidth=4, relief=GROOVE, command=self.master.destroy)
        self.exitButton.grid(row=3, column=3, sticky=E, padx=10)

        #Parser Textbox
        self.parserBox = Text(self.master, width=55, height=15)
        self.parserBox.grid(row=1, column=3, sticky=E, padx=10)

        #Parser Label
        self.parserLabel = Label(self.master, text="Parsed Result")
        self.parserLabel.grid(row=0, column=3, sticky=W, padx=10)

        #Parser Line Counter
        self.parserOutput = 1.0

        #tokenTuple
        self.tokenTuple = ("Empty","Empty")

        #tokenList
        self.Mytokens = []

        #Canvas box and configeration
        self.canvasBox = Canvas(self.master, width=1400, height=400, bg="grey")
        self.canvasBox.grid(row=4, column=0, sticky=W, padx=10, columnspan=4)

        self.scroll_x = Scrollbar(self.master, orient="horizontal", command=self.canvasBox.xview)
        self.scroll_x.grid(row=5,sticky=EW, columnspan=4)

        self.scroll_y = Scrollbar(self.master, orient="vertical", command=self.canvasBox.yview)
        self.scroll_y.grid(row=4, column=0, sticky=W)


        self.canvasBox.configure(scrollregion=self.canvasBox.bbox("all"))


    #Read user input
    def readNextLine(self):
        #Check if there is text in the current line
        if len(self.codeInputText.get(str(self.lineCounter),str(int(self.lineCounter))+'.end' )) != 0: #Check if the current line has any text
            #Get the list of tokens from the current line text
            inputString = self.codeInputText.get(str(self.lineCounter),str(int(self.lineCounter))+'.end')
            print(inputString)
            self.LexerList = self.CutOneLineTokens(inputString)
            print(self.LexerList)

            #Send the current line of text to the outputTextBox
            for i in self.LexerList:
                self.codeOutputText.insert(str(self.lineOutputIndex),i+"\n")
                self.lineOutputIndex+=1

            #Print the list of tuples that will be passed to parser
            for i in self.Mytokens:
                print(i)

            print()

            #Genereate a parse tree given the ListOutput
            self.parser()


            #Move the line to the next part of the text box and change the line number text
            self.label.delete('1.0','1.end');
            self.label.insert('1.0',int(self.lineCounter))
            self.lineCounter+=1

            #Set tokenTuple back to empty
            self.tokenTuple = ("Empty","Empty")
            self.Mytokens = []

        #No text entered in the input line
        else:
            #Display error to user if there is no text in line
            tkinter.messagebox.showerror("Gui Lexer", "Error: Please enter text on line: " + str(int(self.lineCounter)))

    def CutOneLineTokens(self,string):
        outputList = []  # List to store the tokens

        string = string.replace("\t", "") #if user entered tab in the text box
        string = string.replace(" ", "")  # Remove all the whitespace in the string
        print(string)
        while (len(string) != 0):
            result1 = re.match(r'if|else|int|float', string)  # Keyword
            result2 = re.match(r'[*>=+]', string)  # Operator
            result3 = re.match(r'[A-Za-z_][A-Za-z_\d]*', string)  # Identiifer
            result4 = re.match(r'[(;)":]', string)  # Seperators
            result5 = re.match(r'\d+\.\d+', string)  # Literal Float
            result6 = re.match(r'\d+', string)  # Literal Integer
            result7 = re.match(r'\".*\"', string)  # Literal String

            if (result1 != None):  # Add keyword
                outputList.append("<Key," + string[result1.start():result1.end()] + ">")
                self.Mytokens.append(("Keyword",string[result1.start():result1.end()]))
                string = string[result1.end():]

            elif (result2 != None):  # Add operator
                outputList.append("<Op," + string[result2.start():result2.end()] + ">")
                self.Mytokens.append(("Operator", string[result2.start():result2.end()]))
                string = string[result2.end():]

            elif (result3 != None):  # Add identifier
                outputList.append("<Id," + string[result3.start():result3.end()] + ">")
                self.Mytokens.append(("Identifier", string[result3.start():result3.end()]))
                string = string[result3.end():]

            elif (result4 != None):  # Add seperator
                outputList.append("<Sep," + string[result4.start():result4.end()] + ">")
                self.Mytokens.append(("Seperator", string[result4.start():result4.end()]))
                string = string[result4.end():]

                if (result7 != None):  # Add Literal if the string starts with " and ends "
                    outputList.append("<Lit," + string[result7.start():result7.end() - 2] + ">")
                    self.Mytokens.append(("Str_Literal", string[result7.start():result7.end()-2]))
                    string = string[result7.end() - 2:]

            elif (result5 != None):  # Add Integer Literal
                outputList.append("<Lit," + string[result5.start():result5.end()] + ">")
                self.Mytokens.append(("Float_Literal", string[result5.start():result5.end()]))
                string = string[result5.end():]

            elif (result6 != None):  # Add Integer Literal
                outputList.append("<Lit," + string[result6.start():result6.end()] + ">")
                self.Mytokens.append(("Integer_Literal", string[result6.start():result6.end()]))
                string = string[result6.end():]

            else:  # Exit the loop if there is an invalid token
                print("Invalid token detected")
                break
        return outputList

    #Parsing Function
    def parser(self):
        self.parserBox.insert(str(self.parserOutput),"###########Parse tree for line " + str(int(self.lineCounter)) + "###########\n")
        self.parserOutput +=1

        self.tokenTuple = self.Mytokens.pop(0)



        if(self.tokenTuple[1]=="float"): #Use the math_exp

            #Add Math_Exp to tree
            self.Math_Exp = Node("Math_Exp")

            #Set selector value to 1
            self.selector = 1

            self.math_exp()
        elif(self.tokenTuple[1]=="if"):
            #Add if_exp to tree
            self.If_Exp = Node("If_Exp")

            self.if_exp()


        elif(self.tokenTuple[1]=="print"):
            #Add print_exp to tree
            self.Print_Exp = Node("Print_Exp")
            self.selector = 2
            self.print_exp()
        else:
            return

        if (self.tokenTuple[1] == ";"):
            self.parserBox.insert(str(self.parserOutput),"parse tree building success!\n")
            self.parserOutput += 1

            print("\nparse tree building success!")

            # Determine if we add semicolon to math_exp or if_exp
            if (self.selector == 1):  # math_exp
                # Add ID node to Math_exp node
                self.SeperatorNode = Node(";", parent=self.Math_Exp)

                #print the tree
                for pre, fill, node in RenderTree(self.Math_Exp):
                    print("%s%s" % (pre, node.name))

                #Add Generated image to box
                UniqueDotExporter(self.Math_Exp).to_picture("graph.png")
                self.img = ImageTk.PhotoImage(Image.open("graph.png"))
                self.canvasBox.create_image(230,230,image=self.img)
            elif(self.selector ==2):  # print_exp
                self.SeperatorNode = Node(";", parent=self.Print_Exp)

                # print the tree
                for pre, fill, node in RenderTree(self.Print_Exp):
                    print("%s%s" % (pre, node.name))

                # Add Generated image to box
                UniqueDotExporter(self.Print_Exp).to_picture("graph.png")
                self.img = ImageTk.PhotoImage(Image.open("graph.png"))
                self.canvasBox.create_image(230, 230, image=self.img)


        elif (self.tokenTuple[1] == ":"):
            self.parserBox.insert(str(self.parserOutput), "parse tree building success!\n")
            self.parserOutput += 1

            self.SeperatorNode = Node(":", parent=self.If_Exp)

            # print the tree
            for pre, fill, node in RenderTree(self.If_Exp):
                print("%s%s" % (pre, node.name))

            # Add Generated image to box
            UniqueDotExporter(self.If_Exp).to_picture("graph.png")
            self.img = ImageTk.PhotoImage(Image.open("graph.png"))
            self.canvasBox.create_image(230, 230, image=self.img)


            print("\nparse tree building success!")
        return

    #For the print stament
    def print_exp(self):
        self.parserBox.insert(str(self.parserOutput),"----parent node print_exp, finding children nodes:\n")
        self.parserOutput +=1

        print("\n----parent node print_exp, finding children nodes:")
        typeT, token = self.tokenTuple;

        if (typeT == "Identifier"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): identifier\n")
            self.parserOutput += 1

            self.Id_Node = Node("Identifier", parent=self.Print_Exp)
            self.id_Value = Node("Print", parent=self.Id_Node)

            self.parserBox.insert(str(self.parserOutput), "     keyword has child node (token):" + token +"\n")
            self.parserOutput += 1

            print("child node (internal): identifier")
            print("     keyword has child node (token):" + token)
            self.accept_token()

        else:
            self.parserBox.insert(str(self.parserOutput), "expect keyword at the first element of the expression!\n")
            self.parserOutput += 1

            print("expect identifier at the first element of the expression!\n")
            return

        if (self.tokenTuple[0] == "Seperator"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): seperator\n")
            self.parserOutput += 1

            #Add seperator to tree
            self.SeperatorNode = Node("(", parent=self.Print_Exp)

            self.parserBox.insert(str(self.parserOutput),"   seperator has child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            print("child node (internal): seperator")
            print("   seperator has child node (token):" + self.tokenTuple[1])
            self.accept_token()
        else:
            self.parserBox.insert(str(self.parserOutput), "expect seperator as the first element of the expression!\n")
            self.parserOutput += 1

            print("expect seperator as the first element of the expression!\n")
            return


        self.parserBox.insert(str(self.parserOutput), "Child node (internal): content_exp\n")
        self.parserOutput += 1

        self.Content_Exp = Node("Content_Exp", parent=self.Print_Exp)

        print("Child node (internal): content_exp")
        self.content_exp()

        if (self.tokenTuple[0] == "Seperator"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): seperator\n")
            self.parserOutput += 1

            # Add seperator to tree
            self.SeperatorNode = Node(")", parent=self.Print_Exp)

            self.parserBox.insert(str(self.parserOutput),"   seperator has child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            print("child node (internal): seperator")
            print("   seperator has child node (token):" + self.tokenTuple[1])
            self.accept_token()
        else:
            self.parserBox.insert(str(self.parserOutput), "expect seperator as the first element of the expression!\n")
            self.parserOutput += 1

            print("expect seperator as the first element of the expression!\n")
            return

    #For the print stament
    def content_exp(self):
        self.parserBox.insert(str(self.parserOutput), "----parent node content_exp, finding children nodes:\n")
        self.parserOutput += 1

        print("\n----parent node content_exp, finding children nodes:")
        typeT, token = self.tokenTuple;

        if (self.tokenTuple[0] == "Seperator"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): seperator\n")
            self.parserOutput += 1

            self.SeperatorNode = Node("'" ,parent=self.Content_Exp)

            self.parserBox.insert(str(self.parserOutput),"   seperator has child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            print("child node (internal): seperator")
            print("   seperator has child node (token):" + self.tokenTuple[1])
            self.accept_token()

            if(self.tokenTuple[0]=="Str_Literal"):
                self.parserBox.insert(str(self.parserOutput), "child node (internal): Str_Literal\n")
                self.parserOutput += 1

                #Add string literal to tree
                self.String_Literal = Node("String_Literal", parent=self.Content_Exp)
                self.String_Literal_Val = Node(self.tokenTuple[1], parent=self.String_Literal)

                self.parserBox.insert(str(self.parserOutput),"   Str_Literal has child node (token):" + self.tokenTuple[1] + "\n")
                self.parserOutput += 1

                print("child node (internal): Str_Literal")
                print("   Str_Literal has child node (token):" + self.tokenTuple[1])
                self.accept_token()

            else:
                self.parserBox.insert(str(self.parserOutput),"expect Str_Literal at the first element of the expression!\n")
                self.parserOutput += 1

                print("expect Str_Literal at the first element of the expression!\n")
                return

            if(self.tokenTuple[0] == "Seperator"):
                self.parserBox.insert(str(self.parserOutput), "child node (internal): seperator\n")
                self.parserOutput += 1

                self.SeperatorNode = Node("'", parent=self.Content_Exp)

                self.parserBox.insert(str(self.parserOutput),"   seperator has child node (token):" + self.tokenTuple[1] + "\n")
                self.parserOutput += 1

                print("child node (internal): seperator")
                print("   seperator has child node (token):" + self.tokenTuple[1])
                self.accept_token()
            else:
                self.parserBox.insert(str(self.parserOutput),"expect Str_Literal at the first element of the expression!\n")
                self.parserOutput += 1

                print("expect keyword at the first element of the expression!\n")
                return
        elif(self.tokenTuple[0] == "Integer_Literal"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): int\n")
            self.parserOutput += 1

            self.Int_Node = Node("Integer_Literal", parent=self.Content_Exp)
            self.Int_Node_Val = Node(self.tokenTuple[1], parent=self.Int_Node)

            self.parserBox.insert(str(self.parserOutput), "   int has child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            print("child node (internal): int")
            print("   int has child node (token):" + self.tokenTuple[1])
            self.accept_token()
        elif(self.tokenTuple[0]=="Float_Literal"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): float\n")
            self.parserOutput += 1

            self.Float_Node = Node("Float Literal", parent=self.Content_Exp)
            self.Float_Node_Val = Node(self.tokenTuple[1], parent=self.Float_Node)

            self.parserBox.insert(str(self.parserOutput),"   float has child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            print("child node (internal): float")
            print("   float has child node (token):" + self.tokenTuple[1])
            self.accept_token()
        else:
            self.parserBox.insert(str(self.parserOutput), "error, content_exp expects float, int, or string literal \n")
            self.parserOutput += 1

            print("error, content expects float or int, or string literal")



    def if_exp(self):
        self.parserBox.insert(str(self.parserOutput),"----parent node if_exp, finding children nodes:\n")
        self.parserOutput +=1


        print("\n----parent node if_exp, finding children nodes:")
        typeT, token = self.tokenTuple;

        if (typeT == "Keyword"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): keyword\n")
            self.parserOutput += 1

            self.parserBox.insert(str(self.parserOutput), "     keyword has child node (token):" + token +"\n")
            self.parserOutput += 1

            #Add keyword to tree
            self.If_KeyWord = Node("Keyword", parent=self.If_Exp)
            self.If_KeyWord_Value = Node("If", parent=self.If_KeyWord)
            print("child node (internal): keyword")
            print("     keyword has child node (token):" + token)
            self.accept_token()

        else:
            self.parserBox.insert(str(self.parserOutput), "expect keyword at the first element of the expression!\n")
            self.parserOutput += 1

            print("expect keyword at the first element of the expression!\n")
            return

        if (self.tokenTuple[0] == "Seperator"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): seperator\n")
            self.parserOutput += 1

            #Add seperator to tree
            self.SeperatorNode = Node("(", parent=self.If_Exp)

            self.parserBox.insert(str(self.parserOutput),"   seperator has child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            print("child node (internal): seperator")
            print("   seperator has child node (token):" + self.tokenTuple[1])
            self.accept_token()
        else:
            self.parserBox.insert(str(self.parserOutput), "expect seperator as the first element of the expression!\n")
            self.parserOutput += 1

            print("expect seperator as the first element of the expression!\n")
            return

        self.parserBox.insert(str(self.parserOutput), "Child node (internal): comparison_exp\n")
        self.parserOutput += 1

        #Add comp_exp
        self.Comparision_Exp = Node("Comparison_Exp", parent=self.If_Exp)

        print("Child node (internal): comparison_exp")
        self.comparison_exp()

        if (self.tokenTuple[0] == "Seperator"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): seperator\n")
            self.parserOutput += 1

            # Add seperator to tree
            self.SeperatorNode = Node(")", parent=self.If_Exp)

            self.parserBox.insert(str(self.parserOutput),"   seperator has child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            print("child node (internal): seperator")
            print("   seperator has child node (token):" + self.tokenTuple[1])
            self.accept_token()
        else:
            self.parserBox.insert(str(self.parserOutput), "expect seperator as the first element of the expression!\n")
            self.parserOutput += 1

            print("expect seperator as the first element of the expression!\n")
            return



    def comparison_exp(self):
        self.parserBox.insert(str(self.parserOutput),"----parent node comparison_exp, finding children nodes:\n")
        self.parserOutput +=1

        print("\n----parent node comparison_exp, finding children nodes:")
        typeT, token = self.tokenTuple;

        if (self.tokenTuple[0] == "Identifier"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): identifier\n")
            self.parserOutput += 1

            #Add identifier to tree
            self.Id_Node = Node("Identifier", parent=self.Comparision_Exp)
            self.id_Value = Node(self.tokenTuple[1], parent=self.Id_Node)

            self.parserBox.insert(str(self.parserOutput), "   identifier has child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            print("child node (internal): identifier")
            print("   identifier has child node (token):" + self.tokenTuple[1])
            self.accept_token()
        else:
            self.parserBox.insert(str(self.parserOutput),"expect identifier as the first element of the expression!\n")
            self.parserOutput += 1

            print("expect identifier as the first element of the expression!\n")
            return

        if (self.tokenTuple[1] == ">"):
            self.parserBox.insert(str(self.parserOutput), "child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            self.Equiv_OP = Node(">", parent=self.Comparision_Exp)

            print("child node (token):" + self.tokenTuple[1])
            self.accept_token()
        else:
            self.parserBox.insert(str(self.parserOutput), "expect > as the second element of the expression!\n")
            self.parserOutput += 1

            print("expect = as the second element of the expression!\n")
            return

        if (self.tokenTuple[0] == "Identifier"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): identifier\n")
            self.parserOutput += 1

            # Add identifier to tree
            self.Id_Node = Node("Identifier", parent=self.Comparision_Exp)
            self.id_Value = Node(self.tokenTuple[1], parent=self.Id_Node)

            self.parserBox.insert(str(self.parserOutput), "   identifier has child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            print("child node (internal): identifier")
            print("   identifier has child node (token):" + self.tokenTuple[1])
            self.accept_token()
        else:
            self.parserBox.insert(str(self.parserOutput),"expect identifier as the first element of the expression!\n")
            self.parserOutput += 1

            print("expect identifier as the first element of the expression!\n")
            return


    def math_exp(self):
        self.parserBox.insert(str(self.parserOutput),"----parent node exp, finding children nodes:\n")
        self.parserOutput +=1

        print("\n----parent node exp, finding children nodes:")
        typeT, token = self.tokenTuple;

        if (typeT == "Keyword"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): keyword\n")
            self.parserOutput += 1

            #Add the Keyword node tree with child node
            self.KeyWord = Node("Keyword", parent=self.Math_Exp)
            self.Float = Node(token, parent=self.KeyWord)

            self.parserBox.insert(str(self.parserOutput), "     keyword has child node (token):" + token +"\n")
            self.parserOutput += 1

            print("child node (internal): keyword")
            print("     keyword has child node (token):" + token)
            self.accept_token()

        else:
            self.parserBox.insert(str(self.parserOutput), "expect keyword at the first element of the expression!\n")
            self.parserOutput += 1

            print("expect keyword at the first element of the expression!\n")
            return

        if (self.tokenTuple[0] == "Identifier"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): identifier\n")
            self.parserOutput += 1

            # Add ID node to Math_exp node
            self.identifier = Node("Identifier", parent=self.Math_Exp)
            self.idValue = Node(self.tokenTuple[1], parent=self.identifier)

            self.parserBox.insert(str(self.parserOutput), "   identifier has child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            print("child node (internal): identifier")
            print("   identifier has child node (token):" + self.tokenTuple[1])
            self.accept_token()
        else:
            self.parserBox.insert(str(self.parserOutput),"expect identifier as the first element of the expression!\n")
            self.parserOutput += 1

            print("expect identifier as the first element of the expression!\n")
            return

        if (self.tokenTuple[1] == "="):
            self.parserBox.insert(str(self.parserOutput), "child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            # Add ID node to Math_exp node
            self.equalOpNode = Node("=", parent=self.Math_Exp)

            print("child node (token):" + self.tokenTuple[1])
            self.accept_token()
        else:
            self.parserBox.insert(str(self.parserOutput), "expect = as the second element of the expression!\n")
            self.parserOutput += 1


            print("expect = as the second element of the expression!\n")
            return

        # Add ID node to Math_exp node
        self.Math_Node = Node("Math", parent=self.Math_Exp)

        self.parserBox.insert(str(self.parserOutput), "Child node (internal): math\n")
        self.parserOutput += 1

        print("Child node (internal): math")
        self.math()

    def math(self):
        self.parserBox.insert(str(self.parserOutput), "----parent node math, finding children nodes:\n")
        self.parserOutput += 1

        # Add multi node to math_exp node
        self.MultiNode = Node("Multi", parent=self.Math_Node)

        print("\n----parent node math, finding children nodes:")
        self.multi()

        if (self.tokenTuple[1] == "+"):
            self.parserBox.insert(str(self.parserOutput), "child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            #Add multi node to math_exp node
            self.AddNode = Node("+", parent=self.Math_Node)

            print("child node (token):" + self.tokenTuple[1])
            self.accept_token()

            self.parserBox.insert(str(self.parserOutput), "child node (internal): multi\n")
            self.parserOutput += 1

            # Add multi node to math_exp node
            self.MultiNode = Node("Multi", parent=self.Math_Node)

            print("child node (internal): multi")
            self.multi()
        else:
            self.parserBox.insert(str(self.parserOutput), "error, you need a + after multi in the math\n")
            self.parserOutput += 1

            print("error, you need a + after multi in the math")

    def multi(self):
        self.parserBox.insert(str(self.parserOutput), "----parent node multi, finding children nodes:\n")
        self.parserOutput += 1

        print("\n----parent node multi, finding children nodes:")
        if (self.tokenTuple[0] == "Float_Literal"):
            self.parserBox.insert(str(self.parserOutput), "child node (internal): float\n")
            self.parserOutput += 1

            # Add float node to multi node
            self.Float_Node = Node("float", parent=self.MultiNode)
            self.Float_Num_Node = Node(self.tokenTuple[1],parent=self.Float_Node)

            self.parserBox.insert(str(self.parserOutput), "   float has child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            print("child node (internal): float")
            print("   float has child node (token):" + self.tokenTuple[1])
            self.accept_token()

        elif (self.tokenTuple[0] == "Integer_Literal"):
            self.parserBox.insert(str(self.parserOutput),"child node (internal): int\n")
            self.parserOutput += 1

            # Add multi node to math_exp node
            self.Int_Node = Node("Integer", parent=self.MultiNode)
            self.Int_Num_Node = Node(self.tokenTuple[1], parent=self.Int_Node)

            self.parserBox.insert(str(self.parserOutput), "   int has child node (token):" + self.tokenTuple[1] + "\n")
            self.parserOutput += 1

            print("child node (internal): int")
            print("   int has child node (token):" + self.tokenTuple[1])
            self.accept_token()

            if (self.tokenTuple[1] == "*"):
                self.parserBox.insert(str(self.parserOutput),"child node (token):" + self.tokenTuple[1] + "\n")
                self.parserOutput += 1

                # Add multi op to multi node
                self.Mult_Op = Node("*", parent=self.MultiNode)

                print("child node (token):" + self.tokenTuple[1])
                self.accept_token()

                self.parserBox.insert(str(self.parserOutput), "child node (internal): multi\n")
                self.parserOutput += 1

                # Add multi node to multi node
                self.MultiNode = Node("Multi", parent=self.MultiNode)

                print("child node (internal): multi")
                self.multi()
            else:
                self.parserBox.insert(str(self.parserOutput), "error, you need + after the int in the math\n")
                self.parserOutput += 1

                print("error, you need + after the int in the math")
        else:
            self.parserBox.insert(str(self.parserOutput), "error, math expects float or int\n")
            self.parserOutput += 1

            print("error, math expects float or int")

    def accept_token(self):
        self.parserBox.insert(str(self.parserOutput), "     accept token from the list:" + self.tokenTuple[1] + "\n")
        self.parserOutput += 1

        print("     accept token from the list:" + self.tokenTuple[1])
        self.tokenTuple = self.Mytokens.pop(0)

if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = MyFirstGUI(myTkRoot)
    myTkRoot.mainloop()
