'''
Created on 2011-3-1

@author: michael
'''

import tradeutils as tu;
import sqlite3, time, datetime, os, re

class Filter(object):
    def __init__(self):
        self.account = None;
        self.product = None;
        self.exchange = None;
        self.buy_sell = None;
        self.start_time = None;
        self.end_time = None;
        self.source_id = None;
        self.quantity = None;
        self.price = None;



class TradeDB(object):
    '''
    classdocs
    '''
    def __init__(self, sqlite_file):
        '''
        Constructor
        '''
        self.connect = None;
        self.dbFile = sqlite_file;
    
    def openDB(self):
        self.connect = sqlite3.connect(self.dbFile);
    
    def closeDB(self):
        self.connect.close();    
    
    def loadRecordsToDB(self, records, file_name):
        cursor = self.connect.cursor();
#        seq = 0;
        try:
            # 1. get next seq for source_id
            sql = 'update seq set seq=seq+1 where name="source_id"';
            cursor.execute(sql);
            sql = 'select seq from seq where name="source_id"';
            rows = cursor.execute(sql);
            seq = rows.fetchone()[0];
            
            # 2. load trading records into table
            for record in records:
                time_str = record.datetime.strftime('%Y-%m-%d %H:%M:%S');
                entry = (record.account, record.product, record.exchange, record.bought_sold, record.price, record.quantity, time_str, record.currency, seq);
                sql = 'insert into trade_record(account,product,exchange,buy_sell,price,quantity,trade_time,currency,source_id) values(?,?,?,?,?,?,?,?,?)';
                cursor.execute(sql, entry);
            
            #3. add file log information into table
            sql = 'insert into file_log(source_id,file_name,load_time) values(?,?,?)'
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            entry = (seq, file_name, time_str);
            cursor.execute(sql, entry);            
            self.connect.commit();
        except Exception  as e:
            print e.args 
            self.connect.rollback();
        return seq;
    
    def addNewTradeRecord(self, record):
        cursor = self.connect.cursor();
        try:
            entry = (record.account, record.product, record.exchange, record.bought_sold, record.price, record.quantity, record.datetime, 0);
            sql = 'insert into trade_record(account,product,exchange,buy_sell,price,quantity,trade_time,source_id) values(?,?,?,?,?,?,?,?)';
            cursor.execute(sql, entry);
            self.connect.commit();
        except:
            print "error!"
            self.connect.rollback();
    
    def loadRTSRecords(self, rts_file):
        records = tu.get_rts_trade_records(rts_file, enable_header=True);
        self.loadRecordsToDB(records, rts_file);
    
    def loadASAPRecords(self, asap_file):
        records = tu.get_asap_trade_records(asap_file);
        self.loadRecordsToDB(records, asap_file);
    
    def loadTTRecords(self, tt_file):
        records = tu.get_tt_trade_records(tt_file);
        self.loadRecordsToDB(records, tt_file);
            
    def unloadRecords(self, source_id):
        cursor = self.connect.cursor();
        try:
            
            sql = 'delete from trade_record where source_id = ?';
            cursor.execute(sql, (source_id,));
            self.connect.commit();
        except:
            print "error!"
            self.connect.rollback();
    
    def getRecords(self, filter):
        
        records = [];
        sql = 'select * from trade_record where 1=1 ';
        if(filter.account is not None):
            sql += 'and account like \'%' + filter.account + '%\' ';
        
        if(filter.product is not None):
            sql += 'and product like \'%' + filter.product + '%\' ';
        
        if(filter.exchange is not None):
            sql += 'and exchange like \'%' + filter.exchange + '%\' ';
            
        if(filter.buy_sell is not None):
            sql += 'and buy_sell="%s" ' % filter.buy_sell;
        
        if(filter.start_time is not None):
            sql += 'and trade_time>\'%s\' ' % filter.start_time.strftime('%Y-%m-%d %H:%M:%S');
            
        if(filter.end_time is not None):
            sql += 'and trade_time<\'%s\' ' % filter.end_time.strftime('%Y-%m-%d %H:%M:%S');
            
        if(filter.source_id is not None):
            sql += 'and source_id=%d ' % filter.source_id;
        
        if(filter.quantity is not None):
            sql += 'and quantity=%d ' % filter.quantity;
            
        if(filter.price is not None):
            sql += 'and price=%s ' % filter.price;
            
        print sql;
        cursor = self.connect.cursor();
        try:
            rs = cursor.execute(sql);
            rows = rs.fetchall();
            for row in rows:
                (acc, prod, exchange, bs, ts, qty, price, src_id, currency) = row;
                rec = tu.TradeRecord();
                rec.account = acc;
                rec.product = prod;
                rec.exchange = exchange;
                rec.bought_sold = bs;
                rec.datetime = datetime.datetime.strptime(ts,'%Y-%m-%d %H:%M:%S');
                rec.quantity = qty;
                rec.price = price;
                rec.currency = currency;
                records.append(rec);
        except:
            print "error";
            
        return records;
    
    def getSRCFileNames(self,filter):
        file_names = [];
        sql = 'select distinct source_id from trade_record where 1=1 ';
        if(filter.account is not None):
            sql += 'and account like \'%' + filter.account + '%\' ';
        
        if(filter.product is not None):
            sql += 'and product like \'%' + filter.product + '%\' ';
        
        if(filter.exchange is not None):
            sql += 'and exchange like \'%' + filter.exchange + '%\' ';
            
        if(filter.buy_sell is not None):
            sql += 'and buy_sell="%s" ' % filter.buy_sell;
        
        if(filter.start_time is not None):
            sql += 'and trade_time>\'%s\' ' % filter.start_time.strftime('%Y-%m-%d %H:%M:%S');
            
        if(filter.end_time is not None):
            sql += 'and trade_time<\'%s\' ' % filter.end_time.strftime('%Y-%m-%d %H:%M:%S');
            
        if(filter.source_id is not None):
            sql += 'and source_id=%d ' % filter.source_id;
        
        if(filter.quantity is not None):
            sql += 'and quantity=%d ' % filter.quantity;
            
        if(filter.price is not None):
            sql += 'and price=%s ' % filter.price;
            
        
        sql= 'select file_name from file_log where source_id in (%s)'%sql;
        print sql;
        cursor = self.connect.cursor();
        try:
            rs = cursor.execute(sql);
            rows = rs.fetchall();
            for row in rows:
                (filename,) = row;
                file_names.append(filename);
        except:
            print "error";
            
        return file_names;
        
    
    
    def getRecordsByAccount(self, account):
        f = Filter();
        f.account = account;
        return self.getRecords(f);
    
    def getFileLog(self, start=None, end=None):
        
        if(start is None):
            start = 0;
        
        if(end is None):
            end = int(time.time());
       
            
        catch_list = [];
        cursor = self.connect.cursor();
        
        
        # ASAP file
        sql = "select file_name from file_log where file_name like '%asap%'"
        rs = cursor.execute(sql);
        rows = rs.fetchall();
        for row in rows:
            (filepath,) = row;
            filename = os.path.basename(filepath);
            datestamp = re.findall('asap_(\d{8})\.csv', filename);
            ts = int(time.mktime(time.strptime(datestamp[0], '%Y%m%d')));
            if(ts > start and ts < end):
                catch_list.append(filename);
                
        
        # RTS file
        sql = "select file_name from file_log where file_name like '%rtdexport%'"
        rs = cursor.execute(sql);
        rows = rs.fetchall();
        for row in rows:
            (filepath,) = row;
            filename = os.path.basename(filepath);
            datestamp = re.findall('.*rtdexport\.trade\.(\d{8})', filename);
            ts = int(time.mktime(time.strptime(datestamp[0], '%Y%m%d')));
            if(ts > start and ts < end):
                catch_list.append(filename);
        
        
        # TT File
        sql = "select file_name from file_log where file_name like '%Details%'"
        rs = cursor.execute(sql);
        rows = rs.fetchall();
        for row in rows:
            (filepath,) = row;
            filename = os.path.basename(filepath);
            datestamp = re.findall('.*_Export_(\d{4}_\d{2}_\d{2})_.*', filename);
            ts = int(time.mktime(time.strptime(datestamp[0], '%Y_%m_%d')));
            if(ts > start and ts < end):
                catch_list.append(filename);
        
        return catch_list;
    
    
    
class MFGTradeDB(object):
    def __init__(self, sqlite_file):
        '''
        Constructor
        '''
        self.connect = None;
        self.dbFile = sqlite_file;
    
    def openDB(self):
        self.connect = sqlite3.connect(self.dbFile);
    
    def closeDB(self):
        self.connect.close();    
                
    def loadRecordsToDB(self, records, ops, file_name):
        cursor = self.connect.cursor();
        
        try:
            # 1. get next seq for source_id
            sql = 'update seq set seq=seq+1 where name="source_id"';
            cursor.execute(sql);
            sql = 'select seq from seq where name="source_id"';
            rows = cursor.execute(sql);
            seq = rows.fetchone()[0];
            
            # 2. load trading records into table
            for record in records:
                entry = (record.account, record.product, record.currency, record.commission, record.gst, record.mfgdate, record.exchange, record.bought_sold, record.price, record.quantity, seq);
                sql = 'insert into trade_record(account,product,currency, commission, gst, trade_date, exchange, buy_sell,price,quantity,source_id) values(?,?,?,?,?,?,?,?,?,?,?)';
                cursor.execute(sql, entry);
            
            
            # 3. load open positions
            trade_date = records[0].mfgdate
            for op in ops:
                entry = (op.account, op.product, op.price, op.quantity, trade_date, seq);
                sql = 'insert into open_position(account,product,price,quantity,trade_date, source_id) values(?,?,?,?,?,?)';
                cursor.execute(sql, entry);
            
            
            # 4. add file log information into table
            sql = 'insert into file_log(source_id,file_name,load_time) values(?,?,?)'
            entry = (seq, file_name, int(time.time()));
            cursor.execute(sql, entry);            
            self.connect.commit();
        except Exception  as e:
            print e.args 
            self.connect.rollback();
        return seq;
    
    def loadMFGRecords(self,mfg_file):
        return tu.get_mfg_trade_records(mfg_file);
    
    def loadMFGOpenPositions(self,mfg_file):
        return tu.get_open_positions(mfg_file);
        
    def getMFGRecords(self, account=None,product=None,start_date=None,end_date=None):
        records = [];
        sql = 'select * from trade_record where 1=1'
        
        if(account is not None):
            sql += ' and account=\'%s\''%account;
          
        if(product is not None):
            sql += ' and product=\'%s\''%product;
            
        if(start_date is not None):
            sql += ' and trade_date>=\'%s\''%start_date;
            
        if(end_date is not None):
            sql += ' and trade_date<=\'%s\''%end_date;
        
        print sql;
        cursor = self.connect.cursor();
        try:
            rs = cursor.execute(sql);
            rows = rs.fetchall();
            for row in rows:
                (acc, prod, exchange, bs, trade_date, qty, price, comm, gst, currency, src_id) = row;
                rec = tu.TradeRecord();
                rec.account = acc;
                rec.product = prod;
                rec.exchange = exchange;
                rec.bought_sold = bs;
                rec.mfgdate = str(trade_date);
                rec.quantity = qty;
                rec.price = price;
                rec.commission = comm;
                rec.gst = gst;
                
                # this is hard coded for now
                if(rec.product == "SNK"):
                    rec.currency = "JPY";
                    rec.fee_currency = "USD"
                else:
                    rec.currency = currency;
                    rec.fee_currency = currency;
                
                
                records.append(rec);
        except:
            print "error";
            
        return records;
        
    def getOpenPosition(self,account=None,product=None,date=None):
        records = [];
        sql = 'select account, product, quantity, price from open_position where 1=1'
        
        if(account is not None):
            sql += ' and account=\'%s\''%account;
          
        if(product is not None):
            sql += ' and product=\'%s\''%product;
            
        if(date is not None):
            sql += ' and trade_date=\'%s\''%date;
        
        print sql;
        
        cursor = self.connect.cursor();
        try:
            rs = cursor.execute(sql);
            rows = rs.fetchall();
            
            for row in rows:
                (acc,prod,qty,price) = row
                rec = tu.OpenPosition();
                rec.account = acc;
                rec.product = prod;
                rec.quantity = qty;
                rec.price = price;
                records.append(rec);
        except:
            print "error";
        return records;
    
    
    def getOpenPositions(self,account=None,product=None,start_date=None, end_date=None):
        records = [];
        sql = 'select account, product, quantity, price, trade_date from open_position where 1=1'
        
        if(account is not None):
            sql += ' and account=\'%s\''%account;
          
        if(product is not None):
            sql += ' and product=\'%s\''%product;
            
        if(start_date is not None):
            sql += ' and trade_date>=\'%s\''%start_date;
            
        if(end_date is not None):
            sql += ' and trade_date<=\'%s\''%end_date;
        
        print sql;
        
        cursor = self.connect.cursor();
        try:
            rs = cursor.execute(sql);
            rows = rs.fetchall();
            
            for row in rows:
                (acc,prod,qty,price, date) = row
                rec = tu.OpenPosition();
                rec.account = acc;
                rec.product = prod;
                rec.quantity = qty;
                rec.price = price;
                rec.date = str(date);
                records.append(rec);
        except:
            print "error";
        return records;
    
#    def getAllAccounts(self):
#        accs = [];
#        sql = 'select distinct account from trade_record';
#        print sql;
#        cursor = self.connect.cursor();
#        
#        try:
#            rs = cursor.execute(sql);
#            rows = rs.fetchall();            
#            for row in rows:
#                (acc) = row
#                accs.append(acc);
#        except:
#            print "error";
#        return accs;
#    
#    
#    def getAllProductsPerAccount(self,account):
#        products = [];
#        sql = 'select distinct product from trade_record where account = ?';
#        print sql;
#        cursor = self.connect.cursor();
#        
#        try:
#            acc = (account,)
#            rs = cursor.execute(sql,acc);
#            rows = rs.fetchall();            
#            for row in rows:
#                (product) = row
#                products.append(product);
#        except:
#            print "error";
#        return products;
