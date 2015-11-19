'''
Created on 2011-10-26

@author: michael
'''
import math

class ContractCalculationException(Exception):
    pass


class ContractCalculator(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.valueTable = {}
    
    def buildValueTable(self, contractName, start, end):
        
        if(contractName not in ['ABBN', 'AXT', 'AYT', 'XT', 'YT', 'IR']):
            raise ContractCalculationException("contract not supported Exception");
        
        price = start;
        if(contractName in ['ABBN','IR']):            
            self.valueTable['ABBN'] = {};
            while(price <= end):
                self.valueTable['ABBN'][round(price,2)] = self.calculateIRValue(price);
                price = price + 0.01;
         
        if(contractName in ['AXT','XT']):
            self.valueTable['AXT'] = {};
            while(price <= end):
                self.valueTable['AXT'][round(price,3)] = self.calculateXTValue(price);
                price = price + 0.005;       
        
        if(contractName in ['AYT','YT']):
            self.valueTable['AYT'] = {};
            while(price <= end):
                self.valueTable['AYT'][round(price,3)] = self.calculateYTValue(price);
                price = price + 0.005;
    
    def getContractValue(self, contractName, price):
        if(contractName not in self.valueTable):
            raise ContractCalculationException("contract not supported Exception:contract:%s"%contractName);
        
        if(price not in self.valueTable[contractName]):
            raise ContractCalculationException("invalid price Exception: contract:%s,price:%s"%(contractName,price));
        value = self.valueTable[contractName][price];
        return value;
    
    def calculateIRValue(self, price):
        if(price > 100):
            raise ContractCalculationException("invalid price, price cannot larger than 100.00");
        # Below is the calculation method by ASX
        A = 100 - price;
        B = A * 0.9
        C = B + 365
        D = 1000000 * 365
        E = round(float(D / C), 2);
        return E;
        
    def calculateXTValue(self, price):
        if(price > 100):
            raise ContractCalculationException("invalid price, price cannot larger than 100.00");
        # Below is the calculation method by ASX
        A = float(100 - price);
        B = A / 200;
        C = round(1 / (1 + B), 8);
        D = round(math.pow(C, 20), 8);
        E = 1 - D;
        F = 3 * E;
        G = round(F / B, 8);
        H = 100 * D;
        I = G + H;
        J = I * 1000;
        K = round(J, 2);
        return K;
    
    def calculateYTValue(self, price):
        if(price > 100):
            raise ContractCalculationException("invalid price, price cannot larger than 100.00");
        # Below is the calculation method by ASX
        A = float(100 - price);
        B = A / 200;
        C = round(1 / (1 + B), 8);
        D = round(math.pow(C, 6), 8);
        E = 1 - D;
        F = 3 * E;
        G = round(F / B, 8);
        H = 100 * D;
        I = G + H;
        J = I * 1000;
        K = round(J, 2);
        return K;
        
        
    
    
        
