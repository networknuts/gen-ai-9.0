def add_together(n1,n2):
    return(n1+n2)

def userinfo(name,location):
    return [{
        "user": name.upper(),
        "location": location.upper()
    }]

result = userinfo("Salina","India")
print(result)