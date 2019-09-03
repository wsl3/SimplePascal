
class Token(object):
    def __init__(self, tokenType, tokenValue):
        self.tokenType = tokenType
        self.tokenValue = tokenValue
    def __str__(self):
        return f"Token<{self.tokenType,  self.tokenValue}>"
    __repr__ = __str__

class TokenType(object):
    pass


class Lex(object):
    def __init__(self, readpath):
        self.readpath = readpath
        self.tokens = []
        self.source = self._getInputString()
        self.index = 0 # 指向源代码的当前字符
        self.binaryOp = ["+", "-", "*", "/"]
        self.number = [str(i) for i in range(10)]
        self.identify = [chr(i) for i in range(97,123)] + [chr(i) for i in range(65,91)] + ["_"]
        self.keyWords = ["VAR", "PROGRAM", "integer","BEGIN","END"] 



    def tokenize(self):
        char = self._nextChar()
        while(char != None):
            if(char == "\n" or char == "\t" or char == " "):
                char = self._nextChar()
                continue
            elif(char == "{"):
                char = self._nextChar()
                while(char != "}"):
                    char = self._nextChar()
                char = self._nextChar()
            elif(char == ":"):
                nextchar = self._nextChar()
                if(nextchar == "="):
                    res = char + nextchar
                    self.tokens.append(Token("赋值", res))
                    char = self._nextChar()
                else:
                    char = nextchar
            elif(char == ";"):
                self.tokens.append(Token("分号", char))
                char = self._nextChar()
            elif(char == ","):
                self.tokens.append(Token("逗号", char))
                char = self._nextChar()
            elif(char == "."):
                self.tokens.append(Token("小数点", "."))
                char = self._nextChar()
            elif(char in self.binaryOp):
                self.tokens.append(Token("BinaryOp", char))
                char = self._nextChar()
            elif(char in self.number):
                res = int(char)
                char = self._nextChar()
                while(char in self.number):
                    res = res*10 + int(char)
                    char = self._nextChar()
                self.tokens.append(Token("整数", res))
            elif(char in self.identify):
                res = char
                char = self._nextChar()
                while(char in self.identify):
                    res += char 
                    char = self._nextChar()
                # 判断该标识符是否是关键字
                if(res in self.keyWords):
                    self.tokens.append(Token("关键字", res))
                else:
                    self.tokens.append(Token("标识符", res))
            else:
                print(f"出现未识别符号:\t{char}")
                raise Exception("出现未识别Token!")

        return self.tokens
                

    def _getInputString(self):
        with open(self.readpath, "r", encoding="utf8") as f:
            res = f.read()
            return res
    
    def _nextChar(self):
        if(self.index < len(self.source)):
            res = self.source[self.index]
            self.index += 1
            return res
        return None


def test():
    yield 1
    yield 2


if __name__ == "__main__":
    lex = Lex("./source.pas")
    tokens = lex.tokenize()
    for token in tokens:
        print(token)