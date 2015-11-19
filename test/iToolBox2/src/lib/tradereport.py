'''
Created on 2011-3-29

@author: michael
'''
import trade_db as tdb;
import tradeutils as tu;
import commonutils as cutils;
import datetime



class PLReport(object):
    '''
    classdocs
    '''
    def __init__(self, start_date, end_date, db_file):
        '''
        Constructor
        '''
        self.db = tdb.MFGTradeDB(db_file);
        self.startDate = start_date;
        self.endDate = end_date;
        self.tradeRecords = [];
        self.accounts = [];
        # open positions
        self.ops = [];
        pass
    
    def loadTradeRecordsFromDB(self):
        self.db.openDB();
        self.tradeRecords = self.db.getMFGRecords(start_date=self.startDate, end_date=self.endDate);
        # load open position from the previous day
        
        p_date = cutils.last_work_day(self.startDate);
        self.ops = self.db.getOpenPositions(start_date=p_date, end_date=self.endDate)
        self.db.closeDB();
    
    
    def getAllAccounts(self):
        for record in self.tradeRecords:
            if(record.account in self.accounts):
                continue;
            else:
                self.accounts.append(record.account);
                
        self.accounts = sorted(self.accounts);
        return self.accounts;
     
    
    def getAccountSummaries(self, account, date):
        assert type(date) == datetime.datetime;
        
        date_str = date.strftime('%Y%m%d');
        # 1 get trade records
        records = [];
        for record in self.tradeRecords:
            if(record.account == account and record.mfgdate == date_str):
                records.append(record);
        if(len(records) == 0):
            return [];       
        
        # 2 get open positions
        l_date = cutils.last_work_day(date_str)
        start_positions = [];
        end_positions = [];
        for op in self.ops:
            if(op.account == account and op.date == l_date):
                start_positions.append(op);
            elif(op.account == account and op.date == date_str):
                end_positions.append(op)
            else:
                continue
            
        #3. generate summaries
        sorted_records = tu.sort_trade_records(records);
        summaries = tu.make_account_product_summary(sorted_records, MFG=True);
        summaries = tu.merge_with_start_open_positions(summaries, start_positions);
        summaries = tu.merge_with_open_positions(summaries, end_positions);
        return summaries;
                
    
    def getTradeSummaries(self, date, account=None, product=None, MFG=True):
        assert type(date) == datetime.datetime;
        
        date_str = date.strftime('%Y%m%d');
        # 1 get trade records
        records = [];
        for record in self.tradeRecords:
            if(record.mfgdate != date_str):
                continue;
            
            if(account is not None and record.account != account):
                continue;
            
            if(product is not None and record.product != product):
                continue;
            
            records.append(record);
        
        if(len(records) == 0):
            return []; 
        
        
        # 2 get open positions
        l_date = cutils.last_work_day(date_str)
        start_positions = [];
        end_positions = [];
        for op in self.ops:
            if(op.date == l_date):
                if(account is not None and op.account != account):
                    continue;
                if(product is not None and op.product != product):
                    continue;
                start_positions.append(op);
            elif(op.date == date_str):
                if(account is not None and op.account != account):
                    continue;
                if(product is not None and op.product != product):
                    continue;
                end_positions.append(op)
            else:
                continue
        
        #3. generate summaries
        sorted_records = tu.sort_trade_records(records);
        summaries = tu.make_account_product_summary(sorted_records, MFG=MFG);
        summaries = tu.merge_with_start_open_positions(summaries, start_positions);
        summaries = tu.merge_with_open_positions(summaries, end_positions);
        return summaries;
    
    
    def getOverallTradingSummaries(self, MFG=True):
        
        # get open positions
        start_date = cutils.last_work_day(self.startDate)
        start_positions = [];
        end_positions = [];
        for op in self.ops:
            if(op.date == start_date):
                start_positions.append(op);
            elif(op.date == self.endDate):
                end_positions.append(op)
            else:
                continue
        
        # generate overall summary
        sorted_records = tu.sort_trade_records(self.tradeRecords);
        summaries = tu.make_account_product_summary(sorted_records, MFG=MFG);
        summaries = tu.merge_with_start_open_positions(summaries, start_positions);
        summaries = tu.merge_with_open_positions(summaries, end_positions);
        return summaries;
    
            
    
    def getOpenPositionFromCache(self, account, product, date):
        records = []
        for op in self.ops:
            if(op.date == date):
                tmp = tu.OpenPosition();
                tmp.account = account;
                tmp.product = product;
                if(tu.is_same_account_product(op, tmp)):
                    records.append(op);           
        return records;
     
                    
    
    def getAccountProductDateSummary(self, account, product, date, MFG=True):
        assert type(date) == datetime.datetime
        records = [];
        date_str = date.strftime('%Y%m%d');
        for record in self.tradeRecords:
            if(record.account == account and record.product == product and record.mfgdate == date_str):
                records.append(record);
        if(len(records) == 0):
            return [];
        
        sorted_records = tu.sort_trade_records(records);
        summaries = tu.make_account_product_summary(sorted_records, MFG=MFG);
        # get open positions
        # previous working day
        l_date = cutils.last_work_day(date_str)
        start_position = self.getOpenPositionFromCache(account, product, l_date);                
        end_position = self.getOpenPositionFromCache(account, product, date_str);       
        summaries = tu.merge_with_start_open_positions(summaries, start_position);
        summaries = tu.merge_with_open_positions(summaries, end_position)
        return summaries;
         
    
    def buildReportTable(self, account, MFG=True):   
        #####################################################
        # 1. get all prodcuts name for this account
        ####################################################
        products = [];
        for record in self.tradeRecords:
            if(record.account == account and record.product not in products):
                products.append(record.product);
                
            
        products = sorted(products);
        
        #####################################################
        # 2. generte date list
        #####################################################
        dates = [];
        start = datetime.datetime.strptime(self.startDate, '%Y%m%d');
        end = datetime.datetime.strptime(self.endDate, '%Y%m%d');
        
        iter = start;
        while(iter <= end):
            #only week day is added
            if(iter.weekday() < 5):
                dates.append(iter);
            # forward 1 day
            iter = iter + datetime.timedelta(days=1);
        
       
        #################################
        #3. populate the table for account
        ################################## 
        table = [];
        for date in dates:
            date_row = [];
            for product in products:
                summaries = self.getAccountProductDateSummary(account, product, date, MFG=MFG)
                if(len(summaries) == 0):
                    tmp = tu.AccountProductSummary();
                    tmp.account = account;
                    tmp.product = product;
                    date_row.append(tmp);
                else:
                    date_row.append(summaries[0]);
            table.append(date_row);
            
        return (dates, products, table);
    
    
    def buildCurrencyReportTable(self, type='profit', MFG=True):
        #####################################################
        # 1. generate date list
        #####################################################
        dates = [];
        start = datetime.datetime.strptime(self.startDate, '%Y%m%d');
        end = datetime.datetime.strptime(self.endDate, '%Y%m%d');
        
        iter = start;
        while(iter <= end):
            #only week day is added
            if(iter.weekday() < 5):
                dates.append(iter);
            # forward 1 day
            iter = iter + datetime.timedelta(days=1);
        
        #####################################################
        # 2. generate currency account information
        #####################################################
        headerBook = {}
        for record in self.tradeRecords:
            if(type=="profit"):
                curr = record.currency;
            else:
                curr = record.fee_currency;
            
            if(curr not in headerBook):
                headerBook[curr] = [];
                headerBook[curr].append(record.account);
            else:
                if(record.account not in headerBook[curr]):
                    headerBook[curr].append(record.account);
                else:
                    continue;
        
        # sort the header
        for curr in headerBook:
            accounts = headerBook[curr];
            accounts = sorted(accounts);
            headerBook[curr] = accounts;
            
        #####################################################
        # 3. generate currency table
        #####################################################
        table = [];
        for date in dates:
            summaries = self.getTradeSummaries(date, MFG=MFG);
            if(type == 'profit'):
                book = tu.get_PL_per_currency(summaries);
            else:
                book = tu.get_fee_per_currency(summaries);
            table.append(book);
            
        return (dates, headerBook, table);
            
     
    def buildProductReportTable(self, MFG=True):
        #####################################################
        # 1. generate date list
        #####################################################
        dates = [];
        start = datetime.datetime.strptime(self.startDate, '%Y%m%d');
        end = datetime.datetime.strptime(self.endDate, '%Y%m%d');
        
        iter = start;
        while(iter <= end):
            #only week day is added
            if(iter.weekday() < 5):
                dates.append(iter);
            # forward 1 day
            iter = iter + datetime.timedelta(days=1);
            
        #####################################################
        # 2. generate product header list
        #####################################################
        headers = [];
        for record in self.tradeRecords:
            prod = record.product;
            if(prod not in headers):
                headers.append(prod);
                
        headers = sorted(headers)
        #####################################################
        # 3. populate table with data
        #####################################################
        table = [];
        for date in dates:
            data_row = [];
            for product in headers:
                summaries = self.getTradeSummaries(date, product=product, MFG=MFG);
                total_net_profit = 0;
                for sum in summaries:
                    if(product == "SNK"):
                        total_net_profit += sum.profit;
                    else:
                        total_net_profit += (sum.profit - sum.commission - sum.gst);
                    
                total_net_profit = round(total_net_profit, 3);
                data_row.append(total_net_profit);
                
            table.append(data_row);
                    
        return (dates, headers, table);
    
    
    def buildProductPL_FeeSummary(self, MFG=True):
        
        # calculate summaries
        summaries = self.getOverallTradingSummaries(MFG=MFG);
        
        # get and sort product list
        product_list = [];
        for sum in summaries:
            if(sum.product not in product_list):
                product_list.append(sum.product);
        product_list = sorted(product_list);
        
        # calculate summaries per product
        overall_sum_list = {}
        for product in product_list:
            profit = 0;
            comm = 0;
            gst = 0;
            for sum in summaries:
                if(sum.product == product):
                    profit += sum.profit;
                    comm += sum.commission;
                    gst += sum.gst;
            overall_sum_list[product] = (profit,comm,gst);
            
            
        return overall_sum_list;
    
    def buildLotPerExchangeReport(self):
        #####################################################
        # 1. generate date list
        #####################################################
        dates = [];
        start = datetime.datetime.strptime(self.startDate, '%Y%m%d');
        end = datetime.datetime.strptime(self.endDate, '%Y%m%d');
        
        iter = start;
        while(iter <= end):
            #only week day is added
            if(iter.weekday() < 5):
                dates.append(iter);
            # forward 1 day
            iter = iter + datetime.timedelta(days=1);
         
        #####################################################
        # 2. generate product header list
        #####################################################
        headers = [];
        for record in self.tradeRecords:
            exchange = record.exchange;
            if(exchange not in headers):
                headers.append(exchange);
        headers = sorted(headers);
        
        
        #####################################################
        # 3. generate space holder
        #####################################################
        table = {};
        for date in dates:
            mfgdate = date.strftime('%Y%m%d');
            table[mfgdate] = {}
            for exchange in headers:
                if(exchange not in table[mfgdate]):
                    table[mfgdate][exchange] = (0, 0, 0);
                    
        
        #####################################################
        # 4. populate with data
        ##################################################### 
        for record in self.tradeRecords:
            mfgdate = record.mfgdate;
            exchange = record.exchange;
            
            (buy, sell, total) = table[mfgdate][exchange];
            if(record.bought_sold == 'B'):
                buy += record.quantity;
            else:
                sell += record.quantity;
            total = buy + sell;
            table[mfgdate][exchange] = (buy, sell, total);
        return (dates, headers, table);
               
            
    def generateCurrencyCSVReport(self, dates, headerBook, table):
        
        report = [];
        
        # reserve the first column for dates
        firstLine = ','
        for curr in headerBook:
            currList = headerBook[curr];
            # populate Currency header
            firstLine += curr;
            for i in range(len(currList)):
                firstLine += ','
        
        report.append(firstLine);
         
        # reserve the first column for dates       
        secondLine = ',';
        for curr in headerBook:
            currList = headerBook[curr];
            # populate Currency header
            for i in range(len(currList)):
                secondLine += '%s,' % currList[i];
         
        report.append(secondLine);       
        
        
        # populate the table content
        for i in range(len(dates)):
            line = '%s,' % dates[i].strftime('%Y%m%d');
            book = table[i];
            
            for curr in headerBook:
                # if the book has the currency
                if curr in book:
                    # iterate all account under this currency
                    for acc in headerBook[curr]:
                        #if the book has the currency and account
                        if acc in book[curr]:
                            line += '%s,' % book[curr][acc];
                        else:
                            line += '0,';
                # if the book has no such currency
                else:
                    for acc in headerBook[curr]:
                        line += '0,'               
            report.append(line);
            
        return report;
                    
                    
    
    def generateProductCSVReport(self, dates, headers, table):
        report = [];
        
        # prepare the first line
        firstLine = ''
        for product in headers:
            firstLine += ',%s' % product
        report.append(firstLine);
        
        # prepare table body
        for i in range(len(dates)):
            line = '%s' % dates[i].strftime('%Y%m%d');
            row = table[i];
            for value in row:
                line += ',%s' % value
            
            report.append(line)
            
        return report;
    
    
    def generateLotPerExchangeCSVReport(self, dates, headers, table):
        report = [];
        
        firstLine = '';
        for exchange in headers:
            firstLine += ',%s,,'%exchange;
            
        report.append(firstLine);
        
        secondLine = '';
        for i in range(len(headers)):
            secondLine += ',BUY,SELL,TOTAL';
        
        report.append(secondLine);
        
        for date in dates:
            line = '';
            date_str= date.strftime('%Y%m%d');
            line += '%s'%date_str;
            for exchange in headers:
                (buy,sell,total) = table[date_str][exchange];
                line += ',%s,%s,%s'%(buy,sell,total);
            report.append(line);
        return report;
        
    
    def generateCSVReport(self, account, dates, products, table):
        
        report = [];
        
        # account
        report.append("ACCOUNT:,%s" % account);
        
        # product header
        product_header = ','
        for product in products:
            product_header += '%s,,,,,,,' % product;
        report.append(product_header);
        
        # detail header
        d_header = ''
        for i in range(len(products)):
            d_header += ',buy qty,sell qty, gross PL, commission, gst, net PL,';
            
        report.append(d_header);
        
        # rows:
        for i in range(len(table)):
            line = '%s' % dates[i].strftime('%Y%m%d');
            for j in range(len(table[i])):
                t = table[i][j];
                if(t.currency != t.fee_currency):
                    line += ',%s,%s,%s,%s,%s,%s,' % (t.buy_qty, t.sell_qty, t.profit, t.commission, t.gst, t.profit);
                else:
                    line += ',%s,%s,%s,%s,%s,%s,' % (t.buy_qty, t.sell_qty, t.profit, t.commission, t.gst, t.profit - t.commission - t.gst);
            report.append(line);
                
        return report
    
    
    def summarisePLPerAccount(self, table):
        assert(len(table) != 0);
        
        # column number
        product_num = len(table[0]);
        product_sum = [];
        
        for i in range(product_num):
            total_profit = 0;
            total_comm = 0;
            total_gst = 0;
            for j in range(len(table)):
                record = table[j][i];
                total_profit += record.profit;
                total_comm += record.commission;
                total_gst += record.gst;
                
            # determine whether product is SNK
            product = table[0][i].product;
            
            if(product=="SNK"):
                net_pl = total_profit;
            else:
                net_pl = total_profit - total_comm - total_gst;
            
            
            product_sum.append((total_comm, total_gst, net_pl));
            
        return product_sum;
        
    
    def generatePLPerAccountCSV(self, account, header, product_sums):
        report = [];
        report.append("ACCOUNT,%s"%account);
        
        product_line = "PRODUCT,"
        for product in header:
            product_line += '%s,'%product;
        report.append(product_line);
        
        com_line = 'COM,';
        for record in product_sums:
            com_line += '%s,'%record[0];
        report.append(com_line);
        
        gst_line = 'GST,';
        for record in product_sums:
            gst_line += '%s,'%record[1];
        report.append(gst_line);
        
            
        npl_line = 'NPL,';
        for record in product_sums:
            npl_line += '%s,'%record[2];
        report.append(npl_line);
        
        
        return report;
    
    
    def summarisePLPerCurrency(self, headerBook, table):
        sum_book = {};
        
        # initialize
        for curr in headerBook:
            sum_book[curr] = {};
            for account in headerBook[curr]:
                sum_book[curr][account] = 0;
                
        for book in table:
            for curr in book:
                for account in book[curr]:
                    sum_book[curr][account] += book[curr][account];
                    
        
        return sum_book;
        
        
    def generatePLPerCurrencyCSV(self, summaryBook, PnL=True):
        report = [];
        
        if(PnL is True):
            report.append('PnL PER CURRENCY');
        else:
            report.append('FEE PER CURRENCY');
        
        first_line = 'CURRENCY,';
        for curr in summaryBook:
            first_line += '%s'%curr;
            for i in range(len(summaryBook[curr].keys())):
                first_line += ',';
        report.append(first_line);
        
        acc_line = 'ACCOUNT,';
        for curr in summaryBook:
            for account in summaryBook[curr]:
                acc_line += '%s,'%account
        report.append(acc_line);
        
        pl_line = "TOTAL,";
        for curr in summaryBook:
            for account in summaryBook[curr]:
                pl_line += '%s,'%summaryBook[curr][account];
        report.append(pl_line);
        
        sum_line = 'SUM,';
        for curr in summaryBook:
            total = 0;
            for acc in summaryBook[curr]:
                total += summaryBook[curr][acc];
            sum_line += '%s %s'%(curr,total);
            for i in range(len(summaryBook[curr].keys())):
                sum_line += ',';
        report.append(sum_line);
        return report;     
     
     
        
    def sumarrisePLPerProduct(self, table):
        assert(len(table) !=0 );
        
        product_sums = [];
        product_num = len(table[0]);
        
        for i in range(product_num):
            PL = 0;
            for j in range(len(table)):
                PL += table[j][i];
            product_sums.append(PL);   
        return product_sums;
    
    def generatePLPerProductSummaryCSV(self, header, product_sums):
        report = [];
        report.append("SUMMARY PnL PER PRODUCT");
        
        # get product list;
        h_line = ",".join(header);
        h_line = ',' + h_line;
        report.append(h_line);
         
        pl = 'PnL PER PRODUCT,';
        for product in header:
            item = product_sums[product];
            if(product == "SNK"):
                pl += "%s,"%item[0];
            else:
                pl += "%s,"%(item[0] - item[1] - item[2]);   
        report.append(pl);
        
        comm = 'COMMSSION PER PRODUCT,'
        for product in header:
            comm += "%s,"%product_sums[product][1];
        report.append(comm);   
        
        gst = 'GST PER PRODUCT,'
        for product in header:
            gst += "%s,"%product_sums[product][2];
        report.append(gst);   
        
        
        lots = 'LOT PER PRODUCT,'
        for product in header:
            total_lots = 0;
            for rec in self.tradeRecords:
                if(rec.product == product):
                    total_lots += rec.quantity;
            
            lots += '%s,'%total_lots;
        report.append(lots);
        
        return report;
            
    
    def summariseLotsPerExchange(self, table):
        assert(len(table) != 0 );
        
        lot_sums = {};
        
        exchanges = table[table.keys()[0]].keys();
        for ex in exchanges:
            buy_qty = 0;
            sell_qty = 0;
            total_qty = 0;
            for mfgdate in table:
                (b,s,t) = table[mfgdate][ex];
                buy_qty += b;
                sell_qty += s;
                total_qty += t;
            lot_sums[ex] = (buy_qty,sell_qty,total_qty);
        return lot_sums;
        
    
    def generateLotsSummaryCSV(self, header, lot_sums):
        
        report = [];
        report.append("SUMMARY TOTAL LOTS TRADED PER EXCHANGE");
        
        # get product list;
        h_line = ",".join(header);
        h_line = 'EXCHANGE,' + h_line;
        report.append(h_line);
         
        content = 'TOTAL,';
        
        for ex in header:
            content += "%s,"%lot_sums[ex][2];
        
        report.append(content);
        
        return report;
        
