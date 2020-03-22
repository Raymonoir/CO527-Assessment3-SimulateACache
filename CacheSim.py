import math
#Author: Raymond Ward
#Function to read all files, must be placed in folder named 'inputs' on same level as script
def readFiles ():
        for i in range(20):
            filename = str(i).zfill(2) + "-rw468.in"
            f = open("inputs/"+ filename, "r")

            inputs = []
            values = []

            fileLines = f.readlines()

            for j in range(len(fileLines)):
                if j == 0:
                    values = fileLines[j].split()
                else:
                    inputs.append(int(fileLines[j]))
            f.close()
            print('File Number: ' ,i)
            C = CacheSim(int(values[0]),int(values[1]),int(values[2]),int(values[3]), inputs)
            

#Class to perform the address organising and LRU replacement
class CacheSim:
    def __init__(self,W,C,B,K,inputs):
        self.W = W
        self.C = C
        self.B = B
        self.K = K
        self.inputs = inputs
        self.answer = ""
        

        blocks = self.C / self.B
        self.indexLength = math.log2(blocks)
        bytesInLine = self.B / self.K
        self.offsetLength = math.log2(bytesInLine)

        #Dictionary to store cache for each index
        self.indexCache = {}

        self.accessCache()
        print("Answer: " + self.answer + "\n")

    #TAG INDEX OFFSET
    #This function coverts inputs into binary, removes offset, and calls LRU replacement on each address
    def  accessCache (self):
        singleCache = []
        
        #Loops through all inputs
        for i in range(len(self.inputs)):
            self.inputs[i] = str(int(bin(self.inputs[i])[2:])) #decimal to binary to string
            self.inputs[i] = self.inputs[i].zfill(self.W) #fills extra zeros
            self.inputs[i] = self.inputs[i][:int(len(self.inputs[i]) - self.offsetLength)] #removes offset
            index = self.inputs[i][int(len(self.inputs[i]) - self.indexLength) : int(len(self.inputs[i]))] #gets index
            tag = self.inputs[i][0: int(len(self.inputs[i]) - self.indexLength)] #gets tag

            #If index = 0 all addresses are handled together
            if (len(index) == 0):
                self.doLRUReplacement(tag,singleCache)
            else:
                if index not in self.indexCache:
                    self.indexCache[index] = []

                self.doLRUReplacement(tag,self.indexCache[index])

    #Function to perform LRU replacement
    def doLRUReplacement (self,value,cache):
        if value in cache:
            indexOfHit = cache.index(value)
            holder = cache[indexOfHit]
            cache.pop(indexOfHit)
            cache.append(holder)
            self.answer+="C"
        else:
            if len(cache) < self.K:
                cache.append(value)
            else:
                cache.pop(0)
                cache.append(value)
            self.answer+="M"

if __name__ == "__main__":
    readFiles()



