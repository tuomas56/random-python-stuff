def brain_luck(code, input):
    arr = [0]*1000
    dp = 0
    return evalbf(arr,dp,ast(code),input)
    
def evalbf(arr,dp,code,input):
    output = ""
    print(code)
    for cmd in code:
        if isinstance(cmd,list):
               while arr[dp]:
                   output += evalbf(arr,dp,cmd,input)
        else:
            if cmd == ",":
                arr[dp] = ord(input[0])
                print(chr(arr[dp]))
                input = str(input[1:])
                print(input)
            elif cmd == ".":
                output += chr(arr[dp])
            elif cmd == ">":
                dp += 1
            elif cmd == "<":
                dp -= 1
            elif cmd == "+":
                arr[dp] = (arr[dp] + 1) % 256
            elif cmd == "-":
                arr[dp] = (arr[dp] - 1) % 256
    return output
                   
  
def ast(code):
    astt = []
    while len(code):
        print(len(code),flush=True)
        print(code)
        if code[0] == "[":
            cc = ""
            i = 1
            depth = 1
            while depth:
                print("cc")
                cc += code[i]
                if code[i] == "[":
                    depth += 1
                elif code[i] == "]":
                    depth -= 1
                i += 1
            cc = cc[:-1]
            code = code[i:]
            astt.append(ast(cc))
        else:
            astt.append(code[0])
            code = code[1:]
    print("ast len:",len(astt),flush=True)
    return astt

print(brain_luck(",+[-.,+]",'hello'+chr(127)))