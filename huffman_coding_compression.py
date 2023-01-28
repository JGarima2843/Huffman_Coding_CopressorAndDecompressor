import heapq
import os

class BinaryTreeNode:
    def __init__(self,freq,value):
        self.freq=freq
        self.value=value 
        self.left=None
        self.right=None
    
    def __lt__(self,other):
        return self.freq<other.freq
    
    def __eq__(self,other):
        return self.freq==other.freq

        


class HuffmanCoding:
    def __init__(self,path):
        self.path=path
        self.__heap=[]
        self.__compressCodes={}
        self.__decompressCodes={}
        pass
    
    def __makeFrequencyDict(self,text):
        dict={}
        for char in text:
            if char in dict :
                dict[char]+=1
            else:
                dict[char]=1
        return dict


    def __buildHeap(self,freq_dict):
        # see the heap which we are creating is the heap of binary tree nodes so it does not work similar to min q
        # we have to specify on binarytree that on which basis oyr q should be made 
        # as we can see i have made two function __lt__ and __eq__ then on these two function basis out min q is made
        for keys in freq_dict:
            freq=freq_dict[keys]
            node=BinaryTreeNode(freq,keys)
            heapq.heappush(self.__heap,node)
    

    def __buildTree(self):
        while len(self.__heap)>1:
            node1=heapq.heappop(self.__heap)
            heapq.heapify(self.__heap)
            node2=heapq.heappop(self.__heap)

            freq=node1.freq+node2.freq
            newNode=BinaryTreeNode(freq,None)
            heapq.heappush(self.__heap,newNode)

            newNode.left=node1 
            newNode.right=node2 
            heapq.heapify(self.__heap)
        
        return 


    def __buildCompressCharCodes(self,root,currBit):
        if root is None:
            return 
        
        if root.value is not None:
            #🧑🏽‍⚖️🎯 if the value of the node is not None -->it means it the node which contains the char to encode and we have the bits string along with us 
            # so we are just filling the encoded bits corresponding to that char in compressCodes array
            # and also if the node contains value then it is a leaf node so we have to return it from here
            self.__compressCodes[root.value]=currBit
            self.__decompressCodes[currBit]=root.value
            return 
        
        self.__buildCompressCharCodes(root.left,currBit+"0")
        self.__buildCompressCharCodes(root.right,currBit+"1")

    
    def __buildCodes(self):
        root=heapq.heappop(self.__heap)
        self.__buildCompressCharCodes(root,"")

    def __TextEncoder(self,text):
        encodedText=""
        for char in text:
            code=self.__compressCodes[char]
            encodedText+=code
        
        return encodedText
    
    def __binaryTextPadding(self,encodedText):

        paddingAmount=8-(len(encodedText)%8)

        for i in range(paddingAmount):
            encodedText+="0"

        # "{0:0b}" in this first arg tells the the amount to be converted in the specified and the second 0b args tells t convert the amount in binary format in the base2
        
        padded_amount_info="{0:0b}".format(paddingAmount)

        paddedBinaryCode=padded_amount_info+encodedText
        return paddedBinaryCode
    

    def __getBinaryCodeArray(self,encodedText):
        binaryArray=[]
        for i in range(0,len(encodedText),8):
            byte=encodedText[i:i+8]
            # print(byte,int(byte),int(byte,2))
            binaryArray.append(int(byte,2))  #🧑🏽‍⚖️👯 this 2 argument is the byte is a string hence firstly byte-->int and that int is of base 10 but we want that it should be binary of base 2
        
        return binaryArray
    

    def __RemovePadding(self,bit_string):
        padded_info=bit_string[:8]
        extra_padding_amount=int(padded_info,2)

        text=bit_string[8:]
        text_after_removing_padding=text[:(-1)*extra_padding_amount]
        return text_after_removing_padding
    

    def __Get_decompress_text(self,text):
        deCompressed_code=""
        curr_bit=""

        for char in text:
            curr_bit+=char 
            if curr_bit in self.__decompressCodes:
                deCompressed_code+=self.__decompressCodes[curr_bit]
                curr_bit=""
            
        return deCompressed_code
    





    def compress(self):
        # path is the path of the file which we want to compress 
        file_Name,file_extension=os.path.splitext(self.path)
        output_path=file_Name+".bin"
        # reading the file 

        with open(self.path,'r+') as file ,open (output_path,'wb') as output: #🙏🏽✅⬇️opened the file in r+ mode means read/write mode as file and also opened the output file in wb means write in binary  mode as output

            text=file.read()
            text=text.rstrip() #for removing the spaces

            #STEP:1) making the frequency dictionary if the characters encountered in file

            freq_dict=self.__makeFrequencyDict(text)
            # print(freq_dict) ## just for testing
            
            # ---------------------------------------------------------------------------------------------

            #STEP:2) constructing the heap from the frequency dictionary in order to find the minimum occurring character first
            self.__buildHeap(freq_dict)
            # MOST MOST MOST IMPORTANT CONCEPT IN THIS 🍨🍨🍔 MUST HAVE A LOOK BEFORE GOING AHEAD 
            # -----------🦐🦐------->have a look upon what is inside the this heap you will get clarity----🐞🐞-----------------------
            # heapq.heapify(self.__heap)
            # print(self.__heap[0].value,self.__heap[0].freq)
            
            # -----------------------------------------------------------------------------------------------------


            #STEP:3) constructing the Binary tree from the heap minimum character frequency
            self.__buildTree()
            # ----------🐞print this to have better understanding🐞-----------
            # print(self.__heap[0].freq,self.__heap[0].value)

            # -------------------------------------------------------------------------------------------------------



            #STEP:4) constructs the codes from binary tree--->"010101"

            self.__buildCodes()
            # print(self.__compressCodes)  # just for testing

            # -----------------------------------------------------------------------------------------------------------


            #STEP:5) constructing the encoded text from the generated code 

            encodeText=self.__TextEncoder(text)
            # print(encodeText)  # just for testing

            # STEP:6) Padding the encodedText 
            # this step is for this case the you whole binary string is properly distributed in 8bit pairs so just t distribute this properly 
            # we are using the padding so that first 8 bit contains info about hw much bits are padded 
            # and this first 8 bits are padded at the last 

            encodeText=self.__binaryTextPadding(encodeText)
            # print("here is the padded text")
            # print(encodeText)   # just for testing


            # -----------------------------------------------------------------------------------------------------------

            # STEP:7) now putting the bytes in the array that in 1byte=8bite  so making the 1 element by converting the 8bit string in the bits
            Binary_codes_Array=self.__getBinaryCodeArray(encodeText)
            # print(Binary_codes_Array)   # just for testing

            Final_Byte_Array=bytes(Binary_codes_Array) # 👀👀 converted into bytes array 
            # print(Final_Byte_Array)  # just for testing
            

            # ---------------------------------------------------------------------------------------------------------------
            #STEP:8) putting this encoded text into the binary file
            output.write(Final_Byte_Array)
            print("file compressed !! 🥳🍾")

            #STEP:7) return the binary file as output
            return output_path
    

    def Decompressor(self,input_path):
        fileName,fileExtension=os.path.splitext(self.path)
        output_path=fileName+"_decompressed"+".txt"
        # STEP:1) reading binary data from the input file and converting this into binary string 
        with open(input_path,'rb') as file ,open(output_path,'w') as output:
            bit_String=""
            byte=file.read(1)
            while byte:
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,'0')  #🚨🚨 b'101==>[2:]=101==>(8,0)=00000101
                bit_String+=bits
                byte=file.read(1)
            #STEP:2)removing the extra padding from the binary string 
            actual_binary_String=self.__RemovePadding(bit_String)
            # print(actual_binary_String)
            print(self.__decompressCodes)

            #STEP:3)Decoding the actual_binary_string to actual file
            decoded_text=self.__Get_decompress_text(actual_binary_String)
            # print(decoded_text)

            #STEP:4)Writing the decoded text in output file and saving
            output.write(decoded_text)
            print("Decompressed the file !! 🥂💯🚨")










path="C:\\Users\\HP\\Dropbox\\My PC (LAPTOP-H4TETKF0)\\Downloads\\sample-2mb-text-file.txt"
file=HuffmanCoding(path)
output_path=file.compress()
print("output file path :: ",output_path)
file.Decompressor(output_path)
