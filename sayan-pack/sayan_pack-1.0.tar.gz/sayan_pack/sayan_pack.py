import mat
class Poly:
    def __init__(self):
        self.res = 0
        
    def collect_data(self,degree):
        i=0
        data = []
        while i <= degree:
            met = float(input('Enter value:'))
            data.append(met) 
            i += 1
        
        return data
    def calc_horner_methd(self):
        poly = self.collect_data(int(input('Enter PValue :')))
        n = len(poly)
        x = int(input("enter x: ")) 
        result = poly[0]
        for i in range(1,n):
            result = (result*x) + poly[i]
        
        return result
    
    def calc_mean(self):
        data = self.collect_data(int(input('Enter PValue :')))
        sum = 0
        for d in data:
           sum += d
        avg = 1.0 * sum / len(data)
        return avg

    def pascal_triangle(self, x):
        
        l =[1]
        for i in range(x):
            print 
            newl=[]
            newl.append(l[0])
            for i in range(len(l)- 1):
                newl.append(l[i]+ l[i+1])
            newl.append(l[-1])
            l = newl
        return l
    